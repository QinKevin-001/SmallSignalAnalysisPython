import numpy as np
import sympy as sp

def ssmodel_load(wbase, parasLoad, steadyStateValuesX, steadyStateValuesU):
    iloadD, iloadQ = sp.symbols('iloadD iloadQ')
    vbD, vbQ, wcom = sp.symbols('vbD vbQ wcom')
    # Parameters
    Rload = parasLoad['Rload']
    Lload = parasLoad['Lload']
    # Ordinary differential equations
    f = sp.Matrix([
        wbase*(vbD - Rload*iloadD + wcom*Lload*iloadQ)/Lload,
        wbase*(vbQ - Rload*iloadQ - wcom*Lload*iloadD)/Lload
    ])
    # Define state variables as a 2-column structure for consistency.
    stateVariables = [['$i_{loadD}$', ''], ['$i_{loadQ}$', '']]
    x = sp.Matrix([iloadD, iloadQ])
    u = sp.Matrix([vbD, vbQ, wcom])
    # Calculate Jacobians
    Asym = f.jacobian(x)
    Bsym = f.jacobian(sp.Matrix([vbD, vbQ]))
    BwSym = f.jacobian(sp.Matrix([wcom]))
    steadyStateValuesX = np.array(steadyStateValuesX).flatten()
    steadyStateValuesU = np.array(steadyStateValuesU).flatten()
    subs_dict = dict(zip(list(x) + list(u), np.concatenate((steadyStateValuesX, steadyStateValuesU))))
    A = Asym.subs(subs_dict).evalf()
    B = Bsym.subs(subs_dict).evalf()
    Bw = BwSym.subs(subs_dict).evalf()
    stateMatrix = {
        'A': np.array(A).astype(float),
        'B': np.array(B).astype(float),
        'Bw': np.array(Bw).astype(float),
        'ssVariables': np.array(stateVariables)
    }

    return stateMatrix