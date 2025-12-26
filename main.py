import os
import json
import requests
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

def start_threads(everymonitor):
    print(everymonitor)
    main_check_services()

def main_check_services():
    return True

def init_loadconf():
    #Load Raw Config
    raw_conf = json.load(open("conf.json", "r", encoding="utf-8"))
    
    #Grop By Keys
    raw_meta = raw_conf["meta"]
    raw_region = raw_conf["region"]
    raw_monitors = raw_conf["monitors"]
    
    #Process Meta
    version = raw_meta["enable"]
    node_name = raw_meta["node_name"]
    cache_path = raw_meta["cache"]
    enabled = raw_meta["enabled"]

    #Process Region
    hosts_name = raw_region["hostname"]
    node_name = raw_region["node_name"]
    server = raw_region["server"]
    token = raw_region["token"]

    #Process Monitors
    for everymonitor in raw_monitors():
        start_threads(everymonitor)
