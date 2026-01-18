# ~/a-core/identity.py
import os
import json
import uuid
from datetime import datetime

CONFIG_PATH = "config.json"

def get_config():
    if os.path.exists(CONFIG_PATH) and os.path.getsize(CONFIG_PATH) > 0:
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except:
            pass

    # Первичная настройка
    config = {
        "device_id": f"id_{uuid.uuid4().hex[:6]}",
        "first_init": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model": "Unknown",
        "resolution": "Unknown"
    }
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
    return config

def update_config(key, value):
    config = get_config()
    config[key] = value
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)