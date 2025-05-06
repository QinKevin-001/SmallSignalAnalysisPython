import numpy as np

def pf_func_ibrPlant_ibrPlant(x, parasGen1, parasGen2, parasLine1, parasLine2, parasLoad):
    Pset1 = parasGen1['PsetPlant']
    Qset1 = parasGen1['QsetPlant']
    wset1 = parasGen1['wsetPlant']
    Vset1 = parasGen1['VsetPlant']
    mp1 = parasGen1['mpPlant']
    mq1 = parasGen1['mqPlant']
    Rc1 = parasGen1['Rc']

    Pset2 = parasGen2['PsetPlant']
    Qset2 = parasGen2['QsetPlant']
    wset2 = parasGen2['wsetPlant']
    Vset2 = parasGen2['VsetPlant']
    mp2 = parasGen2['mpPlant']
    mq2 = parasGen2['mqPlant']
    Lc1 = parasGen1['Lc']

    Rline1 = parasLine1['Rline']
    Lline1 = parasLine1['Lline']
    Rline2 = parasLine2['Rline']
    Lline2 = parasLine2['Lline']

    Rload = parasLoad['Rload']
    Lload = parasLoad['Lload']
    Rx = parasLoad['Rx']

    imagUnit = 1j
    w = x[0]
    theta0 = 0
    theta1 = x[1]
    theta2 = x[2]
    theta3 = x[3]
    Vabs0 = x[4]
    Vabs1 = x[5]
    Vabs2 = x[6]
    Vabs3 = x[7]

    Zc1 = Rc1 + imagUnit * w * Lc1
    Zline1 = Rline1 + imagUnit * w * Lline1
    Zline2 = Rline2 + imagUnit * w * Lline2
    Zload = Rload + imagUnit * w * Lload

    V0 = Vabs0 * np.exp(imagUnit * theta0)
    V1 = Vabs1 * np.exp(imagUnit * theta1)
    V2 = Vabs2 * np.exp(imagUnit * theta2)
    V3 = Vabs3 * np.exp(imagUnit * theta3)

    Iline1 = (V1 - V3) / Zline1
    Io1 = Iline1 + V1 / Rx
    So1 = V1 * np.conj(Io1)
    Vo1 = V1 + Io1 * Zc1

    Iline2 = (V2 - V3) / Zline2
    Io2 = Iline2 + V2 / Rx
    So2 = V2 * np.conj(Io2)

    Po1 = np.real(So1)
    Qo1 = np.imag(So1)

    Po2 = np.real(So2)
    Qo2 = np.imag(So2)

    Iload = V3 / Zload + V3 / Rx

    f = np.zeros(8, )
    f[0] = wset1 - mp1 * (Po1 - Pset1) - w
    f[1] = Vset1 - mq1 * (Qo1 - Qset1) - Vabs1
    f[2] = wset2 - mp2 * (Po2 - Pset2) - w
    f[3] = Vset2 - mq2 * (Qo2 - Qset2) - Vabs2
    f[4] = np.real(Iline1 + Iline2 - Iload)
    f[5] = np.imag(Iline1 + Iline2 - Iload)
    f[6] = np.real(Vo1 - V0)
    f[7] = np.imag(Vo1 - V0)

    return f
