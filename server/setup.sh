#!/bin/bash
clear
# Ascii Server Receiver
apt-get update
apt-get upgrade -y
 
# Python pillow ibrary
sudo apt-get install python-pillow -y
wget -q https://raw.githubusercontent.com/iaingblack/piMatrix/master/server/server-receive.py -O server-receive.py

# HTTP Server
apt-get install apache2 -y
wget -q https://raw.githubusercontent.com/iaingblack/piMatrix/master/web/AsciiStylesheet.css -O /var/www/html/AsciiStylesheet.css
wget -q https://raw.githubusercontent.com/iaingblack/piMatrix/master/web/index.html -O /var/www/html/index.html

echo TO START RUN LIKE THIS. PORT IS LAST ARGUMENT
echo 
echo   python server-receive.py 8000