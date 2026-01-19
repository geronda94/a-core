import time
from core.vision import Vision
from core.selector import Selector

class TaskExecutor:
    def __init__(self, adb_client):
        self.adb = adb_client
        self.vision = Vision(adb_client)

    def execute_batch(self, batch_data):
        """Выполняет цепочку действий."""
        batch_id = batch_data.get("batch_id", "unknown")
        actions = batch_data.get("actions", [])
        
        print(f"[*] Старт пакета: {batch_id} ({len(actions)} шагов)")
        
        for index, action in enumerate(actions):
            cmd = action.get("command")
            print(f"  -> Шаг {index+1}: {cmd}")
            
            success = False
            
            if cmd == "click":
                success = self._handle_click(action)
            elif cmd == "type":
                success = self._handle_type(action)
            elif cmd == "wait":
                time.sleep(action.get("seconds", 1))
                success = True
            
            # Если действие провалилось - прерываем весь пакет
            if not success:
                print(f"  [!] ОШИБКА на шаге {index+1}. Пакет прерван.")
                # Тут мы будем возвращать отчет об ошибке
                return False
            
            # Если есть блок верификации (проверить, что экран изменился)
            verify_conf = action.get("verification")
            if verify_conf:
                if not self._verify_action(verify_conf):
                    print(f"  [!] Верификация не прошла!")
                    return False

        print(f"[V] Пакет {batch_id} успешно выполнен.")
        return True

    def _handle_click(self, action):
        """Логика поиска элемента и клика"""
        target = action.get("target")
        
        # 1. Получаем актуальный слепок экрана
        xml_root = self.vision.get_screen_data()
        if not xml_root:
            print("    (Ошибка получения XML)")
            return False
            
        # 2. Ищем элемент через Selector
        selector = Selector(xml_root)
        coords = selector.find(target)
        
        if coords:
            print(f"    Нашел элемент! Клик по {coords}")
            self.adb.tap(coords[0], coords[1])
            return True
        else:
            # Если не нашли - пробуем Fallback (запасные координаты)
            fallback = target.get("fallback")
            if fallback:
                print(f"    Элемент не найден, клик наугад: {fallback}")
                self.adb.tap(fallback['x'], fallback['y'])
                return True
            
            print("    Элемент не найден ни по одной стратегии.")
            return False

    def _handle_type(self, action):
        text = action.get("text", "").replace(" ", "%s")
        self.adb.run(f"input text {text}")
        return True

    def _verify_action(self, config):
        """Ждет появления определенного текста/элемента"""
        wait_for = config.get("wait_for") # Например {"type": "text", "value": "Search"}
        timeout = config.get("timeout", 5)
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            xml_root = self.vision.get_screen_data()
            if not xml_root: continue
            
            selector = Selector(xml_root)
            # Оборачиваем условие в формат стратегии для селектора
            check_target = {"strategies": [wait_for]}
            
            if selector.find(check_target):
                return True
            time.sleep(1)
            
        return False