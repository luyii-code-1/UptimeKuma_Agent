# UptimeKuma Agent

[English](README.md) | [简体中文](README_zh-CN.md)

This is a monitoring client for UptimeKuma, used to monitor shell commands, systemd services, or other services.

[![Pylint](https://github.com/luyii-code-1/UptimeKuma_Agent/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/luyii-code-1/UptimeKuma_Agent/actions/workflows/pylint.yml)
[![CodeQL](https://github.com/luyii-code-1/UptimeKuma_Agent/actions/workflows/github-code-scanning/codeql/badge.svg?branch=main)](https://github.com/luyii-code-1/UptimeKuma_Agent/actions/workflows/github-code-scanning/codeql)
## About the Project

### What is this
UptimeKuma Agent is a client designed for the UptimeKuma Push monitoring type. It transmits data (online status, ping, message) via the Push endpoint provided by Kuma, and monitors shell commands, systemd services, or other services in a webhook-like manner.

### Why this project exists
Because I (luyii-code-1) need to remotely connect to some local services (such as Npc, Frpc, Frps, etc.), I needed a monitoring system similar to UptimeKuma. However, UptimeKuma only supports HTTP requests and local Docker hosts. Fortunately, it supports HTTP Push monitoring, so a Push-conversion client similar to UptimeKuma is required to monitor shell commands, systemd services, or other services.

### How it works
The principle is very simple. After the user completes the configuration in Config.json, the client polls services and performs keyword matching based on the configuration file. If specified characters or words are found, the service status (such as Failed or Active) can be determined. Additionally, with the help of Requests, the client may also act as a proxy for UptimeKuma, which is very friendly for NAT environments in mainland China.

### One important clarification
This project is not intended to be used in formal production environments. Before development, I attempted to deploy solutions such as Zabbix, OneUptime (self-hosted/SaaS), etc., but they were too complex and resource-consuming for personal developers. Since I really like UptimeKuma, I decided to leverage its existing ecosystem and modify it by using Push conversion to continuously monitor local services.
However, for production environments, resources and ease of learning are not an issue. Therefore, I do not recommend enterprises or similar organizations use this project for monitoring services. Perhaps Zabbix or other open-source solutions are still better implementations.

### Security considerations
Since this project is installed on the client host and likely needs to run with root privileges, security is extremely important. This project must not evolve into a backdoor or trojan (Trojan/Backdoor). According to the current plan, I will ensure security through HTTPS-only communication, permission checks, code quality and security scanning (CodeQL), and manual reviews. This is also one of the reasons why I chose to open-source this project.

## Development Progress
- [x] Bash command monitoring (keyword-based)
- [x] HTTP request monitoring
- [x] Debug mode
- [x] Threaded loop
- [ ] Systemd service monitoring (coming soon)
- [ ] Comprehensive logging (long-term plan)
- [ ] Improved security checks (long-term work)
- [ ] Cloud configuration (long-term plan)
- [ ] Slim installation runtime
- [ ] Hot update / cloud control / cloud feedback / cloud execution (long-term plan)

## Installation

- 1. Download the corresponding version from the Release Assets
- 2. [Configure the conf.json file](#configuration-file)
- 3. Install Python, Pip, and required modules
- 4. Create a process daemon (systemd or screen)
- 5. `python3 main.py`

### Usage

Currently, two approaches are planned:
Fat installation (default): (`main.py` + `config.json`) and system service (systemd)
Slim installation (to be developed): (pass `--config={json_detail}` to `main.py`)

### Configuration File

[Warning] This project **strongly depends** on a **correct configuration file**. If there are issues with the configuration file, the program may not work properly and may cause **serious consequences**.

Configuration file: `./conf.json`
**All of the following configurations are required, none can be omitted!!!**
Example:

    {
        "meta":{ ←---program settings
            "enabled": true, ←---whether to enable the node (if disabled, the program will exit immediately after startup)
            "cloud_control": false,←---whether to enable cloud control (not implemented)
            "cloud_control_url": "api_point"←---cloud control endpoint
            },
        "region":{←---node information
            "node_name": "Example",←---node name
            "server": "http://127.0.0.1:3001/api/push/" , ←---**UptimeKuma Push API endpoint**, **append `/` after `/api/push`**:`/api/push/`
            "token": ""←---authentication key for accessing the API endpoint (configure according to your endpoint service; empty by default and does not affect usage)
            },
        "monitors":{←---all monitor configurations
            "1":{←---single item name (custom, **must be unique**)
                "name": "shell test(ping)",←---display name
                "enabled": true,←---whether to enable the check; if disabled, a Down status will be submitted
                "type": "bash",←---**type, currently supports only “http” and “bash”**
                "command": "ping 8.8.8.8 -t 1",←---**command to execute**
                "keyword": ["1 packets received"],←---**online keywords to match, type=list**
                "warnword": [],←---**offline keywords to match, type=list**
                "readline": 0,←---number of lines from bottom to top used for keyword checking; 0 means use all (trailing empty lines are automatically removed)
                "ping": false,←---return Ping data (enabled by default, modification not supported yet)
                "datalevel": 0,←---returned log level (not implemented)
                "api": "CsUGkIxISU"←---**important** monitor API, see API key
            },
            "2":{
                "name": "http test",
                "enabled": true,
                "type": "http",
                "url": "https://www.baidu.com",
                "statuscode": [200,301,302],←---**status codes used to determine online status**
                "keyword": ["head"],
                "ping": false,
                "readline": 0,
                "warnword": [],
                "datalevel": 0,
                "api": "kcwjnVGRwx"
            }
        }
    }

#### Evaluation Logic

Bash: return output → split each line by `\n` → filter by `readline` → `keyword` matched? --*yes*→ `warnword` matched --*no*→ status online       otherwise status offline
Http: return content → `statuscode` matched → split returned content by `\n` → filter by `readline` → `keyword` matched? --*yes*→ `warnword` matched --*no*→ status online       otherwise status offline

#### API Key

UptimeKuma - Add Monitor
Type - Passive Monitor - Push
Push URL: (E.G.) http://127.0.0.1:3001/api/push/ib67jWmQ8G?status=up&msg=OK&ping=
-----------------------------------------------^^^^^^^^^^-----------------------
Extract the content between `/push/` and `?status=`

### Warning

For different platforms, Bash check commands are usually not interchangeable. For example, using `ping` to check host availability:

For `Windows (Terminal)`      Recommended command: `ping 127.0.0.1 -n 1` *send 1 ICMP packet to loopback*
For `Linux (Ubuntu)`          Recommended command: `ping 127.0.0.1 -c 1` *send 1 ICMP packet to loopback*
For `MacOS (OS X 26 Tahoe)`   Recommended command: `ping 127.0.0.1 -t 1` *send 1 ICMP packet to loopback*

The program does not check command differences across platforms. Therefore, when migrating platforms, **you must** modify the "command" field; **otherwise**, monitoring may fail due to a 30-second timeout.

## Troubleshooting
`main.py` supports the `--debug` parameter.

### License

Please refer to the LICENSE file.

### Contributing

Currently, the program architecture is not very friendly to Pull Request merges. However, you can still raise questions or submit code via Issues or Pull Requests, and I will manually merge the code.
