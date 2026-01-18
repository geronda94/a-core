import os
import json
import uuid
from datetime import datetime

CONFIG_PATH = "config.json"

def get_config():
    """Загружает или создает расширенный конфиг устройства."""
    if os.path.exists(CONFIG_PATH) and os.path.getsize(CONFIG_PATH) > 0:
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass

    # Если файла нет или он битый — первичная инициализация
    new_config = {
        "device_id": f"phone_{uuid.uuid4().hex[:6]}",
        "first_init": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model": "Unknown",
        "resolution": "Unknown"
    }
    
    with open(CONFIG_PATH, 'w') as f:
        json.dump(new_config, f, indent=4)
    return new_config

def update_config(key, value):
    """Метод для дополнения конфига (например, когда узнали разрешение)."""
    config = get_config()
    config[key] = value
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
        
        
        
if __name__ == "__main__":
    cfg = get_config()
    print("Current Config:", cfg)