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

    ## **State Variable Labels**
    # Helper: force any array into a column vector (flattening any extra dimensions)
    def ensure_column(x):  # Convert input to a column vector containing all elements
        arr = np.array(x)
        return arr.flatten().reshape(-1, 1)

    ssVar1 = ensure_column(stateMatrix1['ssVariables'])  # IBR1 state variables as column vector
    ssVar2 = ensure_column(stateMatrix2['ssVariables'])  # IBR2 state variables as column vector
    ssVarLoad = ensure_column(stateMatrixLoad['ssVariables'])  # Load state variables as column vector
    ssVariables = np.concatenate([ssVar1, ssVar2, ssVarLoad], axis=0)  # (TotalStates,1): Concatenate all state variables

    labels = (  # Create a list of labels corresponding to each state variable
            ['IBR1'] * ssVar1.shape[0] +
            ['IBR2'] * ssVar2.shape[0] +
            ['Load'] * ssVarLoad.shape[0]
    )
    ssVariables = np.column_stack((ssVariables, np.array(labels, dtype=object)))

    # Remove the first row/column to mimic MATLAB's offset indexing.
    Asys = Asys[1:, 1:]
    ssVariables = ssVariables[1:, :]

    # Eigenvalue Analysis
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag