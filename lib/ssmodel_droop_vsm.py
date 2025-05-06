import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibr_ibr import pf_func_ibr_ibr
from lib.pf_calc_ibr_ibr import pf_calc_ibr_ibr
from lib.steadystatevalue_droop import steadystatevalue_droop
from lib.steadystatevalue_vsm import steadystatevalue_vsm
from lib.steadystatevalue_load import steadystatevalue_load
from lib.ssmodel_droop import ssmodel_droop
from lib.ssmodel_vsm import ssmodel_vsm
from lib.ssmodel_load import ssmodel_load
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_droop_vsm(wbase, parasIBR1, parasIBR2, parasLoad, dominantParticipationFactorBoundary):
    # Power Flow Calculation
    x0 = np.array([1, 0, 0, 1, 1, 1])  # Initial condition
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibr_ibr(x, parasIBR1, parasIBR2, parasLoad),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier
    w, V1, V2, V3, Io1, Io2 = pf_calc_ibr_ibr(x, parasIBR1, parasIBR2)
    # Steady-State Values
    steadyStateValuesX1, steadyStateValuesU1 = steadystatevalue_droop(w, V1, Io1, parasIBR1)
    steadyStateValuesX2, steadyStateValuesU2 = steadystatevalue_vsm(w, V2, Io2, parasIBR2)
    steadyStateValuesXLoad, steadyStateValuesULoad = steadystatevalue_load(w, V3, parasLoad)
    steadyStateValuesX = np.concatenate((steadyStateValuesX1, steadyStateValuesX2, steadyStateValuesXLoad))
    # Small-signal Modeling
    stateMatrix1 = ssmodel_droop(wbase, parasIBR1, steadyStateValuesX1, steadyStateValuesU1, 1)
    stateMatrix2 = ssmodel_vsm(wbase, parasIBR2, steadyStateValuesX2, steadyStateValuesU2, 0)
    stateMatrixLoad = ssmodel_load(wbase, parasLoad, steadyStateValuesXLoad, steadyStateValuesULoad)
    A1, B1, Bw1, C1, Cw1 = stateMatrix1['A'], stateMatrix1['B'], stateMatrix1['Bw'], stateMatrix1['C'], stateMatrix1[
        'Cw']
    A2, B2, Bw2, C2 = stateMatrix2['A'], stateMatrix2['B'], stateMatrix2['Bw'], stateMatrix2['C']
    Aload, Bload, Bloadw = stateMatrixLoad['A'], stateMatrixLoad['B'], stateMatrixLoad['Bw']
    Rx = parasLoad['Rx']
    Ngen1 = Rx * np.array([[1, 0], [0, 1]])
    Ngen2 = Rx * np.array([[1, 0], [0, 1]])
    Nload = -Rx * np.array([[1, 0], [0, 1]])

    # Construct system matrix
    # Row 1 (IBR1)
    row1_block1 = A1 + Bw1 @ Cw1.T + B1 @ Ngen1 @ C1
    row1_block2 = B1 @ Ngen2 @ C2
    row1_block3 = B1 @ Nload
    row1 = np.hstack([row1_block1, row1_block2, row1_block3])

    # Row 2 (IBR2)
    row2_block1 = Bw2 @ Cw1.T + B2 @ Ngen1 @ C1
    row2_block2 = A2 + B2 @ Ngen2 @ C2
    row2_block3 = B2 @ Nload
    row2 = np.hstack([row2_block1, row2_block2, row2_block3])

    # Row 3 (Load)
    row3_block1 = Bloadw @ Cw1.T + Bload @ Ngen1 @ C1
    row3_block2 = Bload @ Ngen2 @ C2
    row3_block3 = Aload + Bload @ Nload
    row3 = np.hstack([row3_block1, row3_block2, row3_block3])

    Asys = np.vstack([row1, row2, row3])

    ssVars1 = np.array(stateMatrix1['ssVariables'], dtype=object)
    ssVars2 = np.array(stateMatrix2['ssVariables'], dtype=object)
    ssVarsLoad = np.array(stateMatrixLoad['ssVariables'], dtype=object)

    try:
        # Try direct concatenation first
        ssVariables = np.vstack([ssVars1, ssVars2, ssVarsLoad])
    except ValueError:

        ssVariables = np.empty((13 + 12 + 2, 2), dtype=object)

        if ssVars1.ndim == 2:
            ssVariables[:13, 0] = ssVars1[:, 0]
        else:
            ssVariables[:13, 0] = ssVars1

        if ssVars2.ndim == 2:
            ssVariables[13:25, 0] = ssVars2[:, 0]
        else:
            ssVariables[13:25, 0] = ssVars2

        if ssVarsLoad.ndim == 2:
            ssVariables[25:27, 0] = ssVarsLoad[:, 0]
        else:
            ssVariables[25:27, 0] = ssVarsLoad

    ssVariables[:, 1] = np.array([
        'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1',
        'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2',
        'Load', 'Load'
    ], dtype=object)
    Asys = Asys[1:, 1:]
    ssVariables = ssVariables[1:, :]
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag