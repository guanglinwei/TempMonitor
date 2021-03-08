#!/bin/bash

echo "Starting temperature monitor"
alias python=/usr/local/opt/python-3.8.0
cd "/home/pi/Documents/tempmonitor"
export FLASK_ENV=production
echo "n" | python flaskr/run.py
exit
