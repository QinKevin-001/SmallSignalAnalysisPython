import numpy as np

def pf_func_ibr_ibr(x, parasGen1, parasGen2, parasLoad):
    Pset1 = parasGen1['Pset']
    Qset1 = parasGen1['Qset']
    wset1 = parasGen1['wset']
    Vset1 = parasGen1['Vset']
    mp1 = parasGen1['mp']
    mq1 = parasGen1['mq']

    Pset2 = parasGen2['Pset']
    Qset2 = parasGen2['Qset']
    wset2 = parasGen2['wset']
    Vset2 = parasGen2['Vset']
    mp2 = parasGen2['mp']
    mq2 = parasGen2['mq']

    Rc1 = parasGen1['Rc']
    Lc1 = parasGen1['Lc']
    Rc2 = parasGen2['Rc']
    Lc2 = parasGen2['Lc']

    Rload = parasLoad['Rload']
    Lload = parasLoad['Lload']
    Rx = parasLoad['Rx']

    imagUnit = 1j
    w = x[0]
    theta1 = 0
    theta2 = x[1]
    theta3 = x[2]
    Vabs1 = x[3]
    Vabs2 = x[4]
    Vabs3 = x[5]

    Zline1 = Rc1 + imagUnit * w * Lc1
    Zline2 = Rc2 + imagUnit * w * Lc2
    Zload = Rload + imagUnit * w * Lload

    V1 = Vabs1 * np.exp(imagUnit * theta1)
    V2 = Vabs2 * np.exp(imagUnit * theta2)
    V3 = Vabs3 * np.exp(imagUnit * theta3)

    Io1 = (V1 - V3) / Zline1
    Io2 = (V2 - V3) / Zline2

    So1 = V1 * np.conj(Io1)
    So2 = V2 * np.conj(Io2)

    Po1 = np.real(So1)
    Qo1 = np.imag(So1)

    Po2 = np.real(So2)
    Qo2 = np.imag(So2)

    Iload = V3 / Zload + V3 / Rx

    f = np.zeros(6, )
    f[0] = wset1 - mp1 * (Po1 - Pset1) - w
    f[1] = Vset1 - mq1 * (Qo1 - Qset1) - Vabs1
    f[2] = wset2 - mp2 * (Po2 - Pset2) - w
    f[3] = Vset2 - mq2 * (Qo2 - Qset2) - Vabs2
    f[4] = np.real(Io1 + Io2 - Iload)
    f[5] = np.imag(Io1 + Io2 - Iload)

    return f
