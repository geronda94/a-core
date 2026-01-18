# core/vision.py
import xml.etree.ElementTree as ET
import os
import re

class Vision:
    def __init__(self, adb_client):
        self.adb = adb_client
        self.xml_path = "view.xml"

    def update_view(self):
        """Снимает свежий дамп экрана."""
        self.adb.run("uiautomator dump /sdcard/view.xml")
        # Вытягиваем файл (если на ПК) или копируем в рабочую папку (в Termux)
        os.system(f"adb -s {self.adb.address} pull /sdcard/view.xml {self.xml_path} > /dev/null 2>&1")
        return os.path.exists(self.xml_path)

    def find_element(self, target_text, match_case=False):
        """Ищет элемент и возвращает его координаты центра."""
        if not self.update_view(): return None
        
        try:
            tree = ET.parse(self.xml_path)
            root = tree.getroot()
            
            for node in root.iter():
                text = node.get('text', '') or node.get('content-desc', '')
                if (target_text in text) if not match_case else (target_text == text):
                    bounds = node.get('bounds') # Формат: [x1,y1][x2,y2]
                    coords = re.findall(r'\d+', bounds)
                    if len(coords) == 4:
                        x1, y1, x2, y2 = map(int, coords)
                        return (x1 + x2) // 2, (y1 + y2) // 2
        except:
            pass
        return None