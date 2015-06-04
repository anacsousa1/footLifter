# ######################################################################################################################
# ## imu.py
# ## Description: library for the IMU
# ## Python interpreter: Anaconda 2.2.0 (python 2.7)
# ## Author: Lucas Fonseca
# ## Email: lucasfonseca27@gmail.com
# ## Updated: May 29th 2015
# ######################################################################################################################

# ######################################################################################################################
# ## TIPS FOR IMU
# ##         - Install the YEI 3 space sensor with the YEI 3-SPACE SENSOR SOFTWARE SUITE.
# ##         - The software will install the drivers, inform you the IMU port and the device address.
# ##         - For win8, install the driver without the signature (in portuguese):
# ##                    http://www.hardware.com.br/comunidade/instalar-driver/1358528/
# ## TIPS FOR SERIAL
# ##        - For installing the serial package, go to (in english):
# ##                    https://pypi.python.org/pypi/pyserial
# ######################################################################################################################

__authors__ = [
    '"Lucas Fonseca" <lucasfonseca27@gmail.com>',
    "\"Ana de Sousa\" <anacsousa1@gmail.com>",
]


class IMU:
    def __init__(self, port, address):
        """

        :rtype : object
        """
        self.serial_port = port
        self.address = address

    # #######################################
    # Calibration
    # #######################################

    def calibrate(self):
        msg = ">" + str(self.address) + ",165\n".encode()
        try:
            if self.serial_port is not None:
                self.serial_port.write(msg)     # writes at the port
                dados = read_data(self.serial_port)
                return dados

            else:
                return 0
        except ValueError:
            return 0


    ########################################
    # Set euler to YXZ
    ########################################

    def setEulerToYXZ(self):
        msg = ">" + str(self.address) + ",16,1\n".encode()
        try:
            if self.serial_port is not None:
                self.serial_port.write(msg)     # writes at the port
                dados = read_data(self.serial_port)
                return dados
            else:
                return 0
        except ValueError:
            return 0


    ########################################
    # Tare with current orientation
    ########################################

    def tare(self):
        msg = ">" + str(self.address) + ",96\n".encode()
        try:
            if self.serial_port is not None:
                self.serial_port.write(msg)     # writes at the port
                dados = read_data(self.serial_port)
                return dados
            else:
                return 0
        except ValueError:
            return 0

    ########################################
    # Check Buttons
    ########################################

    def checkButtons(self):

        try:
            if self.serial_port is not None:
                # Get button state) and writes at the port
                self.serial_port.write((">" + str(self.address) + ",250\n".encode()))
                dados = read_data(self.serial_port)
                botao = dados.split(",")
                if len(botao) == 4:
                    botao = botao[3]
                    if int(botao) == 1:
                        return 1
                    elif int(botao) == 2:
                        return 2
                    else:
                        return 0

        except ValueError:
            return 'Error'

    ########################################
    # Get Euler Angles
    ########################################

    def getEulerAngles(self):
        msg = ">" + str(self.address) + ",1\n".encode()
        try:
            if self.serial_port is not None:
                self.serial_port.write(msg)     # writes at the port
                dados = read_data(self.serial_port)
                return dados
            else:
                return 'Port error'
        except ValueError:
            return 'Error'

    ########################################
    # Get Gyro Data
    ########################################

    def getGyroData(self):
        msg = ">" + str(self.address) + ",33\n".encode()
        try:
            if self.serial_port is not None:
                self.serial_port.write(msg)     # writes at the port
                dados = read_data(self.serial_port)
                return dados
            else:
                return 'Port error'
        except ValueError:
            return 'Error'


    ########################################
    # Single Command
    ########################################

    def singleCommand(self, command):
        try:
            if self.serial_port is not None:
                self.serial_port.write(">" + str(self.address) + "," + command + "\n")     # writes at the port
                dados = read_data(self.serial_port)
                dados = dados.split(",")
                if int(dados[0]) == 0:
                    return dados
                else:
                    return "No answer"
            else:
                return 'Port error'

        except ValueError:
            return 'Error'


# #######################################
# Read data
# #######################################

def read_data(port):
    dados = ''
    i = 1
    while dados == "":
        port.flush()
        data = port.read(port.inWaiting())          # reads from bytearray
        dados = data.decode()                       # converts bytearray in string
        i += 1
        if i > 10000:
            dados = 'No answer'
            break
    return dados
