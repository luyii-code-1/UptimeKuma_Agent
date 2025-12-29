import os
import json
import requests
import subprocess
import time
import threading
import argparse

# UptimeKuma Agent v0.0(Work in Progress)
# This is a program that can use UptimeKuma to monitor shell or systemed etc. target
# Developer:Luyii 
# mail:root@luyii.cn

# Warning! This code is developed in MacOS environment, may not fully compatible with Windows or Linux system.
# For example ,ping usage as "ping 8.8.8.8 -t 4" but "ping 8.8.8.8" in Windows.

# Lasts update: 2025-12-28 00:28 on Macbook Air M1(202512280028v1)
### To do List:
# 1.Complete the http check function
# 2.Conplete the final status report function
# 3.Develop the requests models
# 4.Develop the Threading models
### Now
# Bash check is ok and work healthyly

COLOR_RESET = "\033[0m"
COLOR_DEBUG = "\033[36m"    # Cyan
COLOR_INFO  = "\033[32m"    # Green
COLOR_WARN  = "\033[33m"    # Yellow
COLOR_ERROR = "\033[31;1m"  # Bold Red


def parse_args():   # debug mode
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    return parser.parse_args()


# =========================
# Logger Functions
# =========================
def debug_print(msg):
    if debug:
        print(f"{COLOR_DEBUG}[DEBUG] {msg}{COLOR_RESET}")

def info_print(msg):
    print(f"{COLOR_INFO}[INFO] {msg}{COLOR_RESET}")

def warn_print(msg):
    print(f"{COLOR_WARN}[WARN] {msg}{COLOR_RESET}")

def error_print(msg):
    print(f"{COLOR_ERROR}[ERROR] {msg}{COLOR_RESET}")


def start_threads(everymonitor):

    if debug:
        debug_print("===== Now Running start_threads() =====")

    if debug:
        debug_print("Config type: " + str(type(everymonitor)))  # Print Type
        debug_print("Config: " + str(everymonitor))             # Print Value
        for tmp_counter_1 in everymonitor:
            debug_print(tmp_counter_1 + " : " + str(everymonitor[tmp_counter_1]))

    main_check_services(everymonitor)


def main_check_services(conf_monitor):

    if debug:
        debug_print("===== Now Running main_check_services() =====")

    type = conf_monitor["type"]  # Support 2 types now: bash, http
    if type == "bash":
        is_up = bash_check(conf_monitor)
    elif type == "http":
        is_up = http_check(conf_monitor)
    else:
        debug_print("WIP: Unsupported monitor type: " + type)
###################Last Work Here####################

def http_check(conf_monitor):
    if debug:
        debug_print("===== Now Running http_check() =====")
    
    name = conf_monitor["name"]
    url = conf_monitor["url"]
    statuscode = conf_monitor["statuscode"]
    keyword = conf_monitor["keyword"]
    warnword = conf_monitor["warnword"]
    datalevel = conf_monitor["datalevel"]

    if debug:
        debug_print("HTTP Check - Name: " + name)
        debug_print("HTTP Check - URL: " + url)
        debug_print("HTTP Check - Statuscode: " + str(statuscode))
        debug_print("HTTP Check - Keyword: " + str(keyword))
        debug_print("HTTP Check - Warnword: " + str(warnword))  # [Work in Process](DISABLED)
        debug_print("HTTP Check - Datalevel: " + str(datalevel))

    try:
        response = requests.get(url, timeout=30)
        tmp_is_return = True
        tmp_return = response.text
        tmp_status_code = response.status_code
        if debug:
            debug_print("HTTP Check - Response Status Code: " + str(tmp_status_code))
            debug_print("HTTP Check - Response Body: " + str(tmp_return))

    except requests.RequestException as e:
        tmp_is_return = False
        tmp_return = ""
        tmp_status_code = None
        error_print("HTTP request error: " + str(e))# There is an Bug that havn't fix yet：[ERROR] HTTP request error: HTTPSConnectionPool(host='www.baidu.com', port=443): Max retries exceeded with url: / (Caused by ProxyError('Unable to connect to proxy', FileNotFoundError(2, 'No such file or directory')))
    
    tmp_process_output_list = tmp_return.split("\n")    #Use \n to split lines,May Change later(Very long time!)
    debug_print("HTTP Check - Raw Output: " + str(tmp_process_output_list))
