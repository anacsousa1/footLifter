# ######################################################################################################################
# ## my_plotter.py
# ## Description: plot IMU data
# ## Library needed: matplotlib.pyplot, matplotlib.animation, scipy.io, imu, time, math, serial, sys libraries
# ## Python interpreter: Anaconda 2.2.0 (python 2.7)
# ## Author: Ana Carolina Cardoso de Sousa
# ## Email: anacsousa1@gmail.com
# ## Created: Jun 26th 2015
# ## See: http://matplotlib.org/users/pyplot_tutorial.html for matplotlib.pyplot
# ######################################################################################################################


__authors__ = [
    "\"Ana de Sousa\" <anacsousa1@gmail.com>",
]

# Importing...
import time
import math
import imu
import sys
import serial
import matplotlib.pyplot as plt
import scipy.io as sio

# ##############################################################################
# Ports and addresses
portIMU = 'COM4'        # in windows, verify "Manage Devices"
addressIMU = 1          # the device must have a stick informing it

# Open ports
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

# Calibrating
print '\t\tWe are connected! Now, we are going to calibrate the IMU. Keep it still!\n'

device1.calibrate()
device1.tare()

print "\t\t\tIMU Calibrated!\n"

# First...
plt.close('all')
dt = 0.1  # each dt seconds
T = 2    #

# ##############################################################################
# ## Get data
time_ = []
x = []
v = []
N = T / dt  # number of samples

print '\n\t\tWhenever you\'re ready, press button 1 (the left one)!'  # Wait until the user press the 'Start'
while not (device1.checkButtons() == 1):
    pass

plt.figure(1)
plt.ion()
plt.show()

i = 0
pitch = 90
pitch_old = 90
print 'reading...'

while not (device1.checkButtons() == 2):

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
    time.sleep(dt)
    pitch_old = pitch

    plt.subplot(211)
    plt.scatter(time_, x, color='blue', marker=u'.')

    plt.subplot(212)
    plt.scatter(time_, v, color='red', marker=u'.')
    plt.draw()

    i += 1

# ##############################################################################

# Save data
print "Save data."

sio.savemat('x.mat', {'x': x})
sio.savemat('v.mat', {'v': v})
sio.savemat('time.mat', {'time_': time_})

# Plot Pitch angle
print "Plot pitch angle"
plt.close('all')
plt.ioff()

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

print "Bye bye!"
