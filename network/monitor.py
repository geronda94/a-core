# ~/a-core/network/monitor.py
import subprocess
import requests

def get_adb_port():
    try:
        # В Termux мы сами смотрим на проброшенный порт или системный
        port = subprocess.check_output("getprop service.adb.tcp.port", shell=True, text=True).strip()
        return port if port and port != "-1" else "5555"
    except:
        return "5555"

def get_external_ip():
    try:
        # Запрос через мобильный интернет
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        return "0.0.0.0"