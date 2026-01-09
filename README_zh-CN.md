# UptimeKuma Agent

[English](README.md) | [简体中文](README_zh-CN.md)

这是一个用于 UptimeKuma 的监控客户端，用于监控 shell 命令、systemd 服务或其他服务。

## 了解项目

### 这是什么
UptimeKuma Agent 是一个用于 UptimeKuma Push监控类型的客户端，通过Kuma提供的Push地址传输数据（在线状态，Ping，Msg），以类似Webhook的方式监控 shell 命令、systemd 服务或其他服务。
### 为什么会产生这个项目
由于我（luyii-code-1）需要对一些本地服务（如Npc，Frpc， Frps等等）进行远程连接，所以需要一个类似UptimeKuma的监控系统，但是UptimeKuma只支持HTTP请求和本地的Docker宿主，，但是他支持Http Push监控，所以需要一个类似UptimeKuma的Push转化客户端，用于监控shell命令、systemd服务或其他服务。
### 如何工作
原理非常简单，用户在Config.json配置完成后，客户端根据配置文件对服务进行轮询和关键字查找，找到制定字或词即可判别服务状态（如Failed，Active），当然，借助Requests，客户端也许能充当UptimeKuma的代理使用，这对于中国大陆的NAT环境非常友好
### 必须说明的一点
本项目注定不会被正式生产环境使用，在开发前，我曾尝试部署Zabbix/OneUptime自托管/Saas等等方案，但是对于个人开发者还是过于繁琐，浪费资源，正好我非常喜欢UptimeKuma，因此我觉决定借助UptimeKuma已有的生态进行改造，使用Push的转换来对本地的服务经常监控。
但是对于生产环境来说，资源和易学性并不是问题，因而我并不建议企业等使用本项目进行监控服务，或许Zabbix也还是开开源方案的更好实现
### 安全性问题
本项目毕竟是安装在客户主机上的，大概需要root权限运行，因而安全性非常重要，本项目不应被演化为后门木马（Torjan/Backdoor），目前计划下我会通过HTTPS Only，权限检查，代码质量安全性扫描（CodeQL），人工复核保证安全性，这也是我开源的目的之一

## 开发进度
- [x] Bash命令监控（关键字）
- [x] Http 请求监控
- [x] Debug模式
- [x] 线程循环
- [ ] Systemd 服务监控（即将完成）
- [ ] 完善的日志记录（远期计划）
- [ ] 完善的安全性检查（长期工作）
- [ ] 云配置（远期计划）
- [ ] 瘦安装运行
- [ ] 热更新/云控制/云反馈/云执行（远期计划）


## 安装

- 1.下载Release下Asset对应版本
- 2.[配置conf.json文件](#配置文件)
- 3.安装Python,Pip与必须模块
- 4.创建进程守护(systemd或screen)
- 5.`python3 main.py`


### 使用方法

目前计划由两种：
胖安装(默认)：（`main.py`+`config.json`）和系统服务（systemd）
瘦安装(待开发)：（对`main.py`传入`--config={json_detail}`）

### 配置文件

[警告]本项目**强依赖**于**正确的配置文件**，如果配置文件出现问题，程序可能不会正常工作，并可能**造成严重后果**

配置文件`./conf.json`
**以下所有配置缺一不可！！！**
示例：
    {
        "meta":{ ←---程序设置
            "enabled": true, ←---是否启用节点（如果不启用程序将在启动后马上退出）
            "cloud_control": false,←---是否启用云端控制（未开发）
            "cloud_control_url": "api_point"←---云端控制地址
            },
        "region":{←---节点信息
            "node_name": "Example",←---节点名称
            "server": "http://127.0.0.1:3001/api/push/" , ←---**UptimeKuma Push API端点**，**`/api/push`后带上`/`**:`/api/push/`
            "token": ""←---用于访问API端点的验证密钥（基于你自己配置的端点服务自行配置，默认为空不影响使用）
            },
        "monitors":{←---所有监控的配置
            "1":{←---单项名称（自定义，**不可重复**）
                "name": "shell test(ping)",←---显示名称
                "enabled": true,←---是否启用检查，不启用将提交Down状态
                "type": "bash",←---**类型，目前支持“http”，“bash”两种**
                "command": "ping 8.8.8.8 -t 1",←---**执行的命令**
                "keyword": ["1 packets received"],←---**需要命中在线关键词tpye=list**
                "warnword": [],←---**需要命中的离线关键词tpye=list**
                "readline": 0,←---输出内容从下到上用于关键词检查的行数，0为使用全部（自动删除末尾空行）
                "ping": false,←---返回Ping数据（默认开启暂不支持修改）
                "datalevel": 0,←---返回的日志等级（未开发）
                "api": "CsUGkIxISU"←---**重要**监控项API，见API密钥
            },
            "2":{
                "name": "http test",
                "enabled": true,
                "type": "http",
                "url": "https://www.baidu.com",
                "statuscode": [200,301,302],←---**用于判断在线状态的状态码**
                "keyword": ["head"],
                "ping": false,
                "readline": 0,
                "warnword": [],
                "datalevel": 0,
                "api": "kcwjnVGRwx"
            }
        }
    }
#### 判断逻辑

Bash:返回内容 -→ 以`\n`切割每行 -→ `readline`筛选 -→ keyword命中? --*是*-→ warnword命中 --*否*-→ 状态在线       否则状态不在线
Http:返回内容 -→ `statuscode`命中 -→ 以`\n`切割每行返回内容 -→ `readline`筛选 -→ `keyword`命中? --*是*-→ `warnword`命中 --*否*-→ 状态在线       否则状态不在线

#### API密钥

UptimeKuma - 添加监控项
类型 - 被动监控类型 - Push
推送URL：（E.G.）http://127.0.0.1:3001/api/push/ib67jWmQ8G?status=up&msg=OK&ping=
-----------------------------------------------^^^^^^^^^^-----------------------
取`/push/`后`?status=`前的内容
### 警告

对于不同平台，Bash Check命令通常不通，比如使用`ping`检查主机活跃态：

对于`Windows(Terminal)`      推荐的语句为`ping 127.0.0.1 -n 1` *向回环发送1个ICMP包*
对于`Linux(Ubuntu)`          推荐的语句为`ping 127.0.0.1 -c 1` *向回环发送1个ICMP包*
对于`MacOS(OS X 26 Tahoe)`   推荐的语句为`ping 127.0.0.1 -t 1` *向回环发送1个ICMP包*

程序不会检查不同平台的命令差异，因此请在迁移平台时**务必**修改"command"块，**否则**监控可能会应为30s超时未结束而出现错误

## 排障
`main.py`支持`--debug`参数

### 许可证

请查看 LICENSE 文件

### 参与开发

目前程序设计架构与Pull Request Merge的特性并不友好，但是你依然能够通过Issuse或Pull Request发出疑问或提交代码，我会手动去合并代码