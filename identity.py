# identity.py
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
        except: pass
    
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
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

def update_runtime_info(ip=None, port=None):
    """Обновляет только динамические данные в фоне."""
    config = get_config()
    if ip: config["last_ip"] = ip
    if port: config["last_port"] = port
    save_config(config)