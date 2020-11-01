#!/bin/bash

# Manage the tmux sessions
tmux kill-session -t dragonbotz
tmux new-session -d -s dragonbotz

# Kill old instances
pkill -f dragonbotz.py

# Start the game into the tmux session
tmux send-keys -t dragonbotz "cd /home/app/bot/dragonbotz/discordballz-origins/" C-m
tmux send-keys -t dragonbotz "python3 -B dragonbotz.py" C-m
