#DONT TOUCH
import numpy as np

def steadystatevalue_load(w, Vb, parasLoad):
    # Parameters
    Rload = parasLoad['Rload']
    Lload = parasLoad['Lload']

    # Calculation
    imagUnit = 1j
    VbD = Vb.real
    VbQ = Vb.imag
    Zload = Rload + imagUnit * w * Lload
    Iload = Vb / Zload
    IloadD = Iload.real
    IloadQ = Iload.imag

    # Output
    steadyStateValuesX = np.array([IloadD, IloadQ])
    steadyStateValuesU = np.array([VbD, VbQ, w])

    return steadyStateValuesX, steadyStateValuesU
