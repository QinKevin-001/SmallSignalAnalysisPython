import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibr_ibr import pf_func_ibr_ibr
from lib.pf_calc_ibr_ibr import pf_calc_ibr_ibr
from lib.steadystatevalue_droop import steadystatevalue_droop
from lib.steadystatevalue_load import steadystatevalue_load
from lib.ssmodel_droop import ssmodel_droop
from lib.ssmodel_load import ssmodel_load
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_droop_droop(wbase, parasIBR1, parasIBR2, parasLoad, dominantParticipationFactorBoundary):
    # Power Flow Calculation
    x0 = np.array([1, 0, 0, 1, 1, 1])
    opts = {'xtol': 1e-6, 'maxfev': 500, 'factor': 0.1}  # Levenberg-Marquardt equivalent options
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibr_ibr(x, parasIBR1, parasIBR2, parasLoad),
        x0,
        xtol=1e-6,  # Tolerance for termination
        maxfev=500,  # Maximum number of function evaluations
        full_output=True
    )
    pfExitFlag = ier  # fsolve exit flag

    # Power flow calculations
    w, V1, V2, V3, Io1, Io2 = pf_calc_ibr_ibr(x, parasIBR1, parasIBR2)

    # Steady-State Values
    steadyStateValuesX1, steadyStateValuesU1 = steadystatevalue_droop(w, V1, Io1, parasIBR1)
    steadyStateValuesX2, steadyStateValuesU2 = steadystatevalue_droop(w, V2, Io2, parasIBR2)
    steadyStateValuesXLoad, steadyStateValuesULoad = steadystatevalue_load(w, V3, parasLoad)

    # Combine steady-state values
    steadyStateValuesX = np.concatenate((steadyStateValuesX1, steadyStateValuesX2, steadyStateValuesXLoad))

    # Small-signal Modeling
    stateMatrix1 = ssmodel_droop(wbase, parasIBR1, steadyStateValuesX1, steadyStateValuesU1, 1)
    stateMatrix2 = ssmodel_droop(wbase, parasIBR2, steadyStateValuesX2, steadyStateValuesU2, 0)
    stateMatrixLoad = ssmodel_load(wbase, parasLoad, steadyStateValuesXLoad, steadyStateValuesULoad)

    A1, B1, Bw1, C1, Cw1 = stateMatrix1['A'], stateMatrix1['B'], stateMatrix1['Bw'], stateMatrix1['C'], stateMatrix1['Cw']
    A2, B2, Bw2, C2 = stateMatrix2['A'], stateMatrix2['B'], stateMatrix2['Bw'], stateMatrix2['C']
    Aload, Bload, Bloadw = stateMatrixLoad['A'], stateMatrixLoad['B'], stateMatrixLoad['Bw']

    Rx = parasLoad['Rx']
    Ngen1 = Rx * np.array([[1, 0], [0, 1]])
    Ngen2 = Rx * np.array([[1, 0], [0, 1]])
    Nload = -Rx * np.array([[1, 0], [0, 1]])

    # Construct the overall system matrix
    Asys = np.block([
        [A1 + Bw1 * Cw1 + B1 * Ngen1 * C1, B1 * Ngen2 * C2, B1 * Nload],
        [Bw2 * Cw1 + B2 * Ngen1 * C1, A2 + B2 * Ngen2 * C2, B2 * Nload],
        [Bloadw * Cw1 + Bload * Ngen1 * C1, Bload * Ngen2 * C2, Aload + Bload * Nload]
    ])

    # Combine state variables
    ssVariables = np.concatenate((stateMatrix1['ssVariables'], stateMatrix2['ssVariables'], stateMatrixLoad['ssVariables']))

    # Assign IBR1, IBR2, and Load labels
    ssVariables = np.array(ssVariables, dtype=object)
    ssVariables[:, 1] = [
        'IBR1'] * len(stateMatrix1['ssVariables']) + [
        'IBR2'] * len(stateMatrix2['ssVariables']) + [
        'Load'] * len(stateMatrixLoad['ssVariables'])

    # Remove first row/column from system matrix and variables (consistent with MATLAB version)
    Asys = Asys[1:, 1:]
    ssVariables = ssVariables[1:, :]

    # Eigenvalue Analysis
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag
