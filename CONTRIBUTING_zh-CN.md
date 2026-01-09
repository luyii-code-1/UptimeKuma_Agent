# 贡献指南

[English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING_zh-CN.md)

感谢您对 UptimeKuma Agent 项目的兴趣！本指南将帮助您了解如何为项目做出贡献。

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

# 代码提交要求

### 代码质量标准
- **禁止通篇 AI 生成代码**：提交的代码必须是人工编写或经过人工审核的，**不得使用 AI 工具生成整个文件或大段代码**。
- **合理注释**：代码中应包含适当的注释，解释复杂逻辑、函数用途和关键步骤。注释应清晰、简洁，并使用英文注释（多语言文档除外）。

### CI 检查
在提交代码之前，请确保您的更改通过以下自动化检查：
- **PyLint 分数**：代码必须达到 PyLint 分数大于 7。PyLint 用于检查代码质量、风格和潜在错误。
- **CodeQL 扫描**：代码必须通过 CodeQL 安全扫描，确保没有安全漏洞。

### 审核流程
- 提交 Pull Request (PR) 后，CI 将自动运行上述检查。
- 如果 CI 通过，代码将进入 Copilot 审核阶段。Copilot 将检查代码的整体质量、合规性和最佳实践，之后由我（Owner）审核，通过后适时合并。

## 如何贡献
1. Fork 本仓库d `release` 分支
2. 创建您的功能分支
3. 提交更改
4. 推送到分支
5. 打开 Pull Request到 `release` 分支

## 细节注意
为了保证社区可维护性，请尽量在代码中使用标准英语进行注释，避免出现其他语言（多语言文档除外）
目前程序设计架构与Pull Request Merge的特性并不友好，但是你依然能够通过Issuse或Pull Request发出疑问或提交代码，我会手动去合并代码

## 联系我们
如果您有任何问题，请通过 Issues 或 Discussions 与我们联系。