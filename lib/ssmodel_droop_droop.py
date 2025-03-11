#DONT TOUCH
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
    opts = {'xtol': 1e-6, 'maxfev': 500, 'factor': 0.1}
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibr_ibr(x, parasIBR1, parasIBR2, parasLoad),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier

    # Power flow calculations
    w, V1, V2, V3, Io1, Io2 = pf_calc_ibr_ibr(x, parasIBR1, parasIBR2)

    # Steady-State Values
    steadyStateValuesX1, steadyStateValuesU1 = steadystatevalue_droop(w, V1, Io1, parasIBR1)
    steadyStateValuesX2, steadyStateValuesU2 = steadystatevalue_droop(w, V2, Io2, parasIBR2)
    steadyStateValuesXLoad, steadyStateValuesULoad = steadystatevalue_load(w, V3, parasLoad)

    # Combine steady-state values (if needed elsewhere)
    steadyStateValuesX = np.concatenate((steadyStateValuesX1, steadyStateValuesX2, steadyStateValuesXLoad))

    # Small-signal Modeling
    stateMatrix1 = ssmodel_droop(wbase, parasIBR1, steadyStateValuesX1, steadyStateValuesU1, 1)
    stateMatrix2 = ssmodel_droop(wbase, parasIBR2, steadyStateValuesX2, steadyStateValuesU2, 0)
    stateMatrixLoad = ssmodel_load(wbase, parasLoad, steadyStateValuesXLoad, steadyStateValuesULoad)

    # Retrieve state-space matrices
    A1, B1, Bw1, C1, Cw1 = stateMatrix1['A'], stateMatrix1['B'], stateMatrix1['Bw'], stateMatrix1['C'], stateMatrix1['Cw']
    A2, B2, Bw2, C2 = stateMatrix2['A'], stateMatrix2['B'], stateMatrix2['Bw'], stateMatrix2['C']
    Aload, Bload, Bloadw = stateMatrixLoad['A'], stateMatrixLoad['B'], stateMatrixLoad['Bw']

    Rx = parasLoad['Rx']
    Ngen1 = Rx * np.array([[1, 0], [0, 1]])
    Ngen2 = Rx * np.array([[1, 0], [0, 1]])
    Nload = -Rx * np.array([[1, 0], [0, 1]])

    # Construct the overall system matrix.
    block11 = A1 + Bw1 @ Cw1.T + B1 @ Ngen1 @ C1  # (13, 13): Bw1 (13,1)@(1,13) = (13,13)
    block12 = B1 @ Ngen2 @ C2  # (13, 2)@(2,2)@(2,13) = (13, 13)
    block13 = B1 @ Nload  # (13, 2)@(2,2) = (13, 2)

    block21 = Bw2 @ Cw1.T + B2 @ Ngen1 @ C1  # (13,1)@(1,13) + (13,2)@(2,2)@(2,13) = (13, 13)
    block22 = A2 + B2 @ Ngen2 @ C2  # (13, 13) + (13,2)@(2,2)@(2,13) = (13, 13)
    block23 = B2 @ Nload  # (13, 2)@(2,2) = (13, 2)

    block31 = Bloadw @ Cw1.T + Bload @ Ngen1 @ C1  # (2,1)@(1,13) + (2,2)@(2,2)@(2,13) = (2, 13)
    block32 = Bload @ Ngen2 @ C2  # (2,2)@(2,2)@(2,13) = (2, 13)
    block33 = Aload + Bload @ Nload  # (2,2) + (2,2)@(2,2) = (2, 2)

    # Assemble the full system matrix (Asys_full) as a block matrix.
    row1 = np.hstack([block11, block12, block13])  # (13, 28)
    row2 = np.hstack([block21, block22, block23])  # (13, 28)
    row3 = np.hstack([block31, block32, block33])  # (2, 28)
    Asys = np.vstack([row1, row2, row3])  # (28, 28)

    # Combine state variables from the three models.
    ssVariables = np.concatenate((stateMatrix1['ssVariables'], stateMatrix2['ssVariables'], stateMatrixLoad['ssVariables']))
    if len(ssVariables.shape) == 1:
        ssVariables = ssVariables.reshape(-1, 1)

    labels = (['IBR1'] * len(stateMatrix1['ssVariables']) +
              ['IBR2'] * len(stateMatrix2['ssVariables']) +
              ['Load'] * len(stateMatrixLoad['ssVariables']))
    ssVariables = np.column_stack((ssVariables, np.array(labels, dtype=object)))

    # Remove the first row/column to mimic MATLAB's offset indexing.
    Asys = Asys[1:, 1:]
    ssVariables = ssVariables[1:, :]

    # Eigenvalue Analysis
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag