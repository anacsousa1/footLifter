# ######################################################################################################################
# ## footLifter.py
# ## Description: do the foot Lifter
# ## Library needed: ....
# ## Python interpreter: Anaconda 2.2.0 (python 2.7)
# ## Author: Ana Carolina Cardoso de Sousa
# ## Email: anacsousa1@gmail.com
# ## Created: Jul 2st 2015
# ######################################################################################################################

__authors__ = [
    "\"Ana de Sousa\" <anacsousa1@gmail.com>",
]


# Importing...
import subject_profile
import serial
import sys
import stimulator
import time
import math
import imu
import numpy
import matplotlib.pyplot as plt
import scipy.io as sio
import phase_finder


# Important variables
user_name = 'claudir'
serialPortStimulator = 'COM6'        # in windows, verify "Manage Devices"
portIMU = 'COM7'                     # in windows, verify "Manage Devices"
addressIMU = 1                       # the device must have a stick informing it
freq = 50
channels = 1
plt.close('all')
dt = 0.01
T = 2
Tr = 0.5

# #################################### Greetings
print "Welcome to ours Foot Lifter, let\'s get this started?\n"

# #################################### Ports and addresses
                                    # stimulator
print '\tWe are trying to connect to the Stimulator to port ' + serialPortStimulator + '.'

try:  # Open ports
    serialPortStimulator = serial.Serial(serialPortStimulator, timeout=1, writeTimeout=1, baudrate=115200)
except serial.SerialException:
    print '\t\tNo Hardware Found in ' + serialPortStimulator + '... :(\n \t\tExiting now. \n'
    sys.exit(0)

if not serialPortStimulator.isOpen():  # verify if it is already open
    serialPortStimulator.open()

stim = stimulator.Stimulator(serialPortStimulator)     # Construct object
print '\t\tWe are connected! Now, we are going to initialize the stimulator.!\n'

# IMU
print '\tWe are trying to connect to the IMU (address ' + str(addressIMU) + ') to port ' + portIMU + '.'
try:
    serialPortIMU = serial.Serial(portIMU, timeout=1, writeTimeout=1, baudrate=115200)
except serial.SerialException:
    print '\t\tNo Hardware Found in ' + portIMU + '... :(\n \t\tExiting now. \n'
    sys.exit(0)

if not serialPortIMU.isOpen():  # verify if it is already open
    serialPortIMU.open()

device1 = imu.IMU(serialPortIMU, addressIMU)    # Construct object
testing = device1.getEulerAngles()              # Get some info
testing = testing.split(',', 6)                 # Convert to list

if len(testing) == 2:   # testing connection
    print '\t\tUnable to connect to the IMU... :(\n \t\tExiting now. \n'
    sys.exit(1)

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

# #################################### Calibrating
print '\t\tWe are connected! Now, we are going to calibrate the IMU. Keep it still!\n'

device1.calibrate()
device1.tare()

print "\t\t\tIMU Calibrated!\n"


# #################################### Initialize to get data
# initialize variables
time_ = []
x = []
stim_times = []
x_rest = []
v = []
N = T / dt
i = 0
pitch = 90
pitch_old = 90
th = [0, 0]
old_phase = 1

# Wait until the user press the 'Start' button
print '\n\t\tWhenever you\'re ready, press button 1 (the left one)!'
while not (device1.checkButtons() == 1):
    pass

# initialize figure
plt.figure(1)
plt.ion()
plt.show()

print '\n\tGetting rest position...'
time.sleep(2)

# #################################### Get rest position
for i in range(10):

    angles = device1.getEulerAngles()   # get angles
    angles = angles.split(',', 6)       # convert to list

    if len(angles) == 6:                # if we connect correctly with the device
        pitch = float(angles[4])
        if pitch >= 0:
            pitch = 90 + math.degrees(pitch)
        else:
            pitch = 90 + math.degrees(pitch)

    x_rest.append(pitch)
    time.sleep(dt)

rest_pos = numpy.mean(x_rest)

print '\nGot rest position:'
old_pos = rest_pos

time.sleep(3)
stim.update(channels, pulse_width, current)  # First electrical stimulator signal update

# #################################### Routine!!!                                       <<=== important! ===>
while not (device1.checkButtons() == 2):  # Press 2 to stop (the right one)

    angles = device1.getEulerAngles()   # get angles
    angles = angles.split(',', 6)       # convert to list

    if len(angles) == 6:                # if we connect correctly with the device
        pitch = float(angles[4])
        if pitch >= 0:
            pitch = 90 + math.degrees(pitch)
        else:
            pitch = 90 + math.degrees(pitch)

    v.append((pitch - pitch_old) / dt)
    x.append(pitch)
    time_.append(i * dt)
    pitch_old = pitch

    # find phase:
    pos = [pitch, old_pos]
    phase = phase_finder.phase(pos, old_phase, rest_pos, th)
    print phase

    # stimulation:
    if phase == 1:
        stim.update(channels, pulse_width, current)
        stim_times.append(i)
    else:
        stim.update(channels, [0], [0])

    # plot
    plt.subplot(211)
    plt.scatter(time_, x, color='blue', marker=u'.')

    plt.subplot(212)
    plt.scatter(time_, v, color='red', marker=u'.')
    plt.draw()

    # update old data
    old_pos = pitch
    old_phase = phase

    # go ahead
    time.sleep(dt)
    i += 1

# #################################### Save data
print "Save data."

sio.savemat('x.mat', {'x': x})
sio.savemat('v.mat', {'v': v})
sio.savemat('stim_times.mat', {'stim_times': stim_times})
sio.savemat('time.mat', {'time_': time_})

# Plot Pitch angle
print "Plot pitch angle"
plt.ioff()
plt.close('all')

plt.figure(1)
plt.subplot(211)
plt.plot(time_, x, 'b')
plt.xlabel('Time (seg)')
plt.ylabel('Pitch Angle (deg)')

plt.subplot(212)
plt.plot(time_, v, 'r')
plt.xlabel('Time (seg)')
plt.ylabel('Pitch Velocity (deg/s)')

plt.show()

# #################################### Bye bye
time.sleep(1)
stim.stop()
serialPortIMU.close()                               # close port
serialPortStimulator.close()                        # close port
print 'Have a nice day!'
