cat << 'EOF' > ~/.termux/boot/on_boot.sh
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
sshd
crond
~/guardian.sh
EOF
chmod +x ~/.termux/boot/on_boot.sh