#########Last Work Here#########

def bash_check(conf_monitor):

    if debug:
        debug_print("===== Now Running bash_check() =====")

    name = conf_monitor["name"]
    command = conf_monitor["command"]
    keyword = conf_monitor["keyword"]
    warnword = conf_monitor["warnword"]
    datalevel = conf_monitor["datalevel"]

    if debug:
        debug_print("Bash Check - Name: " + name)
        debug_print("Bash Check - Command: " + command)
        debug_print("Bash Check - Keyword: " + str(keyword))
        debug_print("Bash Check - Warnword: " + str(warnword))  # [Work in Process](DISABLED)
        debug_print("Bash Check - Datalevel: " + str(datalevel))

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

    tmp_process_output_list = tmp_return.split("\n")    #Use \n to split lines,May Change later(Very long time!)
    debug_print("Bash Check - Raw Output: " + str(tmp_process_output_list))

    if tmp_is_return and False:   # read last any line [Work in Process](DISABLED)
        if debug:
            debug_print("Bash Check - Output: " + str(tmp_process_output_list))

        final_check_list = []
        try:
            for line in range(len(tmp_process_output_list)):
                final_check_list.append(
                    tmp_process_output_list[len(tmp_process_output_list) - line]
                )
        except Exception as e:
            if debug:
                debug_print("Bash Check - Readline Error: " + str(e))

        if debug:
            debug_print("Bash Check - Final Output: " + str(final_check_list))


    if tmp_is_return:   # Command executed successfully
        #Check if keywword is in output,can't use 'if xx in xx' because keyword not actually is list
        keyword_matched = False
        matched_kw = None
        matched_line = None

        for line in tmp_process_output_list:
            for kw in keyword:
                if kw in line:
                    keyword_matched = True
                    matched_kw = kw
                    matched_line = line
                    break
            if keyword_matched:
                break

        if keyword_matched:
            if debug:
                debug_print(f"Bash Check - Keyword matched: {matched_kw}")
                debug_print(f"Bash Check - Matched line: {matched_line}")
                debug_print("Bash Check - Monitor " + name + " is UP")

            info_print("Monitor " + name + " is UP")
            status_is_up = True

            if datalevel == 0:
                return_msg = matched_line

        else:
            if debug:
                debug_print("Bash Check - Monitor " + name + " is DOWN")
            warn_print("Monitor " + name + " is DOWN")
            status_is_up = False

    else:
        if debug:
            debug_print("Bash Check - Monitor " + name + " Command Error")
        error_print("Monitor " + name + " Command Error")
        status_is_up = False

    return status_is_up


def init_loadconf():

    if debug:
        debug_print("===== Now Running init_conf() =====")

    # Load Raw Config
    raw_conf = json.load(open("./conf.json", "r", encoding="utf-8"))

    # Grop By Keys
    raw_meta = raw_conf["meta"]
    raw_region = raw_conf["region"]
    raw_monitors = raw_conf["monitors"]

    # Process Meta
    version = raw_meta["version"]
    node_name = raw_meta["node_name"]
    cache_path = raw_meta["cache_path"]
    enabled = raw_meta["enabled"]
    
    try:
        platform = raw_meta.get("platform", "Unknown")
    except Exception as e:
        platform = "Unknown"
        debug_print("Error when getting platform field: " + str(e))
    
    if platform == "Unknown":
        warn_print("Platform not specified in config, defaulting to 'Unknown', this Program can't run as an Unknow Platform!")
        warn_print("Please configure the 'platform' field in conf.json to 'Windows', 'Linux' or 'MacOS' accordingly.")
        warn_print("This Program don't check the command but just warn you.")
        os.stop()

    # Process Region
    hosts_name = raw_region["hostname"]
    node_name = raw_region["node_name"]
    server = raw_region["server"]
    token = raw_region["token"]

    # Process Monitors
    for everymonitor in raw_monitors:
        start_threads(raw_monitors[everymonitor])


# =========================
# Entry
# =========================
args = parse_args()
debug = args.debug

if debug:
    print(f"{COLOR_DEBUG}[DEBUG] Debug mode enabled{COLOR_RESET}")

init_loadconf()
