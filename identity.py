# identity.py
import os
import json
import uuid
from datetime import datetime

CONFIG_PATH = "config.json"

def get_config():
    """Загружает конфиг или создает дефолтный при первом запуске."""
    if os.path.exists(CONFIG_PATH) and os.path.getsize(CONFIG_PATH) > 0:
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except: 
            pass
    
    # Дефолтные значения для нового устройства
    config = {
        "device_id": f"id_{uuid.uuid4().hex[:6]}",
        "first_init": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model": "Unknown",
        "resolution": "unknown",
        "last_ip": "0.0.0.0",
        "last_port": "5555"
    }
    save_config(config)
    return config

def save_config(config):
    """Сохраняет объект конфига в файл."""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

def update_config(key, value):
    """Обновляет конкретный статический параметр (модель, разрешение)."""
    config = get_config()
    config[key] = value
    save_config(config)

def update_runtime_info(ip=None, port=None):
    """Обновляет динамические параметры (IP, Порт) без затирания остальных."""
    config = get_config()
    if ip: config["last_ip"] = ip
    if port: config["last_port"] = port
    save_config(config)