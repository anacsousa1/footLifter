# ######################################################################################################################
# ## subject_profile.py
# ## Description: define user profile
# ## Library needed:           libraries
# ## Python interpreter: Anaconda 2.2.0 (python 2.7)
# ## Author: Ana Carolina Cardoso de Sousa
# ## Email: anacsousa1@gmail.com
# ## Created: Jul 2st 2015
# ######################################################################################################################


__authors__ = [
    "\"Ana de Sousa\" <anacsousa1@gmail.com>",
]

def ana_claudia():
    print "User: Ana Claudia"
    current = [8]
    pulse_width = [100]
    return current, pulse_width
def ana_carolina():
    print "User: Ana Carolina"
    current = [8]
    pulse_width = [200]
    return current, pulse_width
def cristina():
    print "User: Cristina"
    current = [8]
    pulse_width = [300]
    return current, pulse_width
def claudir():
    print "User: Claudir"
    current = [8]
    pulse_width = [350]
    return current, pulse_width
def antonio():
    print "User: Antonio"
    current = [8]
    pulse_width = [500]
    return current, pulse_width
def case_default():
    print "default"

user = {'ana_claudia': ana_claudia, 'ana_carolina': ana_carolina, 'cristina': cristina, 'claudir': claudir, 'antonio': antonio}

if __name__ == '__main__':
    print user()

