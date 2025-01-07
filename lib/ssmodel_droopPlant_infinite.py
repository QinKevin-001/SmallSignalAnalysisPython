#Test confirmed

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
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibrPlant_infinite(x, parasIBR),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier # fsolve exit flag

    # Power flow calculations
    w, V1, V2, I = pf_calc_infinite(x, parasIBR)

    # Steady-State Values
    steadyStateValuesX, steadyStateValuesU = steadystatevalue_droopPlant(w, V1, I, parasIBR)

    # Small-signal Modeling
    stateMatrix = ssmodel_droopPlant(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, 0)
    Asys = stateMatrix['A']
    ssVariables = stateMatrix['ssVariables']

    # Assigning labels to the state variables
    if isinstance(ssVariables, list):
        # Convert to a mutable list of lists
        ssVariables = [list(row) for row in ssVariables]
        for row in ssVariables:
            row[1] = 'IBR'
    elif isinstance(ssVariables, np.ndarray):
        # If it's a NumPy array, modify it directly
        ssVariables[:, 1] = ['IBR'] * ssVariables.shape[0]
    else:
        raise TypeError("Unsupported type for ssVariables")

    # Eigenvalue Analysis
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag