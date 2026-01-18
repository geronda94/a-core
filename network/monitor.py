import socket
import requests

def is_port_open(port):
    """Молниеносная проверка одного порта."""
    if not port: return False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.1)
        return s.connect_ex(('127.0.0.1', int(port))) == 0

def find_adb_port(start_port=30000, end_port=49999):
    """Тяжелый сканер (запускается только при необходимости)."""
    print(f"[*] ВНИМАНИЕ: Запуск полного сканирования портов...")
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.02) # Ускоряем сканирование
            if s.connect_ex(('127.0.0.1', port)) == 0:
                return str(port)
    return None