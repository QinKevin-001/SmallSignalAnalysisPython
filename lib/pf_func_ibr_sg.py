import numpy as np

def pf_func_ibr_sg(x, parasGen1, parasGen2, parasLine1, parasLine2, parasLoad):
    # Extract generator parameters (assumed to be provided as dictionaries)
    Pset1 = parasGen1['Pset']
    Qset1 = parasGen1['Qset']
    wset1 = parasGen1['wset']
    Vset1 = parasGen1['Vset']
    mp1   = parasGen1['mp']
    mq1   = parasGen1['mq']

    Pset2 = parasGen2['Pset']
    Qset2 = parasGen2['Qset']
    wset2 = parasGen2['wset']
    Vset2 = parasGen2['Vset']
    mp2   = parasGen2['mp']
    mq2   = parasGen2['mq']

    # Extract line and load parameters
    Rline1 = parasLine1['Rline']
    Lline1 = parasLine1['Lline']
    Rline2 = parasLine2['Rline']
    Lline2 = parasLine2['Lline']

    Rload = parasLoad['Rload']
    Lload = parasLoad['Lload']
    Rx    = parasLoad['Rx']

    # Define imaginary unit
    imagUnit = 1j

    # Unpack the unknown vector x
    w     = x[0]
    theta1 = 0           # Reference angle
    theta2 = x[1]
    theta3 = x[2]
    Vabs1  = x[3]
    Vabs2  = x[4]
    Vabs3  = x[5]

    # Calculate impedances
    Zline1 = Rline1 + imagUnit * w * Lline1
    Zline2 = Rline2 + imagUnit * w * Lline2
    Zload  = Rload  + imagUnit * w * Lload

    # Calculate complex voltages
    V1 = Vabs1 * np.exp(imagUnit * theta1)
    V2 = Vabs2 * np.exp(imagUnit * theta2)
    V3 = Vabs3 * np.exp(imagUnit * theta3)

    # Calculate currents and complex powers
    Io1 = (V1 - V3) / Zline1
    So1 = V1 * np.conj(Io1)

    IlineSG = (V2 - V3) / Zline2
    Io2 = IlineSG + V2 / Rx
    So2 = V2 * np.conj(Io2)

    Po1 = np.real(So1)
    Qo1 = np.imag(So1)

    Po2 = np.real(So2)
    Qo2 = np.imag(So2)

    Iload = V3 / Zload + V3 / Rx

    # Initialize residual vector f (as a 1D array with 6 elements)
    f = np.zeros(6, dtype=float)

    # Power flow equations
    f[0] = wset1 - mp1 * (Po1 - Pset1) - w
    if np.isinf(mq1):
        f[1] = Vset1 - Vabs1
    else:
        f[1] = Vset1 - mq1 * (Qo1 - Qset1) - Vabs1

    f[2] = wset2 - mp2 * (Po2 - Pset2) - w
    if np.isinf(mq2):
        f[3] = Vset2 - Vabs2
    else:
        f[3] = Vset2 - mq2 * (Qo2 - Qset2) - Vabs2

    f[4] = np.real(Io1 + IlineSG - Iload)
    f[5] = np.imag(Io1 + IlineSG - Iload)

    return f
