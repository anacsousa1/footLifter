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
    if (0 <= ang < 88) or (ang >= 358):
        return 1
    elif 88 <= ang < 178:
        return 2
    elif 178 <= ang < 268:
        return 3
    elif 268 <= ang < 358:
        return 4
    return


####################################
####################################
def muscle(phase_):     # muscle
    out = 0
    if phase_ == 1:
        out = 0
    elif phase_ == 2:
        out = 100
    elif phase_ == 3:
        out = 200
    elif phase_ == 4:
        out = 300
    return out



