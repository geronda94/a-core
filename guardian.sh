#!/usr/bin/env bash

ID=777

# --- НАСТРОЙКИ ---
CHECK_INTERVAL=5
HEARTBEAT_INTERVAL=10
# -----------------

# Функция логирования (пишет и время, и текст)
log() {
    echo -e "\033[1;32m[$(date +%H:%M:%S)]\033[0m $1"
}

error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# 1. ПРОВЕРКА ЗАВИСИМОСТЕЙ ПЕРЕД СТАРТОМ
echo "=== ЗАПУСК ПРОВЕРКИ ==="

if ! command -v termux-wake-lock &> /dev/null; then
    error "Пакет 'termux-api' не установлен!"
    echo "Выполните: pkg install termux-api"
    exit 1
fi

if ! command -v nmap &> /dev/null; then
    error "Пакет 'nmap' не установлен!"
    echo "Выполните: pkg install nmap"
    exit 1
fi

if ! command -v adb &> /dev/null; then
    error "Пакет 'android-tools' не установлен!"
    echo "Выполните: pkg install android-tools"
    exit 1
fi

termux-wake-lock
log "Блокировка сна (Wake Lock) активна."

cleanup() {
    termux-notification-remove $ID
    termux-wake-unlock
    log "Скрипт остановлен."
    exit
}

trap cleanup SIGINT SIGTERM

notify_status() {
    # Пытаемся отправить уведомление, но не падаем, если ошибка
    termux-notification \
        --title "Guard Xiaomi 🛡️" \
        --content "$1" \
        --id $ID \
        --priority default >/dev/null 2>&1 || true
}

log "=== GUARDIAN v3.1: DEBUG MODE ==="
notify_status "🚀 Запуск скрипта"

LAST_HEARTBEAT=$(date +%s)

find_adb_port() {
    log "Сканирование портов (Nmap)..."
    nmap localhost -p 30000-49999 -T4 --min-rate 1000 \
        | awk '/open/ {print $1}' \
        | cut -d'/' -f1 \
        | head -n 1
}

hard_reset() {
    log "⚠️ Выполняю сброс соединения..."
    adb disconnect >/dev/null 2>&1
    sleep 1
}

# --- MAIN LOOP ---
while true; do
    # Получаем список
    DEVICES_OUTPUT=$(adb devices | grep -v "List of devices attached" | grep -v "^$")
    
    # 1. СПИСОК ПУСТ?
    if [ -z "$DEVICES_OUTPUT" ]; then
        log "Устройств нет. Ищу порт..."
        
        PORT=$(find_adb_port)
        
        if [ -n "$PORT" ]; then
            notify_status "🔌 Нашел порт: $PORT"
            log "Подключаюсь к $PORT"
            adb connect localhost:$PORT >/dev/null 2>&1
            sleep 2
        else
            log "Порт не найден. Жду..."
            sleep 3
        fi
        continue
    fi

    # 2. ПРОВЕРКА OFFLINE
    if echo "$DEVICES_OUTPUT" | grep -q "offline"; then
        notify_status "⚠️ Статус OFFLINE"
        hard_reset
        continue
    fi

    # 3. ПРОВЕРКА ЖИВОГО СОЕДИНЕНИЯ
    if echo "$DEVICES_OUTPUT" | grep -q "device"; then
        
        # Heartbeat логика
        CURRENT_TIME=$(date +%s)
        TIME_DIFF=$((CURRENT_TIME - LAST_HEARTBEAT))
        
        if [ $TIME_DIFF -ge $HEARTBEAT_INTERVAL ]; then
            if adb shell true >/dev/null 2>&1; then
                # Успех - ничего не пишем в лог, чтобы не засорять, просто обновляем время
                # Или можно вывести точку, если хочется видеть жизнь
                # echo -n "." 
                LAST_HEARTBEAT=$CURRENT_TIME
            else
                log "❌ Команда не прошла (Завис). Ресет."
                notify_status "💀 Зависший сокет"
                hard_reset
                continue
            fi
        fi
        
        # Если всё ок, просто ждем
        sleep $CHECK_INTERVAL
        continue
    fi

    log "Неизвестный статус: $DEVICES_OUTPUT"
    sleep 2
done