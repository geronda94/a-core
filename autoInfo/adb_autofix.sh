cat << 'EOF' > ~/adb_autofix.sh
#!/bin/bash
# Проверяем, видит ли ADB хоть одно устройство
if ! adb devices | grep -q "device$"; then
    echo "ADB отвалился. Ищу новый порт..."
    # Пытаемся вытащить порт из системы
    PORT=$(getprop service.adb.tcp.port)
    # Если системный метод не сработал, сканируем диапазон портов через nmap
    if [ -z "$PORT" ] || [ "$PORT" == "-1" ]; then
        PORT=$(nmap localhost -p 30000-49999 | grep "open" | head -n 1 | cut -d'/' -f1)
    fi
    
    if [ ! -z "$PORT" ]; then
        adb connect localhost:$PORT
    fi
fi
EOF
chmod +x ~/adb_autofix.sh