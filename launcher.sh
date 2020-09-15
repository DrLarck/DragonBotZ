#!/bin/bash
# Tmux session managment
tmux kill-session -t dragonbotz   # Kill the dragonbotz session
tmux new-session -d -s dragonbotz # Create the sesssion named dragonbotz

# Dragon Bot Z managment
echo "Starting Dragon Bot Z : Origins ..."
pkill -F dragonbotz.pid  # Kill the process
python3.6 -B main.py &   # Starts the bot
echo $! > dragonbotz.pid # Stores the process pid
