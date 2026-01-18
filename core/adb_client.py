# core/adb_client.py
import subprocess

class ADBClient:
    def __init__(self, host="127.0.0.1", port="5555"):
        self.host = host
        self.port = port
        self.address = f"{host}:{port}"

    def run(self, command):
        """Выполняет команду и возвращает результат."""
        # Добавляем принудительное указание устройства через -s
        full_cmd = f"adb -s {self.address} shell \"{command}\""
        try:
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                return ""
            return result.stdout.strip()
        except:
            return ""

    def is_connected(self):
        res = subprocess.run(f"adb devices", shell=True, capture_output=True, text=True)
        return self.address in res.stdout and "device" in res.stdout