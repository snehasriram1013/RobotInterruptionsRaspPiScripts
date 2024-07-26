#!/bin/bash

# Activate the virtual environment
source /home/snehasriram6/myenv/bin/activate

# Run the motor-control.py script
python /home/snehasriram6/motor-control.py &

# Wait for a few seconds to ensure the script starts properly
sleep 5

# Set the display environment variable
export DISPLAY=:0

# Disable screensaver and power management
xset s off
xset s noblank

# Launch Chromium in kiosk mode with your desired URL
chromium-browser --noerrdialogs --disable-infobars --kiosk https://robotdashboard.medien.ifi.lmu.de &
