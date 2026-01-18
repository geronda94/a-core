import subprocess
import time

class ADBClient:
    def __init__(self, host="localhost", port="5555"):
        self.addr = f"{host}:{port}"

    def run(self, command):
        """Выполняет adb shell команду."""
        cmd = f"adb -s {self.addr} shell {command}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()

    def tap(self, x, y):
        self.run(f"input tap {x} {y}")

    def swipe(self, x1, y1, x2, y2, ms=500):
        self.run(f"input swipe {x1} {y1} {x2} {y2} {ms}")

    def key(self, key_code):
        self.run(f"input keyevent {key_code}")

    def get_xml(self):
        """Выгружает иерархию экрана."""
        self.run("uiautomator dump /sdcard/view.xml")
        # Для ПК нужно вытянуть файл к себе, в Termux можно читать напрямую
        subprocess.run(f"adb -s {self.addr} pull /sdcard/view.xml .", shell=True, capture_output=True)
        with open("view.xml", "r", encoding="utf-8") as f:
            return f.read()