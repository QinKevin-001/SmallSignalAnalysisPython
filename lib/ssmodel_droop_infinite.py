import numpy as np
from scipy.optimize import fsolve

from lib.pf_func_ibr_infinite import pf_func_ibr_infinite
from lib.pf_calc_infinite import pf_calc_infinite
from lib.steadystatevalue_droop import steadystatevalue_droop
from lib.ssmodel_droop import ssmodel_droop
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_droop_infinite(wbase, parasIBR, dominantParticipationFactorBoundary):
    # Power Flow Calculation
    x0 = np.array([0, 1])
    x, info, pfExitFlag, msg = fsolve(
        lambda x: pf_func_ibr_infinite(x, parasIBR),
        x0,
        xtol=1e-6,  # Tolerance for termination
        maxfev=500,  # Maximum number of function evaluations
        full_output=True
    )
    w, V1, V2, I = pf_calc_infinite(x, parasIBR)
    # Steady-State Values
    steadyStateValuesX, steadyStateValuesU = steadystatevalue_droop(w, V2, I, parasIBR)
    # Small-signal Modeling
    stateMatrix = ssmodel_droop(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, 0)
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

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag