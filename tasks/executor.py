# tasks/executor.py
import time

class TaskExecutor:
    def __init__(self, adb_client, vision):
        self.adb = adb_client
        self.vision = vision

    def execute(self, task_packet):
        """
        Принимает пакет вида: 
        {"task_id": "123", "actions": [{"type": "click_text", "target": "Sasha"}, ...]}
        """
        actions = task_packet.get("actions", [])
        task_id = task_packet.get("task_id", "unknown")
        
        print(f"[#] Выполнение задачи {task_id} ({len(actions)} действий)")
        
        for action in actions:
            act_type = action.get("type")
            
            try:
                if act_type == "click_text":
                    target = action.get("target")
                    coords = self.vision.find_by_text(target)
                    if coords:
                        self.adb.run(f"input tap {coords[0]} {coords[1]}")
                        print(f"  - Клик по тексту '{target}' {coords}")
                    else:
                        print(f"  - Текст '{target}' не найден")

                elif act_type == "click":
                    x, y = action.get("x"), action.get("y")
                    self.adb.tap(x, y)
                    print(f"  - Клик по координатам {x}, {y}")

                elif act_type == "type":
                    text = action.get("text", "")
                    # ADB не очень любит пробелы напрямую, лучше через %s
                    safe_text = text.replace(" ", "%s")
                    self.adb.run(f"input text {safe_text}")
                    print(f"  - Ввод текста: {text}")

                elif act_type == "wait":
                    sec = action.get("seconds", 1)
                    time.sleep(sec)
                    print(f"  - Ожидание {sec} сек.")

                elif act_type == "key":
                    code = action.get("code")
                    self.adb.run(f"input keyevent {code}")
                    print(f"  - Нажата клавиша {code}")

            except Exception as e:
                print(f"  [!] Ошибка в действии {act_type}: {e}")