#!/bin/bash

# ==============================
# Linux Navigation & Filesystem
# ==============================

pwd
ls
ls -la

cd /
cd ..
cd .

ls /etc
ls /var/log


# ==============================
# File Searching & Inspection
# ==============================

find /home -type f
find /home -type d
find /home -name "*.py"

stat file.txt

grep "failed" login.log

tail login.log
tail -f login.log


# ==============================
# File Permissions & Ownership
# ==============================

chmod u+x script.py
chmod u-x script.py
chmod g+x script.py
chmod a+x script.py

chmod 755 script.py
chmod 600 secret.txt

chown esther file.txt


# ==============================
# Processes
# ==============================

ps aux
ps aux --sort=-%cpu | head

ps -p 3122 -f

kill 3122


# ==============================
# Networking
# ==============================

ping google.com
ping 8.8.8.8

traceroute google.com

ip addr


# ==============================
# Network Sockets
# ==============================

ss -ltnp

ss -ltnp | grep 9999


# ==============================
# Output & Redirection
# ==============================

echo "Hello Linux"

echo "First line" > test.txt
echo "Second line" >> test.txt