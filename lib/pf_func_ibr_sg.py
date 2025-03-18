import numpy as np
import cmath

def pf_func_ibr_sg(x, parasGen1, parasGen2, parasLine1, parasLine2, parasLoad):
    # Extract parameters
    Pset1, Qset1 = parasGen1['Pset'], parasGen1['Qset']
    wset1, Vset1 = parasGen1['wset'], parasGen1['Vset']
    mp1, mq1 = parasGen1['mp'], parasGen1['mq']

    Pset2, Qset2 = parasGen2['Pset'], parasGen2['Qset']
    wset2, Vset2 = parasGen2['wset'], parasGen2['Vset']
    mp2, mq2 = parasGen2['mp'], parasGen2['mq']

    Rline1, Lline1 = parasLine1['Rline'], parasLine1['Lline']
    Rline2, Lline2 = parasLine2['Rline'], parasLine2['Lline']

    Rload, Lload = parasLoad['Rload'], parasLoad['Lload']
    Rx = parasLoad['Rx']

    # Unpack state vector
    w = x[0]
    theta1 = 0  # Reference angle
    theta2, theta3 = x[1], x[2]
    Vabs1, Vabs2, Vabs3 = x[3], x[4], x[5]

    # Complex calculations
    Zline1 = Rline1 + 1j * w * Lline1
    Zline2 = Rline2 + 1j * w * Lline2
    Zload = Rload + 1j * w * Lload

    # Complex voltages
    V1 = Vabs1 * np.exp(1j * theta1)
    V2 = Vabs2 * np.exp(1j * theta2)
    V3 = Vabs3 * np.exp(1j * theta3)

    # Current and power calculations
    Io1 = (V1 - V3) / Zline1
    So1 = V1 * np.conj(Io1)

    IlineSG = (V2 - V3) / Zline2
    Io2 = IlineSG + V2 / Rx
    So2 = V2 * np.conj(Io2)

    Po1, Qo1 = So1.real, So1.imag
    Po2, Qo2 = So2.real, So2.imag

    Iload = V3 / Zload + V3 / Rx

    # Power flow equations
    f = np.zeros(6)
    f[0] = wset1 - mp1 * (Po1 - Pset1) - w

    # Fix: Handle infinite mq cases properly
    if np.isinf(mq1):
        f[1] = Vset1 - Vabs1
    else:
        f[1] = Vset1 - mq1 * (Qo1 - Qset1) - Vabs1

    f[2] = wset2 - mp2 * (Po2 - Pset2) - w

    if np.isinf(mq2):
        f[3] = Vset2 - Vabs2
    else:
        f[3] = Vset2 - mq2 * (Qo2 - Qset2) - Vabs2

    # Current balance equations
    f[4] = (Io1 + IlineSG - Iload).real
    f[5] = (Io1 + IlineSG - Iload).imag

    return f