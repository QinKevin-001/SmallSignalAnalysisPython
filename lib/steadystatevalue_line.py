import numpy as np

def steadystatevalue_line(w, Vb1, Vb2, parasLine):
    # parameters
    Rline = parasLine['Rline']
    Lline = parasLine['Lline']

    imagUnit = 1j
    VbD1 = Vb1.real
    VbQ1 = Vb1.imag
    VbD2 = Vb2.real
    VbQ2 = Vb2.imag
    Zline = Rline + imagUnit * w * Lline
    Iline = (Vb1 - Vb2) / Zline
    IlineD = Iline.real
    IlineQ = Iline.imag
    steadyStateValuesX = np.array([IlineD, IlineQ])
    steadyStateValuesU = np.array([VbD1, VbQ1, VbD2, VbQ2, w])

    return steadyStateValuesX, steadyStateValuesU
