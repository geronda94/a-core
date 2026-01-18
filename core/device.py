# ~/a-core/core/device.py
import subprocess
import re

class DeviceHardware:
    def __init__(self, adb_client):
        self.adb = adb_client

    def get_resolution(self):
        res = self.adb.run("wm size")
        match = re.search(r"(\d+x\d+)", res)
        return match.group(1) if match else "unknown"

    def get_model(self):
        return self.adb.run("getprop ro.product.model")

    def get_mac(self):
        # В Termux доступ к интерфейсам может быть ограничен, пробуем так:
        res = self.adb.run("cat /sys/class/net/wlan0/address")
        return res.strip() if res else "unknown"