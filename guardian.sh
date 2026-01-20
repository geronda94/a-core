#!/bin/bash

ID=777
termux-wake-lock

cleanup() {
    termux-notification-remove $ID
    termux-wake-unlock
    exit
}
trap cleanup SIGINT SIGTERM

notify_status() {
    termux-notification --title "A-Core Status 🛡️" --content "$1" --id $ID --priority default
}

echo "=== GUARDIAN: OLD SCHOOL PROTOTYPE ==="

# Очистка ТОЛЬКО ОДИН РАЗ при ручном старте
adb disconnect > /dev/null 2>&1

while true; do
    # 1. Если есть ХОТЬ ОДИН живой device — мы счастливы и спим.
    # Нам плевать, сколько там висит offline-строк, главное есть active.
    if adb devices | grep -v "List" | grep -q "device$"; then
        echo -n "."
        sleep 10
    else
        echo ""
        echo "[!] Нет активного подключения. Ищу порт..."
        
        # 2. Мы НЕ делаем disconnect. Мы просто ищем новый порт.
        PORT=$(nmap localhost -p 30000-49999 | grep "open" | head -n 1 | awk -F'/' '{print $1}')

        if [ ! -z "$PORT" ]; then
            notify_status "➕ Добавляю порт: $PORT"
            
            # Просто кидаем коннект поверх всего.
            adb connect localhost:$PORT > /dev/null 2>&1
            sleep 5
            
            # Проверка
            if adb devices | grep -q "device$"; then
                notify_status "✅ Связь есть"
            fi
        else
            notify_status "🔍 Порт не найден"
            sleep 10
        fi
    fi
done
