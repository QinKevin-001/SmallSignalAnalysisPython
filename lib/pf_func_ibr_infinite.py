#DONT TOUCH
import numpy as np

def pf_func_ibr_infinite(x, parasIBR):
    Pset = parasIBR['Pset']
    Qset = parasIBR['Qset']
    wset = parasIBR['wset']
    Vset = parasIBR['Vset']
    mp = parasIBR['mp']
    mq = parasIBR['mq']
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
    S2 = V2 * np.conj(I)

    P2 = np.real(S2)
    Q2 = np.imag(S2)

    f = np.zeros(2, )
    f[0] = (wset - w) / mp + Pset - P2
    f[1] = (Vset - Vabs2) / mq + Qset - Q2

    return f