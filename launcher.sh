#!/bin/bash
echo "Starting Dragon Bot Z : Origins ..."
pkill -F dragonbotz.pid
python3.6 -B main.py &
echo $! > dragonbotz.pid