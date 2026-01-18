cat << 'EOF' > ~/guardian.sh
#!/bin/bash
# 1. Убеждаемся, что процессор не спит
termux-wake-lock

# 2. Чиним ADB если надо
~/adb_autofix.sh

# 3. Проверяем, запущен ли основной воркер
if ! pgrep -f "python ~/worker.py" > /dev/null; then
    nohup python ~/worker.py > ~/worker.log 2>&1 &
fi
EOF
chmod +x ~/guardian.sh