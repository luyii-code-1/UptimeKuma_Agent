# UptimeKuma Agent

[English](README.md) | [简体中文](README_zh-CN.md)

This is a monitoring client for UptimeKuma, designed to monitor shell commands, systemd services, or other services.

[![CodeQL](https://github.com/luyii-code-1/UptimeKuma_Agent/actions/workflows/github-code-scanning/codeql/badge.svg?branch=main)](https://github.com/luyii-code-1/UptimeKuma_Agent/actions/workflows/github-code-scanning/codeql)
[![Pylint](https://github.com/luyii-code-1/UptimeKuma_Agent/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/luyii-code-1/UptimeKuma_Agent/actions/workflows/pylint.yml)

## About the Project

### What Is This
UptimeKuma Agent is a client for the UptimeKuma **Push** monitor type. It sends data (online status, ping, message) to the Push endpoint provided by UptimeKuma, enabling webhook-like monitoring of shell commands, systemd services, or other services.

### Why This Project Exists
I (luyii-code-1) need to remotely access and monitor some local services (such as Npc, Frpc, Frps, etc.), so I required a monitoring system similar to UptimeKuma. However, UptimeKuma only supports HTTP checks and local Docker hosts. Since it supports HTTP Push monitoring, a Push-conversion client was needed to monitor shell commands, systemd services, or other services.

### How It Works
The principle is straightforward. After the user completes the configuration in `config.json`, the client polls services according to the configuration file and performs keyword matching. If specified words or phrases are found, the service status can be determined (e.g., Failed, Active). Additionally, with the help of the `requests` library, the client can act as a proxy for UptimeKuma, which is particularly friendly for NAT environments in mainland China.

### An Important Note
This project is not intended for formal production use. Before development, I attempted solutions such as Zabbix, OneUptime (self-hosted/SaaS), etc., but these were overly complex and resource-intensive for an individual developer. Since I am very fond of UptimeKuma, I decided to leverage its existing ecosystem and adapt it by converting Push monitoring to continuously monitor local services.

For production environments, however, resource usage and ease of learning are not major concerns. Therefore, I do not recommend enterprises or organizations use this project for monitoring. Established solutions like Zabbix, as a mature open-source option, are likely a better choice.

### Security Considerations
This project runs on the client host and may require root privileges, so security is critical. The project must not evolve into a backdoor or Trojan. Under the current plan, security will be ensured through HTTPS-only communication, permission checks, code quality and security scanning (CodeQL), and manual reviews. This is also one of the reasons the project is open source.

## Development Status
- [x] Bash command monitoring (keyword-based)
- [x] HTTP request monitoring
- [x] Debug mode
- [x] Threaded loop
- [x] Systemd service monitoring
- [x] Slim installation mode
- [ ] Comprehensive logging (long-term plan)
- [ ] Enhanced security checks (long-term work)
- [ ] Cloud-based configuration (long-term plan)
- [ ] Hot updates / cloud control / cloud feedback / cloud execution (long-term plan)

## Installation

1. Download the corresponding asset from the Release page.
2. [Configure the `conf.json` file](#configuration-file).
3. Install Python, pip, and required modules.
4. Create a process daemon (systemd or screen).
5. Run `python3 main.py`.

### Usage

Currently, two modes are planned:

- **Fat installation (default)**: (`main.py` + `config.json`) and a system service (systemd)
- **Slim installation (under development)**: pass `--config={json_detail}` to `main.py`

### Configuration File

**Warning**: This project **strongly depends** on a **correct configuration file**. If the configuration file is incorrect, the program may not work properly and may cause **serious consequences**.

Configuration file: `./conf.json`  
Use the [online configuration tool](https://luyii-code-1.github.io/UptimeKuma_Agent/)

#### Decision Logic

- **Bash**:  
  Command output → split lines by `\n` → `readline` filtering → keyword matched?  
  - Yes → warnword matched?
    - No → status online  
    - Yes → status offline
  - No → status offline

- **HTTP**:  
  Response → `statuscode` matched → split response body by `\n` → `readline` filtering → `keyword` matched?  
  - Yes → `warnword` matched?
    - No → status online  
    - Yes → status offline
  - No → status offline

#### API Key

In UptimeKuma, add a monitor:
- Type: Passive Monitor – Push
- Push URL (example):  
  `http://127.0.0.1:3001/api/push/ib67jWmQ8G?status=up&msg=OK&ping=`
----------------------------------^^^^^^^^^^-----------------------

Extract the content between `/push/` and `?status=`.

### Warnings

For different platforms, Bash check commands usually differ. For example, using `ping` to check host availability:

- **Windows (Terminal)**:  
  Recommended: `ping 127.0.0.1 -n 1` *(send 1 ICMP packet to loopback)*

- **Linux (Ubuntu)**:  
  Recommended: `ping 127.0.0.1 -c 1` *(send 1 ICMP packet to loopback)*

- **macOS (OS X 26 Tahoe)**:  
  Recommended: `ping 127.0.0.1 -t 1` *(send 1 ICMP packet to loopback)*

The program does not check command differences across platforms. Therefore, when migrating between platforms, you **must** modify the `"command"` section. Otherwise, monitoring may fail due to a 30-second timeout.

## Troubleshooting
`main.py` supports the `--debug` parameter.

### License
Please see the LICENSE file.

### Contributing
The current program architecture is not very friendly to Pull Request merges. However, you are still welcome to raise questions via Issues or submit code via Pull Requests. I will manually review and merge contributions.
