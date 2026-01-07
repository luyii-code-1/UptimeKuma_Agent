# Contribution Guide

[English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING_zh-CN.md)

Thank you for your interest in the UptimeKuma Agent project! This guide explains how you can contribute to the project.

# Understanding the Project

## What It Is
UptimeKuma Agent is a client designed for the **UptimeKuma Push** monitoring type. It sends data (online status, ping, messages) to the Push URL provided by UptimeKuma, enabling webhook-like monitoring of shell commands, systemd services, or other types of services.

## Why This Project Exists
I (luyii-code-1) needed a way to remotely monitor several local services (such as Npc, Frpc, Frps, etc.). While UptimeKuma is an excellent monitoring tool, it primarily supports HTTP checks and local Docker hosts. However, it does support HTTP Push monitoring. This project was created to act as a Push conversion client, allowing shell commands, systemd services, and other local services to be monitored through UptimeKuma.

## How It Works
The design is straightforward. After the user completes the configuration in `config.json`, the client periodically polls services according to the configuration and searches for specific keywords in the output. The presence of predefined keywords determines the service status (e.g., `Failed`, `Active`).  
Additionally, by leveraging the `requests` library, the client may also act as a proxy for UptimeKuma, which is particularly useful in NAT-restricted environments such as mainland China.

## An Important Note
This project is not intended for formal production environments. Before starting development, I experimented with solutions such as Zabbix, OneUptime (self-hosted and SaaS), and others. For individual developers, these options often felt overly complex and resource-intensive. Since I am a long-time fan of UptimeKuma, I decided to build on its existing ecosystem by extending its Push mechanism to enable lightweight monitoring of local services.

For production use cases, however, resource consumption and ease of learning are generally not limiting factors. Therefore, I do not recommend using this project for enterprise or production monitoring. Established solutions like Zabbix remain a more appropriate choice in such scenarios.

## Security Considerations
Because this project runs on the client host and may require root privileges, security is a critical concern. The project must not evolve into a backdoor or trojan. Under the current plan, security is addressed through:
- HTTPS-only communication  
- Permission checks  
- Code quality and security scanning (CodeQL)  
- Manual code review  

This focus on transparency and review is also one of the reasons the project is open source.

# Code Submission Requirements

### Code Quality Standards
- **No fully AI-generated code**: Submitted code must be written by humans or thoroughly reviewed by humans. Using AI tools to generate entire files or large blocks of code is not allowed.
- **Reasonable comments**: Code should include appropriate comments explaining complex logic, function purposes, and key steps. Comments must be clear, concise, and written in English (except for multilingual documentation).

### CI Checks
Before submitting your changes, ensure that they pass the following automated checks:
- **PyLint score**: The code must achieve a PyLint score greater than 7. PyLint is used to evaluate code quality, style, and potential issues.
- **CodeQL scan**: The code must pass CodeQL security analysis with no detected vulnerabilities.

### Review Process
- After a Pull Request (PR) is submitted, CI will automatically run the checks listed above.
- If CI passes, the code enters the Copilot review stage. Copilot evaluates overall quality, compliance, and best practices, after which I (the owner) perform a final review and merge when appropriate.

## How to Contribute
1. Fork the repository’s `dev` branch  
2. Create your feature branch  
3. Commit your changes  
4. Push the branch  
5. Open a Pull Request targeting `dev`

## Additional Notes
To maintain long-term community maintainability, please use standard English for code comments and avoid other languages (except in multilingual documentation).

## Contact
If you have any questions, please reach out via Issues or Discussions.
