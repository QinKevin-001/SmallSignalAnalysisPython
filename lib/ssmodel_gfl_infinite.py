import numpy as np
from scipy.optimize import fsolve

from lib.pf_func_ibr_infinite import pf_func_ibr_infinite
from lib.pf_calc_infinite import pf_calc_infinite
from lib.steadystatevalue_gfl import steadystatevalue_gfl
from lib.ssmodel_gfl import ssmodel_gfl
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_gfl_infinite(wbase, parasIBR, dominantParticipationFactorBoundary):
    # Power Flow Calculations
    x0 = np.array([0, 1])
    x, info, pfExitFlag, msg = fsolve(
        lambda x: pf_func_ibr_infinite(x, parasIBR),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    w, V1, V2, I = pf_calc_infinite(x, parasIBR)
    # Steady-State Values
    steadyStateValueX,  steadyStateValueU = steadystatevalue_gfl(w, V2, I, parasIBR)
    # Small-signal Modeling
    stateMatrix = ssmodel_gfl(wbase, parasIBR, steadyStateValueX, steadyStateValueU, 0)
    Asys = stateMatrix['A']
    ssVariables = stateMatrix['ssVariables']
    # Assigning "IBR" labels to the state variables
    if isinstance(ssVariables, (list, np.ndarray)):
        ssVariables = [[var, 'IBR'] if isinstance(var, str) or isinstance(ssVariables, np.ndarray) else var for var in
                       ssVariables]
    else:
        raise TypeError("Unsupported type for ssVariables")
    # Eigenvalue Analysis
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValueX, eigenvalueAnalysisResults, pfExitFlag