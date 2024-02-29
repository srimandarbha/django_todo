#!/bin/bash

# Check if another instance of the process is already running
if pgrep -f "python manage.py runserver" >/dev/null; then
    echo "Another instance of the process is already running."
    exit 0
fi

# Start the process in the background
nohup python manage.py runserver &>/dev/null &

echo "Process started successfully."
