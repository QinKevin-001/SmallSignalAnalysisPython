import numpy as np

def pf_func_ibrPlant_infinite(x, parasIBR):
    PsetPlant = parasIBR['PsetPlant']
    QsetPlant = parasIBR['QsetPlant']
    wsetPlant = parasIBR['wsetPlant']
    VsetPlant = parasIBR['VsetPlant']
    mpPlant = parasIBR['mpPlant']
    mqPlant = parasIBR['mqPlant']
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
    S1 = V1 * np.conj(I)
    P1 = np.real(S1)
    Q1 = np.imag(S1)
    f = np.zeros(2)
    f[0] = (wsetPlant - w) / mpPlant + PsetPlant - P1
    f[1] = (VsetPlant - Vabs1) / mqPlant + QsetPlant - Q1

    return f