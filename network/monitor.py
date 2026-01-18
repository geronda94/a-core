import socket
import requests
import subprocess

def find_adb_port(start_port=30000, end_port=49999):
    """Сканирует порты в поисках активной отладки."""
    print(f"[*] Сканирование портов {start_port}-{end_port}...")
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.01) # Очень быстрый скан
            if s.connect_ex(('127.0.0.1', port)) == 0:
                # Проверяем, реально ли это ADB
                return str(port)
    return None

def get_external_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        return "0.0.0.0"

def get_network_info():
    return {
        "ip": get_external_ip(),
        "adb_port": find_adb_port()
    }