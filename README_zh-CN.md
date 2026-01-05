# UptimeKuma Agent

[English](README.md) | [简体中文](README_zh-CN.md)

一个用于 UptimeKuma 的监控客户端，用于监控 shell 命令、systemd 服务或其他服务。

[警告] 此仓库仍在开发中
# 了解项目

## 这是什么
UptimeKuma Agent 是一个用于 UptimeKuma Push监控类型的客户端，通过Kuma提供的Push地址传输数据（在线状态，Ping，Msg），以类似Webhook的方式监控 shell 命令、systemd 服务或其他服务。
## 为什么会产生这个项目
由于我（luyii-code-1）需要对一些本地服务（如Npc，Frpc， Frps等等）进行远程连接，所以需要一个类似UptimeKuma的监控系统，但是UptimeKuma只支持HTTP请求和本地的Docker宿主，，但是他支持Http Push监控，所以需要一个类似UptimeKuma的Push转化客户端，用于监控shell命令、systemd服务或其他服务。
## 如何工作
原理非常简单，用户在Config.json配置完成后，客户端根据配置文件对服务进行轮询和关键字查找，找到制定字或词即可判别服务状态（如Failed，Active），当然，借助Requests，客户端也许能充当UptimeKuma的代理使用，这对于中国大陆的NAT环境非常友好
## 必须说明的一点
本项目注定不会被正式生产环境使用，在开发前，我曾尝试部署Zabbix/OneUptime自托管/Saas等等方案，但是对于个人开发者还是过于繁琐，浪费资源，正好我非常喜欢UptimeKuma，因此我觉决定借助UptimeKuma已有的生态进行改造，使用Push的转换来对本地的服务经常监控。
但是对于生产环境来说，资源和易学性并不是问题，因而我并不建议企业等使用本项目进行监控服务，或许Zabbix也还是开开源方案的更好实现
## 安全性问题
本项目毕竟是安装在客户主机上的，大概需要root权限运行，因而安全性非常重要，本项目不应被演化为后门木马（Torjan/Backdoor），目前计划下我会通过HTTPS Only，权限检查，代码质量安全性扫描（CodeQL），人工复核保证安全性，这也是我开源的目的之一

## 开发进度
- [x] Bash命令监控（关键字）
- [ ] Systemd 服务监控
- [x] Http 请求监控
- [ ] 线程循环
- [ ] 完善的日志记录
- [ ] Debug模式
- [ ] 云配置
- [ ] 热更新/云控制/云反馈/云执行
- [ ] 完善的安全性检查

# 未来功能

- Systemd 服务监控
- 自定义 bash 命令监控
- HTTP 请求监控
- 多线程监控机制
- 完善的日志记录
- 易于使用
- 一键云端控制

### 安装

正在开发中

### 使用方法

目前计划由两种，
胖安装：（main.py+config.json）和系统服务（systemd）
瘦安装：（main.py --config={json_detail}）

### 配置

正在开发中

### 警告

此程序在 macOS 环境中开发，可能与 Windows 或 Linux 系统不完全兼容。

### 许可证

请查看 LICENSE 文件。