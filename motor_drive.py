# Stepper Mtor Driving Script
# for Raspberry Pi 4
#
# VDC to +ENA, +PUL, +DIR
# GPIO outputs to -ENA, -PUL, -DIR

from time import sleep
import RPi.GPIO as GPIO
import math

# GPIO assignment
PUL = 21
DIR = 20
ENA = 16

# Assign pins based on BCM mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Constant velocity, single-direction drive
def drive(dir, steps, steps_per_s):
    
    # Enable motor   
    GPIO.output(ENA, GPIO.HIGH)
    
    # Set motor direction
    if dir == 0:
        GPIO.output(DIR, GPIO.LOW)
    elif dir == 1:
        GPIO.output(DIR, GPIO.HIGH)
    else:
        None
    
    # Translate velocity to delay between pulses (s per step)
    delay = 1 / steps_per_s
    
    # Initialize pulse step
    GPIO.output(PUL, GPIO.LOW)
    
    # Driving loop
    for i in range(steps):
        
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay/2)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay/2)
        
      
# Driver Settings
pul_per_rev = 400
steps_per_deg = pul_per_rev / 360

# Drive the motor
travel_rpm = 40 # choose motor velocity in rpm. Note: start slewing at about 110 rpm with a single gear attached
steps_per_s = travel_rpm * pul_per_rev / 60
# Move 1
dir = 0 # choose motor direction (0 = ___, 1 = ___)
travel_deg = 360 # choose distance in degrees for motor to go
steps = math.floor(travel_deg * steps_per_deg)
drive(dir, steps, steps_per_s)
# Pause between moves
sleep(2)
# Move 2
dir = 1
travel_deg = 360
steps = math.floor(travel_deg * steps_per_deg)
drive(dir, steps, steps_per_s)


# Disable motor at end of run to save power
GPIO.output(ENA, GPIO.HIGH)




# Print numbers for debugging
travel_time = (1 / steps_per_s) * steps
print(steps)
print(steps_per_s)
print(travel_time)
