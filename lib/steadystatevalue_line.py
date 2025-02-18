import numpy as np
import cmath

def steadystatevalue_line(w, Vb1, Vb2, parasLine):
    # Extract parameters
    Rline = parasLine['Rline']
    Lline = parasLine['Lline']

    # Define imaginary unit
    imagUnit = 1j

    # Compute voltage components
    VbD1 = Vb1.real
    VbQ1 = Vb1.imag
    VbD2 = Vb2.real
    VbQ2 = Vb2.imag

    # Compute line impedance
    Zline = Rline + imagUnit * w * Lline

    # Compute line current
    Iline = (Vb1 - Vb2) / Zline
    IlineD = Iline.real
    IlineQ = Iline.imag

    # Store steady-state values
    steadyStateValuesX = np.array([IlineD, IlineQ])
    steadyStateValuesU = np.array([VbD1, VbQ1, VbD2, VbQ2, w])

    return steadyStateValuesX, steadyStateValuesU
