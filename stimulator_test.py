# ######################################################################################################################
# ## stimulation_test.py
# ## Description: testing the stimulator
# ## Library needed: stimulator, serial, sys libraries
# ## Python interpreter: Anaconda 2.2.0 (python 2.7)
# ## Author: Ana Carolina Cardoso de Sousa
# ## Email: anacsousa1@gmail.com
# ## Created: Jun 04th 2015
# ######################################################################################################################

__authors__ = [
    "\"Ana de Sousa\" <anacsousa1@gmail.com>",
]


# Importing...
import serial
import sys
import stimulator

# Greetings
print "Welcome to ours stimulator tester, let\'s get this started?\n"

# Ports and addresses
serialPortStimulator = 'COM6'        # in windows, verify "Manage Devices"

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
print '\t\tWe are connected! Now, we are going to initialize the stimulator.!\n'


# Initialize stimulator
freq = 50
current = [8]
pulse_width = [500]
channels = 1
print "\tStandard parameters: " + str(freq) + "Hz " + str(current) + "mA " + str(pulse_width) + "us."

stim.initialization(freq, channels)

print "\n\tInitialized! Stimulating channel."

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
