import os
import json
import uuid

CONFIG_PATH = "config.json"

def get_device_id():
    """Возвращает существующий ID или создает новый."""
    if os.path.exists(CONFIG_PATH) and os.path.getsize(CONFIG_PATH) > 0:
        try:
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
                return config.get("device_id")
        except json.JSONDecodeError:
            pass # Если файл битый, перезапишем его

    # Создаем новый конфиг
    new_id = f"phone_{uuid.uuid4().hex[:6]}"
    config = {"device_id": new_id}
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
    return new_id

if __name__ == "__main__":
    print(f"Device ID: {get_device_id()}")