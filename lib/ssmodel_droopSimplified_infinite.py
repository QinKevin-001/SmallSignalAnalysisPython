import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibr_infinite import pf_func_ibr_infinite
from lib.pf_calc_infinite import pf_calc_infinite
from lib.steadystatevalue_droopSimplified import steadystatevalue_droopSimplified
from lib.ssmodel_droopSimplified import ssmodel_droopSimplified
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_droopSimplified_infinite(wbase, parasIBR, dominantParticipationFactorBoundary):
    # Power Flow Calculation
    x0 = np.array([0, 1])
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibr_infinite(x, parasIBR),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier
    w, V1, V2, I = pf_calc_infinite(x, parasIBR)
    steadyStateValuesX, steadyStateValuesU = steadystatevalue_droopSimplified(w, V2, I, parasIBR)
    stateMatrix = ssmodel_droopSimplified(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, 0)
    Asys = stateMatrix['A']
    ssVariables = stateMatrix['ssVariables']
    if isinstance(ssVariables, list):
        new_ssVariables = []
        for var in ssVariables:
            if isinstance(var, str):
                new_ssVariables.append([var, "IBR"])
            elif isinstance(var, list) or isinstance(var, tuple):
                new_ssVariables.append([var[0], "IBR"])
            else:
                raise TypeError("Element of ssVariables is not a string or list/tuple")
        ssVariables = new_ssVariables
    elif isinstance(ssVariables, np.ndarray):
        ssVariables = ssVariables.tolist()
        ssVariables = [[row[0], "IBR"] for row in ssVariables]
    else:
        raise TypeError("Unsupported type for ssVariables")
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag