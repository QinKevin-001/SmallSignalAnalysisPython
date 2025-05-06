import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibrPlant_infinite import pf_func_ibrPlant_infinite
from lib.pf_calc_infinite import pf_calc_infinite
from lib.steadystatevalue_vsmPlant import steadystatevalue_vsmPlant
from lib.ssmodel_vsmPlant import ssmodel_vsmPlant
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_vsmPlant_infinite(wbase, parasIBR, dominantParticipationFactorBoundary):
    x0 = np.array([0, 1])
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibrPlant_infinite(x, parasIBR),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier
    w, V1, V2, I = pf_calc_infinite(x, parasIBR)
    steadyStateValuesX, steadyStateValuesU = steadystatevalue_vsmPlant(w, V1, I, parasIBR)

    # Small-signal Modeling
    stateMatrix = ssmodel_vsmPlant(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, 0)
    Asys = stateMatrix['A']
    ssVariables = stateMatrix['ssVariables']
    ssVariables = [[sv, 'IBR'] for sv in ssVariables]
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag