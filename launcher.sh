#!/bin/bash
# Tmux session managment
tmux kill-session -t dragonbotz   # Kill the dragonbotz session
tmux new-session -d -s dragonbotz # Create the sesssion named dragonbotz

# Dragon Bot Z managment
# Execute commands in the tmux session
tmux send-keys -t dragonbotz "echo \"Starting Dragon Bot Z : Origins ...\""
tmux send-keys -t dragonbotz "pkill -F dragonbotz.pid"  # Kill the process
tmux send-keys -t dragonbotz "python3.6 -B main.py &"   # Starts the bot
tmux send-keys -t dragonbotz "echo $! > dragonbotz.pid" # Stores the process pid
