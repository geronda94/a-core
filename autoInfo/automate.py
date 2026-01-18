import subprocess
import requests
import time
import json
import os

SERVER_URL = "http://твой-сервер.com"
DEVICE_ID = "phone_miui_1"

def run_shell(command):
    """Выполняет команду и возвращает результат"""
    try:
        process = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return {
            "exit_code": process.returncode,
            "stdout": process.stdout.strip(),
            "stderr": process.stderr.strip()
        }
    except Exception as e:
        return {"exit_code": -1, "stdout": "", "stderr": str(e)}

def upload_file(path):
    """Специальная команда для отправки файлов на сервер"""
    if not os.path.exists(path):
        return {"status": "error", "msg": "File not found"}
    
    try:
        with open(path, 'rb') as f:
            r = requests.post(f"{SERVER_URL}/upload", files={'file': f}, data={"device_id": DEVICE_ID})
        return {"status": "uploaded", "server_response": r.text}
    except Exception as e:
        return {"status": "error", "msg": str(e)}

def process_batch():
    try:
        # 1. Запрашиваем пакет команд
        resp = requests.get(f"{SERVER_URL}/get_work?device_id={DEVICE_ID}")
        if resp.status_code != 200: return
        
        batch = resp.json()
        batch_id = batch.get("batch_id")
        commands = batch.get("commands", [])
        
        print(f"--- Выполняю пакет {batch_id} ---")
        
        report = {
            "batch_id": batch_id,
            "device_id": DEVICE_ID,
            "results": []
        }

        # 2. Цикл по командам в пакете
        for cmd in commands:
            cmd_id = cmd.get("id")
            action = cmd.get("action")
            
            print(f"Шаг {cmd_id}: {action}")
            
            # Обработка внутренних команд (не ADB)
            if action.startswith("sleep"):
                seconds = int(action.split()[1])
                time.sleep(seconds)
                res = {"exit_code": 0, "stdout": f"Slept {seconds}s"}
            elif action.startswith("upload_file"):
                path = action.split()[1]
                res = upload_file(path)
            else:
                # Обычная ADB или Shell команда
                res = run_shell(action)
            
            report["results"].append({
                "cmd_id": cmd_id,
                "result": res
            })

            # Если команда провалилась, можно прервать весь пакет (опционально)
            if res.get("exit_code", 0) != 0:
                print(f"Ошибка на шаге {cmd_id}, прерываю пакет.")
                break

        # 3. Отправляем полный отчет о пакете
        requests.post(f"{SERVER_URL}/report_batch", json=report)
        print(f"--- Пакет {batch_id} завершен, отчет отправлен ---")

    except Exception as e:
        print(f"Ошибка связи: {e}")

if __name__ == "__main__":
    while True:
        process_batch()
        time.sleep(5) # Пауза перед проверкой нового задания