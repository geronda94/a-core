# core/device.py
import re

class DeviceHardware:
    def __init__(self, adb_client):
        self.adb = adb_client

    def get_resolution(self):
        res = self.adb.run("wm size")
        # Ищем паттерн типа 1080x2400
        match = re.search(r'(\d+x\d+)', res)
        return match.group(1) if match else "unknown"

    def get_model(self):
        # Пробуем несколько системных свойств
        model = self.adb.run("getprop ro.product.model")
        if not model:
            model = self.adb.run("getprop ro.product.brand") + " " + self.adb.run("getprop ro.product.device")
        return model if model.strip() else "Android Device"