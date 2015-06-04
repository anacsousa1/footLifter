# ######################################################################################################################
# ## userProfile.py
# ## Description: describe the user profile
# ## Library needed:
# ## Python interpreter: Anaconda 2.2.0 (python 2.7)
# ## Author: Ana Carolina Cardoso de Sousa
# ## Email: anacsousa1@gmail.com
# ## Created: Jun 04th 2015
# ######################################################################################################################

__authors__ = [
    "\"Ana de Sousa\" <anacsousa1@gmail.com>",
]


####################################
####################################
def phase(ang):
    if -20 < ang < 20:
        return 0
    elif ang < -20:
        return -1
    elif ang > 20:
        return 1
    return


####################################
####################################
def muscle(phase_):     # muscle
    out = 0
    if phase_ == 0:
        out = 0
    elif phase_ == -1:
        out = 100
    elif phase_ == 1:
        out = 200
    return out



