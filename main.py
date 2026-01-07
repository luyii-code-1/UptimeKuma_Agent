import sys
import json
import subprocess
import threading
import argparse
import requests
import  time


"""UptimeKuma Agent main module."""

# UptimeKuma Agent v0.0(Work in Progress)
# This is a program that can use UptimeKuma to monitor shell or systemed etc. targe
# Developer:Luyii
# mail:root@luyii.cn


COLOR_RESET = "\033[0m"
COLOR_DEBUG = "\033[36m"    # Cyan
COLOR_INFO  = "\033[32m"    # Green
COLOR_WARN  = "\033[33m"    # Yellow
COLOR_ERROR = "\033[31;1m"  # Bold Red


def parse_args():   # debug mode
    def parse_args():
        """Parse CLI arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    return parser.parse_args()


def debug_print(msg):
    """Print debug message."""
    if debug:
        print(f"{COLOR_DEBUG}[DEBUG] {msg}{COLOR_RESET}")

def info_print(msg):
    """Print info message."""
    print(f"{COLOR_INFO}[INFO] {msg}{COLOR_RESET}")

def warn_print(msg):
    """Print warn message"""
    print(f"{COLOR_WARN}[WARN] {msg}{COLOR_RESET}")

def error_print(msg):
    """Print error message"""
    print(f"{COLOR_ERROR}[ERROR] {msg}{COLOR_RESET}")

def check_in(keyword, tmp_return):
    """Check if str in list"""
    if keyword is None:
        return True
    if isinstance(keyword, str):
        keyword_list = [keyword]
    else:
        keyword_list = keyword
    if tmp_return is None:
        return False
    if isinstance(tmp_return, str):
        lines = tmp_return.splitlines()
    else:
        lines = tmp_return
    if not keyword_list:
        return True

    keyword_list = [k.lower() for k in keyword_list]

    for line in lines:
        line_lower = str(line).lower()
        for kw in keyword_list:
            if kw in line_lower:
                return True

    return False

def everymonitor_thread(everymonitor, server, token):
    """Every threads program"""
    result = main_check_services(everymonitor)
    if result:
        info_print("Monitor " + everymonitor["name"] + " is UP")
        req_sts = "up"
    else:
        warn_print("Monitor " + everymonitor["name"] + " is DOWN")
        req_sts = "down"
        
    # Build Request to UptimeKuma Server
    #req_msg = ? (WIP)
    #req_ping = ? (WIP)
    api = everymonitor["api"]
    if debug:
        debug_print("API Key: " + api)
    request = server + api + "?status=" + req_sts
    if debug:
        debug_print("Request API URL: " + request)
    try:
        response = requests.get(request, timeout=30)
        trn = response.text
        sta = response.status_code
        if debug:
            debug_print("UptimeKuma Server Response Status Code: " + str(response.status_code))
            debug_print("UptimeKuma Server Response Text: " + str(response.text))
    except requests.RequestException as e:
        error_print("UptimeKuma Server request error: " + str(e))
        sta = None
        trn = None

    if sta == 200 and trn == '{"ok":true}':
        info_print("UptimeKuma Server updated successfully for monitor " + everymonitor["name"])
    else:
        error_print("UptimeKuma Server update failed for monitor " + everymonitor["name"])

    
def start_threads(everymonitor, server, token):
    """Creat Threads"""
    if debug:
        debug_print("===== Now Running start_threads() =====")

    if debug:
        debug_print("Config type: " + str(type(everymonitor)))  # Print Type
        debug_print("Config: " + str(everymonitor))             # Print Value
        for tmp_counter_1 in everymonitor:
            debug_print(tmp_counter_1 + " : " + str(everymonitor[tmp_counter_1]))
    #This will be Threading part in future
    everymonitor_thread(everymonitor, server, token)

def main_check_services(conf_monitor):
    """Check Target"""
    if debug:
        debug_print("===== Now Running main_check_services() =====")

    if conf_monitor["enabled"]:
        monitor_type = conf_monitor["type"]  # Support 2 types now: bash, http
        if monitor_type == "bash":
            status_is_up = bash_check(conf_monitor)
        elif monitor_type == "http":
            status_is_up = http_check(conf_monitor)
        else:
            debug_print("WIP: Unsupported monitor type: " + monitor_type)
    else:
        status_is_up = False#May use another types
        if  debug:
            debug_print("Monitor is disabled")


    result = status_is_up#Temply only status_is_up for now[Work in Process]
    return status_is_up


def http_check(conf_monitor):
    """Check Http Target"""
    if debug:
        debug_print("===== Now Running http_check() =====")

    name = conf_monitor["name"]
    url = conf_monitor["url"]
    statuscode = conf_monitor["statuscode"]
    keyword = conf_monitor["keyword"]
    warnword = conf_monitor["warnword"]
    datalevel = conf_monitor["datalevel"]
    readline = conf_monitor["readline"]

    if debug:
        debug_print("HTTP Check - Name: " + name)
        debug_print("HTTP Check - URL: " + url)
        debug_print("HTTP Check - Statuscode: " + str(statuscode))
        debug_print("HTTP Check - Keyword: " + str(keyword))
        debug_print("HTTP Check - Warnword: " + str(warnword))  # [Work in Process](DISABLED)
        debug_print("HTTP Check - Datalevel: " + str(datalevel))
        debug_print("HTTP Check - Readline: " + str(readline))
        

    try:
        response = requests.get(url, timeout=30)
        tmp_is_return = True
        tmp_return = response.text
        tmp_status_code = response.status_code
        if debug:
            debug_print("HTTP Check - Response Status Code: " + str(tmp_status_code))

    except requests.RequestException as e:
        tmp_is_return = False
        tmp_return = ""
        tmp_status_code = None
        error_print("HTTP request error: " + str(e))

    tmp_process_output_list = tmp_return.split("\n")

    if debug:
        debug_print("HTTP Check - Raw Output: " + str(tmp_process_output_list))

    if tmp_is_return and readline != 0: #  Readline
        readline += 1 if tmp_process_output_list[-1] == "" else 0
        tmp_return = tmp_process_output_list[int(-readline)]
        if debug:
            debug_print("Bash Check - Final Output: " + str(tmp_return))
    
    status_is_up = False
    if tmp_is_return:   # Request executed successfully

        # Check status code
        if tmp_status_code in statuscode:
            if debug:
                debug_print("HTTP Check - Status Code Matched")
            status_is_up = False
            if  check_in(keyword, tmp_return):
                status_is_up = True
                if debug:
                    debug_print("HTTP Check - Keyword Matched")
            else:
                status_is_up = False
                if debug:
                    debug_print("HTTP Check - Keyword Not Matched")
            if check_in(warnword, tmp_return) and warnword != []:
                status_is_up = False
                if debug:
                    debug_print("HTTP Check - Warnword Matched")
        else:
            if debug:
                warn_print("HTTP Check - Status Code Not Matched")
            status_is_up = False
    else:
        if debug:
            warn_print("HTTP Check - Request Failed")
        status_is_up = False

    return status_is_up#Temply use only

def bash_check(conf_monitor):
    """Check Bash Target"""
    if debug:
        debug_print("===== Now Running bash_check() =====")

    name = conf_monitor["name"]
    command = conf_monitor["command"]
    keyword = conf_monitor["keyword"]
    warnword = conf_monitor["warnword"]
    datalevel = conf_monitor["datalevel"]
    readline = conf_monitor["readline"]

    if debug:
        debug_print("Bash Check - Name: " + name)
        debug_print("Bash Check - Command: " + command)
        debug_print("Bash Check - Keyword: " + str(keyword))
        debug_print("Bash Check - Warnword: " + str(warnword))  # [Work in Process](DISABLED)
        debug_print("Bash Check - Datalevel: " + str(datalevel))
        debug_print("Bash Check - Readline: " + str(readline))

    try:    # run bash command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            check=True,
            text=True,
            timeout=30
        )
        tmp_is_return = True
        tmp_return = str(result.stdout)
    except subprocess.CalledProcessError as e:
        tmp_is_return = False
        tmp_return = ""
        error_print("Bash command error: " + str(e))

    tmp_process_output_list = tmp_return.split("\n")

    debug_print("Bash Check - Raw Output: " + str(tmp_process_output_list))

    if tmp_is_return and readline != 0: #  Readline
        readline += 1 if tmp_process_output_list[-1] == "" else 0
        tmp_return = tmp_process_output_list[int(-readline)]
        if debug:
            debug_print("Bash Check - Final Output: " + str(tmp_return))

    status_is_up = False
    if tmp_is_return:   # Command executed successfully
        if  check_in(keyword, tmp_return):
            status_is_up = True
            if debug:
                debug_print("Bash Check - Keyword Matched")
        else:
            status_is_up = False
            if debug:
                debug_print("Bash Check - Keyword Not Matched")
        if check_in(warnword, tmp_return) and warnword != []:
            status_is_up = False
            if debug:
                debug_print("Bash Check - Warnword Matched")
    else:
        if debug:
            warn_print("Bash Check - Command Failed")
        status_is_up = False    
    return status_is_up#Temply use only


def __init__():
    """Main"""
    if debug:
        debug_print("===== Now Running __init__() =====")

    # Load Raw Config
    raw_conf = json.load(open("./conf.json", "r", encoding="utf-8"))

    # Grop By Keys
    raw_meta = raw_conf["meta"]
    raw_region = raw_conf["region"]
    raw_monitors = raw_conf["monitors"]

    # Process Meta
    enabled = raw_meta["enabled"]
    if not enabled:
        sys.stop ()
    #cloud_control = raw_meta["cloud_control"]
    #cloud_control_url = raw_meta["cloud_control_url"]


    # Process Region
    hosts_name = raw_region["hostname"]
    node_name = raw_region["node_name"]
    server = raw_region["server"]
    token = raw_region["token"]

    print(
        f"UptimeKuma_Agent\n",
        f"Node Name: {node_name}\n",
        f"Hostname: {hosts_name}\n",
        f"Server: {server}\n",
        f"Token: {token}\n",
    )

    # Process Monitors
    for everymonitor in raw_monitors:
        start_threads(raw_monitors[everymonitor], server ,token)



args = parse_args()
debug = args.debug

if debug:
    print(f"{COLOR_DEBUG}[DEBUG] Debug mode enabled{COLOR_RESET}")


if __name__ == "__main__":
    __init__()
