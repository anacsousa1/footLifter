# ######################################################################################################################
# ## phase_finder.py
# ## Description: do the foot Lifter
# ## Library needed: ...
# ## Python interpreter: Anaconda 2.2.0 (python 2.7)
# ## Author: Ana Carolina Cardoso de Sousa
# ## Email: anacsousa1@gmail.com
# ## Created: Jul 2st 2015
# ######################################################################################################################

__authors__ = [
    "\"Ana de Sousa\" <anacsousa1@gmail.com>",
]

def phase(pos, old_phase, rest_pos, th):
    th_p = 1.05 * rest_pos
    th_n = 0.90 * rest_pos

    th_old = th[1]
    if pos[1] > th_p:
        th = [1, 0]
    elif pos[1] < th_n:
        th = [0, 1]
    else:
        th = [0, 0]

    if old_phase == 1:
        if ((th[0] == 1) and (pos[0] < pos[1])) or ((th_old == 1) and (th[0] == 0)):
            phase_ = 0
        else:
            phase_ = old_phase
    else:
        if (th[1] == 1) and (pos[0] < pos[1]):
            phase_ = 1
        else:
            phase_ = old_phase


    return phase_

