# core/vision.py
import xml.etree.ElementTree as ET
import os
import re

class Vision:
    def __init__(self, adb_client):
        self.adb = adb_client
        self.xml_dump_path = "/sdcard/view.xml"
        self.local_xml = "view.xml"

    def get_screen_data(self):
        """Делает свежий дамп экрана и подгружает его."""
        self.adb.run(f"uiautomator dump {self.xml_dump_path}")
        # Копируем файл из памяти Android в папку скрипта
        os.system(f"adb pull {self.xml_dump_path} {self.local_xml} > /dev/null 2>&1")
        if not os.path.exists(self.local_xml):
            return None
        return ET.parse(self.local_xml).getroot()

    def find_by_text(self, target_text):
        """Ищет элемент по тексту и возвращает центр (x, y)."""
        root = self.get_screen_data()
        if root is None: return None

        for node in root.iter():
            text = node.get('text', '') or node.get('content-desc', '')
            if target_text.lower() in text.lower():
                bounds = node.get('bounds') # Формат: [x1,y1][x2,y2]
                coords = list(map(int, re.findall(r'\d+', bounds)))
                if len(coords) == 4:
                    x_center = (coords[0] + coords[2]) // 2
                    y_center = (coords[1] + coords[3]) // 2
                    return x_center, y_center
        return None