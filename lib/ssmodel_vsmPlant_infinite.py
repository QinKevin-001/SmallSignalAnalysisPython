#DONT TOUCH
import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibrPlant_infinite import pf_func_ibrPlant_infinite
from lib.pf_calc_infinite import pf_calc_infinite
from lib.steadystatevalue_vsmPlant import steadystatevalue_vsmPlant
from lib.ssmodel_vsmPlant import ssmodel_vsmPlant
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_vsmPlant_infinite(wbase, parasIBR, dominantParticipationFactorBoundary):
    # Power Flow Calculation
    x0 = np.array([0, 1])
    opts = {'xtol': 1e-6, 'maxfev': 500, 'factor': 0.1}  # Levenberg-Marquardt equivalent options
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibrPlant_infinite(x, parasIBR),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier  # fsolve exit flag

    # Power flow calculations
    w, V1, V2, I = pf_calc_infinite(x, parasIBR)

    # Steady-State Values:
    # Note: In the MATLAB code the voltage V1 is passed to steadystatevalue_vsmPlant.
    # Here we correct the Python version to use V1 (not V2) to match the MATLAB behavior.
    steadyStateValuesX, steadyStateValuesU = steadystatevalue_vsmPlant(w, V1, I, parasIBR)

    # Small-signal Modeling
    stateMatrix = ssmodel_vsmPlant(wbase, parasIBR, steadyStateValuesX, steadyStateValuesU, 0)
    Asys = stateMatrix['A']
    ssVariables = stateMatrix['ssVariables']

    # Properly convert state variable names into a two-column list:
    # Each state variable is paired with the label 'IBR'.
    ssVariables = [[sv, 'IBR'] for sv in ssVariables]

    # Eigenvalue Analysis
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag