import numpy as np

def pf_calc_ibr_ibr(x, parasIBR1, parasIBR2):
    imagUnit = 1j

    w = x[0]
    theta1 = 0
    theta2 = x[1]
    theta3 = x[2]
    Vabs1 = x[3]
    Vabs2 = x[4]
    Vabs3 = x[5]

    Rc1 = parasIBR1['Rc']
    Lc1 = parasIBR1['Lc']
    Rc2 = parasIBR2['Rc']
    Lc2 = parasIBR2['Lc']

    Zc1 = Rc1 + imagUnit * w * Lc1
    Zc2 = Rc2 + imagUnit * w * Lc2

    V1 = Vabs1 * np.exp(imagUnit * theta1)
    V2 = Vabs2 * np.exp(imagUnit * theta2)
    V3 = Vabs3 * np.exp(imagUnit * theta3)

    Io1 = (V1 - V3) / Zc1
    Io2 = (V2 - V3) / Zc2

    return w, V1, V2, V3, Io1, Io2
