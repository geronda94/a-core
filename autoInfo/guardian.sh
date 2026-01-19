
#!/bin/bash

ID=777
termux-wake-lock

cleanup() {
    termux-notification-remove $ID
    termux-wake-unlock
    exit
}
trap cleanup SIGINT SIGTERM

notify() {
    MSG="$1"
    echo "$(date '+%H:%M:%S') $MSG"
    termux-notification --title "A-Core Guardian 🛡️" --content "$MSG" --id $ID --priority default
}

echo "=== A-CORE GUARDIAN: PASSIVE MODE ==="

while true; do
    # 1. Проверяем наличие ХОТЯ БЫ ОДНОГО живого устройства
    # awk '{print $2}' вытягивает только статус (device, offline и т.д.)
    if adb devices | grep -v "List" | awk '{print $2}' | grep -qx "device"; then
        # Если нашли статус 'device' — уходим в глубокий сон
        echo -n "." 
        sleep 30
    else
        echo ""
        # 2. Только если девайсов НЕТ, ищем порт
        PORT=$(nmap localhost -p 30000-49999 | grep "open" | head -n 1 | awk -F'/' '{print $1}')

        if [ ! -z "$PORT" ]; then
            notify "🔄 Восстановление связи: $PORT"
            # Пробуем подключиться, не разрывая старое (вдруг оно оживет)
            adb connect localhost:$PORT > /dev/null 2>&1
            sleep 5
        else
            notify "🔍 Ожидание порта (проверь отладку)"
            sleep 10
        fi
    fi
done
