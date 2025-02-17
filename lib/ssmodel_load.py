import numpy as np
import sympy as sp

def ssmodel_load(wbase, parasLoad, steadyStateValuesX, steadyStateValuesU):
    # Define symbolic variables
    iloadD, iloadQ = sp.symbols('iloadD iloadQ')
    vbD, vbQ, wcom = sp.symbols('vbD vbQ wcom')

    # Parameters
    Rload = parasLoad['Rload']
    Lload = parasLoad['Lload']

    # Ordinary differential equations
    f = sp.Matrix([
        wbase * (vbD - Rload * iloadD + wcom * Lload * iloadQ) / Lload,
        wbase * (vbQ - Rload * iloadQ - wcom * Lload * iloadD) / Lload
    ])

    # State-Space Matrices
    stateVariables = ['$i_{loadD}$', '$i_{loadQ}$']
    x = sp.Matrix([iloadD, iloadQ])
    u = sp.Matrix([vbD, vbQ, wcom])

    # Calculate Jacobians
    Asym = f.jacobian(x)
    Bsym = f.jacobian(sp.Matrix([vbD, vbQ]))
    BwSym = f.jacobian(sp.Matrix([wcom]))

    # Ensure steadyStateValuesX and steadyStateValuesU are 1D arrays
    steadyStateValuesX = np.array(steadyStateValuesX).flatten()
    steadyStateValuesU = np.array(steadyStateValuesU).flatten()

    # Substitute steady-state values
    subs_dict = dict(zip(list(x) + list(u), np.concatenate((steadyStateValuesX, steadyStateValuesU))))
    A = Asym.subs(subs_dict).evalf()
    B = Bsym.subs(subs_dict).evalf()
    Bw = BwSym.subs(subs_dict).evalf()

    # Convert symbolic matrices to numerical arrays
    stateMatrix = {
        'A': np.array(A).astype(float),
        'B': np.array(B).astype(float),
        'Bw': np.array(Bw).astype(float),
        'ssVariables': stateVariables
    }

    return stateMatrix
