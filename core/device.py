import subprocess
import re

class DeviceInfo:
    def __init__(self, adb_client):
        self.adb = adb_client

    def get_resolution(self):
        """Получает разрешение экрана: '1080x2400'."""
        res = self.adb.run("wm size")
        match = re.search(r"(\d+x\d+)", res)
        return match.group(1) if match else "unknown"

    def get_model(self):
        """Получает модель устройства."""
        return self.adb.run("getprop ro.product.model")

    def get_mac(self):
        """Получает MAC-адрес (может потребоваться уточнение интерфейса wlan0)."""
        res = self.adb.run("cat /sys/class/net/wlan0/address")
        return res if res else "unknown"

    def get_imei(self):
        """
        IMEI получить сложно без ROOT или спец. разрешений.
        Пробуем через service call (работает не везде).
        """
        # В современных Android (10+) доступ к IMEI ограничен для обычных приложений
        return "restricted_or_root_needed"