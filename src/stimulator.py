# ######################################################################################################################
# ## stimulator.py
# ## Description: library for the stimulator
# ## Library needed: time library
# ## Python interpreter: Anaconda 2.2.0 (python 2.7)
# ## Author: Lucas Fonseca
# ## Email: lucasfonseca27@gmail.com
# ## Updated: Jun 03rd 2015
# ######################################################################################################################

# ######################################################################################################################
# ## TIPS FOR STIMULATOR
# ##         - First test it with an oscilloscope!
# ## TIPS FOR SERIAL
# ##        - For installing the serial package, go to (in english):
# ##                    https://pypi.python.org/pypi/pyserial
# ######################################################################################################################

__authors__ = [
    '"Lucas Fonseca" <lucasfonseca27@gmail.com>',
    "\"Ana de Sousa\" <anacsousa1@gmail.com>",
]


# import
import time


class Stimulator:
    def __init__(self, port):
        self.serial_port = port

    ########################################
    # Initialization
    ########################################


    def initialization(self, freq, channels):
        #    try:
        delay = 0.001
        # values for test
        ts1 = round((1 / float(freq)) * 1000)
        # print ts1
        ts2 = 1.5
        main_time = int(round((ts1 - 1) / 0.5))
        # main_time = int(round(ts1))
        group_time = int(round((ts2 - 1.5) / 0.5))
        channel_stim = channels
        channel_lf = 0
        n_factor = 0
        check = int((n_factor + channel_stim + channel_lf + group_time + main_time) % 8)

        init_1 = (1 << 7) | (0 << 6) | (check << 2) | (n_factor >> 1)
        init_2 = ((n_factor & 1) << 6) | (channel_stim >> 2)
        init_3 = ((channel_stim & 3) << 5) | (channel_lf >> 3)
        init_4 = ((channel_lf & 7) << 4) | (group_time >> 3)
        init_5 = ((group_time & 7) << 4) | (main_time >> 7)
        init_6 = main_time & 127

        # print(group_time)
        # print(init_1)
        # print(init_2)
        # print(init_3)
        # print(init_4)
        # print(init_5)
        # print(init_6)

        init = bytearray([init_1, init_2, init_3, init_4, init_5, init_6])

        dados = ""
        i = 1
        self.serial_port.write(init)  # writes at the port

        time.sleep(delay)
        while dados == "":
            self.serial_port.flush()
            data = self.serial_port.read(self.serial_port.inWaiting())  # reads bytearray port
            dados = data.decode()  # converts bytearray in a string
            i += 1
            if i > 10000:
                #  print "No answer."
                dados = 'No answer'
                return dados
        dados = data.decode()  # converts bytearray in a string
        # print "resposta: " + dados
        # print data

        # except ValueError:
        # print("Error (initialization)")

        return dados

    ########################################
    # Update
    ########################################

    def update(self, channels, width, current):

        try:
            # print "beggining update"
            # values for test
            # for i in width:
            #   pulse_width(i) = width
            pulse_width = width
            pulse_current = current
            mode = 0
            # a = sum(pulse_width)
            # print type(width[0])
            # pulse_width = [200]
            # pulse_current = [4]
            check = int((mode + sum(pulse_width) + sum(pulse_current)) % 32)
            init_b = []
            for i in range(len(width) * 3 + 1):
                init_b.append(0)
            init_b[0] = (1 << 7) | (1 << 5) | check
            for i in range(len(width)):
                init_b[i * 3 + 1] = (mode << 5) | (int(pulse_width[i]) >> 7)
                init_b[i * 3 + 2] = (int(pulse_width[i]) & 127)
                init_b[i * 3 + 3] = pulse_current[i]

                # print(init_1)
                # print(init_2)
                # print(init_3)
                # print(init_4)
                # init(1) = init_b(1)

            init = bytearray(init_b)

            i = 0


            # print "requesting update"
            self.serial_port.flush()
            self.serial_port.write(init)  # writes at the port
            dados = ""
            # print "wrote"
            while dados == "":
                self.serial_port.flush()
                data = self.serial_port.read(self.serial_port.inWaiting())  # reads bytearray port
                dados = data.decode()  # converts bytearray in a string
                i += 1
                if i > 10000:
                    # print "No answer."
                    dados = 'No answer'
                    return dados

            dados = data.decode()  # converts bytearray in a string



        except ValueError:
            return 'Error'

        return dados

    ########################################
    # Stop
    ########################################

    def stop(self):
        try:
            stop_1 = 192
            stop = bytearray([stop_1])
            i = 1
            self.serial_port.write(stop)  # writes at the port
            dados = ""

            while dados == "":
                self.serial_port.flush()
                data = self.serial_port.read(self.serial_port.inWaiting())  # reads bytearray port
                dados = data.decode()  # converts bytearray in a string
                i += 1
                if i > 10000:
                    # print "No answer."
                    dados = 'No answer'
                    return dados

                    # dados = data.decode()  # converts bytearray in a string
                    # print "answer: " + dados

        except ValueError:
            return 0

        return dados
