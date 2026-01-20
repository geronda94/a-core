cat << 'EOF' > guardian.sh
#!/bin/bash

# ID уведомления в шторке
ID=777

# Запрещаем системе усыплять Termux
termux-wake-lock

cleanup() {
    termux-notification-remove $ID
    termux-wake-unlock
    exit
}
trap cleanup SIGINT SIGTERM

notify_status() {
    # Обновляем уведомление только при изменении состояния
    termux-notification --title "A-Core Status 🛡️" --content "$1" --id $ID --priority default
}

echo "=== A-CORE GUARDIAN: PASSIVE MODE ==="
notify_status "✅ Связь активна (мониторинг)"

while true; do
    # 1. Проверяем: есть ли хоть ОДНО устройство в статусе 'device'
    # Мы игнорируем 'offline', 'unauthorized' и прочее.
    if adb devices | grep -v "List" | grep -q "device$"; then
        # Если всё ОК — просто ждем минуту
        echo -n "."
        sleep 60
    else
        echo ""
        echo "[!] Связь потеряна. Пытаюсь восстановить..."
        notify_status "⚠️ Восстановление связи..."

        # 2. Ищем порт через nmap (только на localhost)
        PORT=$(nmap localhost -p 30000-49999 | grep "open" | head -n 1 | awk -F'/' '{print $1}')

        if [ ! -z "$PORT" ]; then
            # 3. Подключаемся тихо, без вывода лишнего мусора
            adb connect localhost:$PORT > /dev/null 2>&1
            sleep 5
            
            if adb devices | grep -q "device$"; then
                notify_status "✅ Связь активна (мониторинг)"
            fi
        else
            notify_status "🔍 Ожидание порта (проверь отладку)"
            sleep 10
        fi
    fi
done
EOF
chmod +x guardian.sh




