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
    termux-notification \
        --title "A-Core Status 🛡️" \
        --content "$1" \
        --id $ID \
        --priority default
}

echo "=== GUARDIAN: ACTUALLY STABLE ==="

adb disconnect >/dev/null 2>&1

# ----------------------------------
# Проверка живого ADB (БЕЗ subshell)
# ----------------------------------
has_alive_device() {
    for dev in $(adb devices | awk '/device$/ {print $1}'); do
        if adb -s "$dev" shell true >/dev/null 2>&1; then
            return 0
        fi
    done
    return 1
}

# ----------------------------------
# Удаление offline
# ----------------------------------
cleanup_dead_devices() {
    for dev in $(adb devices | awk '/offline/ {print $1}'); do
        adb disconnect "$dev" >/dev/null 2>&1
    done
}

# ----------------------------------
# Поиск порта (только когда реально надо)
# ----------------------------------
find_adb_port() {
    nmap localhost -p 30000-49999 \
        | awk '/open/ {print $1}' \
        | cut -d'/' -f1 \
        | head -n 1
}

# ----------------------------------
# MAIN LOOP
# ----------------------------------
while true; do

    cleanup_dead_devices

    if has_alive_device; then
        echo -n "."
        sleep 10
        continue
    fi

    echo ""
    echo "[!] ADB не отвечает. Восстанавливаю..."

    PORT=$(find_adb_port)

    if [ -z "$PORT" ]; then
        notify_status "🔍 ADB порт не найден"
        sleep 10
        continue
    fi

    notify_status "🔌 Подключаюсь к localhost:$PORT"
    adb connect localhost:$PORT >/dev/null 2>&1
    sleep 3

    if has_alive_device; then
        notify_status "✅ Связь восстановлена"
    else
        notify_status "❌ Порт есть, ADB не отвечает"
    fi

    sleep 5
done
