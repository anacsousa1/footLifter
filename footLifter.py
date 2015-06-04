# ######################################################################################################################
# ## footLifter.py
# ## Description: do the foot Lifter
# ## Library needed: stimulator, serial, imu, sys libraries
# ## Python interpreter: Anaconda 2.2.0 (python 2.7)
# ## Author: Ana Carolina Cardoso de Sousa
# ## Email: anacsousa1@gmail.com
# ## Created: Jun 04th 2015
# ######################################################################################################################

__authors__ = [
    "\"Ana de Sousa\" <anacsousa1@gmail.com>",
]


# Importing...
# import time
# import math
import userProfile
import imu
import serial
import sys
import stimulator

# Greetings
print "Welcome to ours Foot Lifter, let\'s get this started?\n"

# Ports and addresses
serialPortStimulator = 'COM8'       # in windows, verify "Manage Devices"
portIMU = 'COM9'                    # in windows, verify "Manage Devices"
addressIMU = 1                      # the device must have a stick informing it

# ########################### STIMULATOR INITIALIZATION
# Open stimulator port
print '\tWe are trying to connect to the Stimulator to port ' + serialPortStimulator + '.'

try:
    serialPortStimulator = serial.Serial(serialPortStimulator, timeout=1, writeTimeout=1, baudrate=115200)
except serial.SerialException:
    print '\t\tNo Hardware Found in ' + serialPortStimulator + '... :(\n \t\tExiting now. \n'
    sys.exit(0)

if not serialPortStimulator.isOpen():  # verify if it is already open
    serialPortStimulator.open()

stim = stimulator.Stimulator(serialPortStimulator)     # Construct object
print '\t\tWe are connected! Now, we are going to initialize the stimulator.!\n'

# Initialize stimulator
freq = 50
current = [8]
pulse_width = [500]
channels = 1
print "\tStandard parameters: " + str(freq) + "Hz " + str(current) + "mA " + str(pulse_width) + "us."

stim.initialization(freq, channels)

print "\n\tInitialized!"

# ########################### IMU INITIALIZATION
# Open IMU port

print '\tWe are trying to connect to the IMU (address ' + str(addressIMU) + ') to port ' + portIMU + '.'

try:
    serialPortIMU = serial.Serial(portIMU, timeout=1, writeTimeout=1, baudrate=115200)
except serial.SerialException:
    print '\t\tNo Hardware Found in ' + portIMU + '... :(\n \t\tExiting now. \n'
    sys.exit(1)

if not serialPortIMU.isOpen():  # verify if it is already open
    serialPortIMU.open()

device1 = imu.IMU(serialPortIMU, addressIMU)    # Construct object

testing = device1.getEulerAngles()              # Get some info
testing = testing.split(',', 6)                 # Convert to list

if len(testing) == 2:   # testing connection
    print '\t\tUnable to connect to the IMU... :(\n \t\tExiting now. \n'
    sys.exit(1)

# Calibrating
print '\t\tWe are connected! Now, we are going to calibrate the IMU. Keep it still!\n'

device1.calibrate()
device1.tare()

print "\t\t\tIMU Calibrated!\n"

# ########################### FOOT LIFTER

# First electrical stimulator signal update
stim.update(channels, pulse_width, current)

# Loop to change the pulse_width

exit_key = 'esc'
msg = "\n\tWrite a different width pulse (range between 100 and 500) like this [p]:\n\t(Write " + exit_key + " to exit)\n\t\t>>"

key_input = raw_input(msg)      # reads the keyboard

while key_input != exit_key:
    pulse_width[0] = int(key_input)                 # change pulse_width variable
    stim.update(channels, pulse_width, current)     # update the stimulator signal
    key_input = raw_input(msg)                      # reads the keyboard

# Stop the stimulator
stim.stop()

# Bye bye
serialPortStimulator.close()                   # close port
print 'Have a nice day!'
