import numpy as np
import sympy as sp

def ssmodel_line(wbase, parasLine, steadyStateValuesX, steadyStateValuesU):
    ilineD, ilineQ = sp.symbols('ilineD ilineQ')
    vbD1, vbQ1, vbD2, vbQ2, wcom = sp.symbols('vbD1 vbQ1 vbD2 vbQ2 wcom')
    # Parameters
    Rline = parasLine['Rline']
    Lline = parasLine['Lline']
    # Algebraic equations
    f = sp.Matrix([
        wbase * (vbD1 - vbD2 - Rline * ilineD + wcom * Lline * ilineQ) / Lline,
        wbase * (vbQ1 - vbQ2 - Rline * ilineQ - wcom * Lline * ilineD) / Lline
    ])
    # State-Space Matrices
    stateVariables = ['$i_{lineD}$', '$i_{lineQ}$']
    x = sp.Matrix([ilineD, ilineQ])
    u = sp.Matrix([vbD1, vbQ1, vbD2, vbQ2, wcom])
    # Calculate Jacobians
    Asym = f.jacobian(x)
    B1sym = f.jacobian(sp.Matrix([vbD1, vbQ1]))
    B2sym = f.jacobian(sp.Matrix([vbD2, vbQ2]))
    BwSym = f.jacobian(sp.Matrix([wcom]))
    # Ensure steadyStateValuesX and steadyStateValuesU are 1D arrays
    steadyStateValuesX = np.array(steadyStateValuesX).flatten()
    steadyStateValuesU = np.array(steadyStateValuesU).flatten()
    # Substitute steady-state values
    subs_dict = dict(zip(list(x) + list(u), np.concatenate((steadyStateValuesX, steadyStateValuesU))))
    A = Asym.subs(subs_dict).evalf()
    B1 = B1sym.subs(subs_dict).evalf()
    B2 = B2sym.subs(subs_dict).evalf()
    Bw = BwSym.subs(subs_dict).evalf()
    stateMatrix = {
        'A': np.array(A).astype(float),
        'B1': np.array(B1).astype(float),
        'B2': np.array(B2).astype(float),
        'Bw': np.array(Bw).astype(float),
        'ssVariables': stateVariables
    }

    return stateMatrix
