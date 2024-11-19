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
    opts = {'method': 'lm', 'disp': False}
    x, infodict, pfExitFlag, msg = fsolve(lambda x: pf_func_ibr_infinite(x, parasIBR), x0, full_output=True, **opts)
    w, V1, V2, I = pf_calc_infinite(x, parasIBR)

    # Steady-State Values
    steadyStateValuesX, steadyStateValuesU = steadystatevalue_droopSimplified(w, V2, I, parasIBR)

    # Small-signal Modeling
    stateMatrix = ssmodel_droopSimplified(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, 0)
    Asys = stateMatrix['A']
    ssVariables = stateMatrix['ssVariables']
    ssVariables[:, 1] = ['IBR'] * 5

    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag
