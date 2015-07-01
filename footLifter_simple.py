# ######################################################################################################################
# ## footLifter.py
# ## Description: do the foot Lifter
# ## Library needed: stimulator, serial, imu, sys libraries
# ## Python interpreter: Anaconda 2.2.0 (python 2.7)
# ## Author: Ana Carolina Cardoso de Sousa
# ## Email: anacsousa1@gmail.com
# ## Created: Jul 1st 2015
# ######################################################################################################################

__authors__ = [
    "\"Ana de Sousa\" <anacsousa1@gmail.com>",
]


# Importing...
import subject_profile
import serial
import sys
import stimulator


# Important variables
user_name = 'antonio'
serialPortStimulator = 'COM6'        # in windows, verify "Manage Devices"
freq = 50
channels = 1

# #################################### Greetings
print "Welcome to ours Foot Lifter, let\'s get this started?\n"

# #################################### Ports and addresses

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

# #################################### Subject Profile
try:
    [current, pulse_width] = subject_profile.user[user_name]()
except:
        [current, pulse_width] = subject_profile.case_default()

print str(current)


# #################################### Initialize stimulator
print "\tStandard parameters: " + str(freq) + "Hz " + str(current) + "mA " + str(pulse_width) + "us."
stim.initialization(freq, channels)

print "\n\tInitialized! Stimulating channel."
stim.update(channels, pulse_width, current)  # First electrical stimulator signal update

# #################################### Loop to change the pulse_width

exit_key = 'esc'
msg = "\n\tStimulation started\n\t\t>>"

key_input = raw_input(msg)      # reads the keyboard

while key_input != exit_key:
    key_input = raw_input(msg)                      # reads the keyboard

# Stop the stimulator
stim.stop()

# Bye bye
serialPortStimulator.close()                   # close port
print 'Have a nice day!'