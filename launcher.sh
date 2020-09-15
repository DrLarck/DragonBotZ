#!/bin/bash
# Tmux session managment
tmux kill-session -t dragonbotz   # Kill the dragonbotz session
tmux new-session -d -s dragonbotz # Create the sesssion named dragonbotz

# Dragon Bot Z managment
# Execute commands in the tmux session
tmux send-keys -t dragonbotz "cd app/bot/discordballz/discordballz-origins/" C-m # Open the game directory
tmux send-keys -t dragonbotz "echo \"Starting Dragon Bot Z : Origins ...\"" C-m
tmux send-keys -t dragonbotz "pkill -F dragonbotz.pid" C-m  # Kill the process
tmux send-keys -t dragonbotz "python3.6 -B main.py &"  C-m  # Starts the bot
tmux send-keys -t dragonbotz "echo $! > dragonbotz.pid" C-m # Stores the process pid
