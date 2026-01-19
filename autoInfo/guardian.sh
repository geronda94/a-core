cat << 'EOF' > guardian.sh
#!/bin/bash

echo "=== A-CORE GUARDIAN: AGGRESSIVE v3 ==="

# Функция перезапуска ADB при проблемах
restart_adb() {
    echo "[☠️] Перезапуск ADB сервера..."
    adb disconnect > /dev/null 2>&1
    adb kill-server
    sleep 2
    adb start-server
    sleep 2
}

while true; do
    # 1. Проверяем, есть ли ЖИВОЕ устройство
    if adb devices | grep -q "device$"; then
        echo -n "."
        sleep 5
    else
        echo ""
        echo "[!] Связь потеряна."
        
        # 2. Сканируем порт (берем только первый)
        PORT=$(nmap 127.0.0.1 -p 30000-49999 | grep "open" | head -n 1 | awk -F'/' '{print $1}')

        if [ -z "$PORT" ]; then
            echo "[?] Портов нет. ADB спит?"
            # Если портов нет долгое время, можно попробовать пнуть сервер
            sleep 3
        else
            echo "[*] Пробую порт: $PORT"
            
            # 3. Пытаемся подключиться и сохраняем вывод
            OUTPUT=$(adb connect 127.0.0.1:$PORT 2>&1)
            echo "   > $OUTPUT"

            # 4. Анализируем ответ
            if [[ "$OUTPUT" == *"failed"* ]] || [[ "$OUTPUT" == *"refused"* ]]; then
                echo "[!] Ошибка подключения. Сброс сервера..."
                restart_adb
            else
                # Вроде подключились, проверяем статус
                sleep 2
                if adb devices | grep -q "offline"; then
                    echo "[X] Устройство OFFLINE. Жесткий сброс..."
                    restart_adb
                else
                    echo "[V] Успех!"
                fi
            fi
        fi
    fi
done
EOF
chmod +x guardian.sh