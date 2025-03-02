#DONT TOUCH
import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibrPlant_infinite import pf_func_ibrPlant_infinite
from lib.pf_calc_infinite import pf_calc_infinite
from lib.steadystatevalue_gflPlant import steadystatevalue_gflPlant
from lib.ssmodel_gflPlant import ssmodel_gflPlant
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_gflPlant_infinite(wbase, parasIBR, dominantParticipationFactorBoundary):
    # Power Flow Calculation
    x0 = np.array([0, 1])
    opts = {'xtol': 1e-6, 'maxfev': 500}  # Levenberg-Marquardt equivalent options
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibrPlant_infinite(x, parasIBR),
        x0,
        xtol=opts['xtol'],
        maxfev=opts['maxfev'],
        full_output=True
    )
    pfExitFlag = ier  # fsolve exit flag

    # Power Flow Calculations
    w, V1, V2, I = pf_calc_infinite(x, parasIBR)

    # Steady-State Values
    steadyStateValuesX, steadyStateValuesU = steadystatevalue_gflPlant(w, V1, I, parasIBR)

    # Small-Signal Modeling
    stateMatrix = ssmodel_gflPlant(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, 0)
    Asys = stateMatrix['A']
    ssVariables = stateMatrix['ssVariables']

    # Assigning labels to the state variables
    if isinstance(ssVariables, list):
        ssVariables = [list(row) for row in ssVariables]  # Convert to a mutable list of lists
        for row in ssVariables:
            row[1] = 'IBR'
    elif isinstance(ssVariables, np.ndarray):
        ssVariables[:, 1] = ['IBR'] * ssVariables.shape[0]
    else:
        raise TypeError("Unsupported type for ssVariables")

    # Eigenvalue Analysis
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag
