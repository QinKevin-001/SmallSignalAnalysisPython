import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibrPlant_infinite import pf_func_ibrPlant_infinite
from lib.pf_calc_infinite import pf_calc_infinite
from lib.steadystatevalue_droopPlant import steadystatevalue_droopPlant
from lib.ssmodel_droopPlant import ssmodel_droopPlant
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_droopPlant_infinite(wbase, parasIBR, dominantParticipationFactorBoundary):
    # Power flow calculation (using fsolve with LM-like options)
    x0 = np.array([0, 1])
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibrPlant_infinite(x, parasIBR),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier

    # Compute power flow results
    w, V1, V2, I = pf_calc_infinite(x, parasIBR)

    # Compute steady-state values (the delay states are computed here)
    steadyStateValuesX, steadyStateValuesU = steadystatevalue_droopPlant(w, V1, I, parasIBR)

    # Build the state-space model (with 22 states)
    stateMatrix = ssmodel_droopPlant(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, 0)
    Asys = stateMatrix['A']
    ssVariables = stateMatrix['ssVariables']
    # Label each state variable for modal analysis
    ssVariables = [[var, 'IBR'] for var in ssVariables]

    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag