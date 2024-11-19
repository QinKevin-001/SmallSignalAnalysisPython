import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibrPlant_infinite import pf_func_ibrPlant_infinite
from lib.pf_calc_infinite import pf_calc_infinite
from lib.steadystatevalue_droopPlant import steadystatevalue_droopPlant
from lib.ssmodel_droopPlant import ssmodel_droopPlant
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_droopPlant_infinite(wbase, parasIBR, dominantParticipationFactorBoundary):
    # Power Flow Calculation
    x0 = np.array([0, 1])
    opts = {'maxfev': 1000}  # Removed 'disp'

    # Use pf_func_ibrPlant_infinite for fsolve
    x, infodict, pfExitFlag, msg = fsolve(lambda x: pf_func_ibrPlant_infinite(x, parasIBR), x0, full_output=True, **opts)

    # Check if fsolve succeeded
    if pfExitFlag != 1:
        raise ValueError(f"fsolve failed: {msg}")

    w, V1, V2, I = pf_calc_infinite(x, parasIBR)

    # Steady-State Values
    steadyStateValuesX, steadyStateValuesU = steadystatevalue_droopPlant(w, V1, I, parasIBR)

    # Small-signal Modeling
    stateMatrix = ssmodel_droopPlant(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, 0)
    Asys = stateMatrix['A']
    ssVariables = stateMatrix['ssVariables']
    ssVariables = ['IBR'] * 20

    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag