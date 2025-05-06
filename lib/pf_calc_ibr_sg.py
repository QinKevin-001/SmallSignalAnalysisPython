import numpy as np

def pf_calc_ibr_sg(x, parasLine1, parasLine2, parasLoad):
    imagUnit = 1j

    w = x[0]
    theta1 = 0
    theta2 = x[1]
    theta3 = x[2]
    Vabs1 = x[3]
    Vabs2 = x[4]
    Vabs3 = x[5]

    Rline1 = parasLine1['Rline']
    Lline1 = parasLine1['Lline']
    Rline2 = parasLine2['Rline']
    Lline2 = parasLine2['Lline']

    Zline1 = Rline1 + imagUnit * w * Lline1
    Zline2 = Rline2 + imagUnit * w * Lline2

    V1 = Vabs1 * np.exp(imagUnit * theta1)
    V2 = Vabs2 * np.exp(imagUnit * theta2)
    V3 = Vabs3 * np.exp(imagUnit * theta3)

    Io1 = (V1 - V3) / Zline1
    Io2 = (V2 - V3) / Zline2 + V2 / parasLoad['Rx']

    return w, V1, V2, V3, Io1, Io2
