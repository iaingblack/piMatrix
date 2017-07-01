#!/bin/bash
clear
apt-get update
apt-get upgrade -y
wget -q https://raw.githubusercontent.com/iaingblack/piMatrix/master/client/client-send.py -O client-send.py

echo TO RUN TYPE SOMETHING LIKE THIS
echo 
echo   python client-send.py myserver myport 160 120