# ######################################################################################################################
# ## stimulation_test.py
# ## Description: testing the stimulator
# ## Library needed: stimulator, serial
# ## Python interpreter: Anaconda 2.2.0 (python 2.7)
# ## Author: Ana Carolina Cardoso de Sousa
# ## Email: anacsousa1@gmail.com
# ## Created: Jun 03rd 2015
# ######################################################################################################################

__authors__ = [
    "\"Ana de Sousa\" <anacsousa1@gmail.com>",
]


# Importing...
import serial
import sys
import stimulator
import time
# import math
# import imu

# Greetings
print "Welcome to ours stimulator tester, let\'s get this started?\n"

# Ports and addresses
serialPortStimulator = 'COM8'        # in windows, verify "Manage Devices"

# Open ports
print '\tWe are trying to connect to the Stimulator to port ' + serialPortStimulator + '.'

try:
    serialPortStimulator = serial.Serial(serialPortStimulator, timeout=1, writeTimeout=1, baudrate=115200)
except serial.SerialException:
    print '\t\tNo Hardware Found in ' + serialPortStimulator + '... :(\n \t\tExiting now. \n'
    sys.exit(0)

if not serialPortStimulator.isOpen():  # verify if it is already open
    serialPortStimulator.open()


stim = stimulator.Stimulator(serialPortStimulator)     # Construct object


# Initialize stimulator
print "\tInitializing stimulator. Input the desired frequency and channels bellow.\n"
freq = 50
current = [12]
pulse_width = [500]
channels = 1

# freq = int(raw_input("\tInput frequency: "))            # get frequency
# channels = int(raw_input("\tInput channels: "))         # get channels
# current_str = raw_input("\tInput current: ")            # get current
# current = [int(i) for i in (current_str.split(","))]

stim.initialization(freq, channels)

print "\n\tStimulating channel " + str(channels) + " with frequency " + str(freq)

# Electrical stimulator signal update
stim.update(channels, pulse_width, current)

# Stop
raw_input("Press any key and done!")
stim.stop()

# Bye bye
serialPortStimulator.close()                   # close port
print 'Have a nice day!'
