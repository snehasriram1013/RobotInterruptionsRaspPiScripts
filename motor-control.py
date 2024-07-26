import time
import RPi.GPIO as GPIO
import socketio

# Initialize Socket.IO client
sio = socketio.Client()

# Define your server URL
SERVER_URL = 'https://robotdashboard.medien.ifi.lmu.de'

#room ip
room_ip = '10.163.181.43'

# GPIO pins connected to the ULN2003 driver board IN1, IN2, IN3, IN4
control_pins = [23, 24, 25, 8]

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM) 
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Define the half-step sequence for the 28BYJ-48 stepper motor
halfstep_seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

reverse_halfstep_seq = list(reversed(halfstep_seq))
# Function to perform a single half-step movement
def step_motor(sequence, delay, steps):
    seq_len = len(sequence)
    for i in range(steps):
       for step in range(seq_len):
            for pin in range(4):
                GPIO.output(control_pins[pin], sequence[step][pin])
            time.sleep(delay)


# Handle connection event
@sio.event
def connect():
    print('Connected to server')

# Handle disconnection event
@sio.event
def disconnect():
    print('Disconnected from server')

# Handle "move" event
@sio.event
def modality(data):
    print('modality recieved')
    if ('move' in data):
        print('Move command received with data:')
        steps = 512  # Default to 512 steps if not specified
        try:
         # Move from -90 degrees to 0 degrees (quarter revolution, reverse)
                 step_motor(reverse_halfstep_seq, 0.001, 256)
                 time.sleep(1)

    # Move from 0 degrees to 90 degrees (quarter revolution, forward)
                 step_motor(halfstep_seq, 0.001, 256)
                 time.sleep(1)

        except KeyboardInterrupt:
                 pass
# Connect to the server
sio.connect(SERVER_URL)

#emit stepper-motor event
sio.emit('stepper-motor', room_ip)
print(room_ip,' attempted to be placed')
# Wait indefinitely for messages
sio.wait()

# Clean up GPIO pins on exit
def cleanup_gpio():
    GPIO.cleanup()
