import numpy as np

def pf_calc_infinite(x, parasIBR):
    Rc = parasIBR['Rc']
    Lc = parasIBR['Lc']

    imagUnit = 1j
    w = 1
    theta1 = 0
    theta2 = x[0]
    Vabs1 = 1
    Vabs2 = x[1]

    Zc = Rc + imagUnit * w * Lc
    V1 = Vabs1 * np.exp(imagUnit * theta1)
    V2 = Vabs2 * np.exp(imagUnit * theta2)
    I = (V2 - V1) / Zc

    return w, V1, V2, I