# 贡献指南

[English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING_zh-CN.md)

感谢您对 UptimeKuma Agent 项目的兴趣！本指南将帮助您了解如何为项目做出贡献。

## 代码提交要求

### 代码质量标准
- **禁止通篇 AI 生成代码**：提交的代码必须是人工编写或经过人工审核的，**不得使用 AI 工具生成整个文件或大段代码**。
- **合理注释**：代码中应包含适当的注释，解释复杂逻辑、函数用途和关键步骤。注释应清晰、简洁，并使用中文或英文。

### CI/CD 检查
在提交代码之前，请确保您的更改通过以下自动化检查：
- **PyLint 分数**：代码必须达到 PyLint 分数大于 7。PyLint 用于检查代码质量、风格和潜在错误。
- **CodeQL 扫描**：代码必须通过 CodeQL 安全扫描，确保没有安全漏洞。

### 审核流程
- 提交 Pull Request (PR) 后，CI 将自动运行上述检查。
- 如果 CI 通过，代码将进入 Copilot 审核阶段。Copilot 将检查代码的整体质量、合规性和最佳实践，之后由至少一位贡献者审核。

## 如何贡献
1. Fork 本仓库。
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 打开 Pull Request。

## 联系我们
如果您有任何问题，请通过 Issues 或 Discussions 与我们联系。