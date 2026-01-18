# network/monitor.py
import subprocess
import requests

def find_adb_port():
    """
    Использует системный nmap для мгновенного поиска порта.
    Точно так же, как это делает autoconnect.sh.
    """
    try:
        # Команда 1-в-1 как в твоем bash скрипте
        cmd = "nmap localhost -p 30000-49999 | grep 'open' | head -n 1 | cut -d'/' -f1"
        result = subprocess.check_output(cmd, shell=True, text=True).strip()
        
        if result and result.isdigit():
            return result
    except Exception as e:
        pass
    return None

def get_external_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        return "0.0.0.0"