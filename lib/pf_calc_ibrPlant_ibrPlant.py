#DONT TOUCH
import numpy as np

def pf_calc_ibrPlant_ibrPlant(x, parasLine1, parasLine2, parasLoad):
    # Define imaginary unit
    imagUnit = 1j

    # Extract states from input array
    w = x[0]
    theta0 = 0
    theta1 = x[1]
    theta2 = x[2]
    theta3 = x[3]
    Vabs0 = x[4]
    Vabs1 = x[5]
    Vabs2 = x[6]
    Vabs3 = x[7]

    # Extract line and load parameters
    Rline1 = parasLine1['Rline']
    Lline1 = parasLine1['Lline']
    Rline2 = parasLine2['Rline']
    Lline2 = parasLine2['Lline']
    Rx = parasLoad['Rx']

    # Compute impedances
    Zline1 = Rline1 + imagUnit * w * Lline1
    Zline2 = Rline2 + imagUnit * w * Lline2

    # Compute voltage phasors
    V0 = Vabs0 * np.exp(imagUnit * theta0)
    V1 = Vabs1 * np.exp(imagUnit * theta1)
    V2 = Vabs2 * np.exp(imagUnit * theta2)
    V3 = Vabs3 * np.exp(imagUnit * theta3)

    # Compute output currents
    Io1 = (V1 - V3) / Zline1 + V1 / Rx
    Io2 = (V2 - V3) / Zline2 + V2 / Rx

    return w, V1, V2, V3, Io1, Io2
