import numpy as np

def pf_calc_ibrPlant_sg(x, parasLine1, parasLine2, parasLoad):
    imagUnit = 1j

    # Unpack the variables from x (assumed to be an 8-element array)
    w      = x[0]
    theta0 = 0
    theta1 = x[1]
    theta2 = x[2]
    theta3 = x[3]
    Vabs0  = x[4]
    Vabs1  = x[5]
    Vabs2  = x[6]
    Vabs3  = x[7]

    # Extract line parameters (assuming dictionaries or objects)
    Rline1 = parasLine1['Rline'] if isinstance(parasLine1, dict) else parasLine1.Rline
    Lline1 = parasLine1['Lline'] if isinstance(parasLine1, dict) else parasLine1.Lline
    Rline2 = parasLine2['Rline'] if isinstance(parasLine2, dict) else parasLine2.Rline
    Lline2 = parasLine2['Lline'] if isinstance(parasLine2, dict) else parasLine2.Lline

    # Extract load parameter Rx
    Rx = parasLoad['Rx'] if isinstance(parasLoad, dict) else parasLoad.Rx

    # Calculate impedances
    Zline1 = Rline1 + imagUnit * w * Lline1
    Zline2 = Rline2 + imagUnit * w * Lline2

    # Calculate complex voltages
    V0 = Vabs0 * np.exp(imagUnit * theta0)  # V0 is computed but not returned
    V1 = Vabs1 * np.exp(imagUnit * theta1)
    V2 = Vabs2 * np.exp(imagUnit * theta2)
    V3 = Vabs3 * np.exp(imagUnit * theta3)

    # Calculate currents
    Io1 = (V1 - V3) / Zline1 + V1 / Rx
    Io2 = (V2 - V3) / Zline2 + V2 / Rx

    return w, V1, V2, V3, Io1, Io2
