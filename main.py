import os
import json
import requests
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

def _init_loadconf():
    #Load Raw Config
    raw_conf = json.load(open("conf.json", "r", encoding="utf-8"))
    
    #Grop By Keys
    raw_meta = raw_conf["meta"]
    raw_region = raw_conf["region"]
    raw_monitors = raw_conf["monitors"]
    
    #Process Meta
    version = raw_meta["enable"]
    run_mode = raw_meta["install"]
    cache_path = raw_meta["cache"]
    monitor_num = raw_meta["monitor_num"]

    #Process Region
    node_name = raw_region["name"]
    server = raw_region["server"]
    security_mode = raw_region["security"]
    server_token = raw_region["token"]

    #Process Monitors
    for i in range(monitor_num):
        return


