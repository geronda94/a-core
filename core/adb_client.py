import subprocess
import time
from network.monitor import find_adb_port

class ADBClient:
    def __init__(self):
        self.port = None
        self.address = None

    def ensure_connection(self):
        """Проверяет и восстанавливает соединение."""
        res = subprocess.run("adb devices", shell=True, capture_output=True, text=True).stdout
        
        # Если устройства нет или оно offline
        if "device" not in res or "offline" in res:
            print("[!] Связь потеряна. Ищу порт...")
            self.port = find_adb_port()
            if self.port:
                self.address = f"127.0.0.1:{self.port}"
                subprocess.run(f"adb disconnect", shell=True)
                subprocess.run(f"adb connect {self.address}", shell=True)
                time.sleep(2)
                return True
            return False
        return True

    def run(self, command):
        if not self.ensure_connection():
            return ""
        
        # Автоматически находим адрес устройства из списка
        cmd = f"adb shell \"{command}\""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()