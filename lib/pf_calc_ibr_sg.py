import numpy as np

def pf_calc_ibr_sg(x, parasLine1, parasLine2, parasLoad):
    # Define imaginary unit
    imagUnit = 1j

    # Unpack variables from x (assuming x is a 1D array or list of length 6)
    w      = x[0]
    theta1 = 0
    theta2 = x[1]
    theta3 = x[2]
    Vabs1  = x[3]
    Vabs2  = x[4]
    Vabs3  = x[5]

    # Extract line parameters (assumed to be dictionaries or objects with attributes)
    Rline1 = parasLine1['Rline'] if isinstance(parasLine1, dict) else parasLine1.Rline
    Lline1 = parasLine1['Lline'] if isinstance(parasLine1, dict) else parasLine1.Lline
    Rline2 = parasLine2['Rline'] if isinstance(parasLine2, dict) else parasLine2.Rline
    Lline2 = parasLine2['Lline'] if isinstance(parasLine2, dict) else parasLine2.Lline

    # Calculate impedances
    Zline1 = Rline1 + imagUnit * w * Lline1
    Zline2 = Rline2 + imagUnit * w * Lline2

    # Calculate complex voltages
    V1 = Vabs1 * np.exp(imagUnit * theta1)
    V2 = Vabs2 * np.exp(imagUnit * theta2)
    V3 = Vabs3 * np.exp(imagUnit * theta3)

    # Calculate currents
    Io1 = (V1 - V3) / Zline1
    # Extract Rx from parasLoad
    Rx = parasLoad['Rx'] if isinstance(parasLoad, dict) else parasLoad.Rx
    Io2 = (V2 - V3) / Zline2 + V2 / Rx

    return w, V1, V2, V3, Io1, Io2
