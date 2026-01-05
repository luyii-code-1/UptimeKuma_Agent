# UptimeKuma Agent

[English](README.md) | [简体中文](README_zh-CN.md)

A monitoring client for UptimeKuma, designed to monitor shell commands, systemd services, and other types of services.

[Warning] This repository is still under active development.

# Understanding the Project

## What It Is
UptimeKuma Agent is a client for the **UptimeKuma Push** monitoring type. It sends data (online status, ping, messages) to the Push URL provided by UptimeKuma, enabling webhook-like monitoring of shell commands, systemd services, or other services.

## Why This Project Exists
I (luyii-code-1) needed to remotely monitor several local services (such as Npc, Frpc, Frps, etc.). While UptimeKuma is a powerful monitoring system, it mainly supports HTTP checks and local Docker hosts. However, it does support HTTP Push monitoring. This project was created to act as a Push conversion client, allowing shell commands, systemd services, and other local services to be monitored through UptimeKuma.

## How It Works
The mechanism is simple. After the user completes the configuration in `config.json`, the client polls services based on the configuration and searches for specific keywords in the output. The presence of predefined keywords is used to determine the service status (e.g., `Failed`, `Active`).  
In addition, by leveraging the `requests` library, the client can also act as a proxy for UptimeKuma, which is particularly friendly for NAT-restricted environments such as mainland China.

## An Important Note
This project is not intended for formal production use. Before development, I experimented with solutions such as Zabbix and OneUptime (self-hosted and SaaS). For individual developers, these options were often too complex and resource-intensive. As a long-time UptimeKuma user, I decided to build on its existing ecosystem and extend its Push mechanism to provide lightweight monitoring for local services.

For production environments, however, resource usage and learning cost are usually not major concerns. Therefore, I do not recommend using this project for enterprise monitoring. Mature solutions such as Zabbix remain a better fit in those scenarios.

## Security Considerations
Because this project runs on the client host and may require root privileges, security is a critical concern. The project must not evolve into a backdoor or trojan. Under the current plan, security is addressed through:
- HTTPS-only communication  
- Permission checks  
- Code quality and security scanning (CodeQL)  
- Manual review  

This focus on security and transparency is also one of the reasons the project is open source.

## Development Status
- [x] Bash command monitoring (keyword-based)
- [ ] Systemd service monitoring
- [x] HTTP request monitoring
- [ ] Threaded polling loop
- [ ] Comprehensive logging
- [ ] Debug mode
- [ ] Cloud-based configuration
- [ ] Hot updates / cloud control / cloud feedback / remote execution
- [ ] Improved security checks

# Planned Features

- Systemd service monitoring  
- Custom bash command monitoring  
- HTTP request monitoring  
- Multi-threaded monitoring mechanism  
- Comprehensive logging  
- Ease of use  
- One-click cloud control  

### Installation

Under development.

### Usage

Two usage modes are currently planned:
- **Full installation**: `main.py + config.json`, running as a system service (systemd)
- **Lightweight installation**: `main.py --config={json_detail}`

### Configuration

Under development.

### Warning

This program is developed in a macOS environment and may not be fully compatible with Windows or Linux systems.

### License

Please refer to the LICENSE file.
