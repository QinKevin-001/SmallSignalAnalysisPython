# DONT TOUCH
import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibr_ibr import pf_func_ibr_ibr
from lib.pf_calc_ibr_ibr import pf_calc_ibr_ibr
from lib.steadystatevalue_vsm import steadystatevalue_vsm
from lib.steadystatevalue_load import steadystatevalue_load
from lib.ssmodel_vsm import ssmodel_vsm
from lib.ssmodel_load import ssmodel_load
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_vsm_vsm(wbase, parasIBR1, parasIBR2, parasLoad, dominantParticipationFactorBoundary):
    ## Power Flow Calculation
    x0 = np.array([1, 0, 0, 1, 1, 1])  # Initial guess for power flow solution
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibr_ibr(x, parasIBR1, parasIBR2, parasLoad),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier  # Convergence status of fsolve

    # Calculate Power Flow outputs
    w, V1, V2, V3, Io1, Io2 = pf_calc_ibr_ibr(x, parasIBR1, parasIBR2)

    ## Steady-State Values
    steadyStateValuesX1, steadyStateValuesU1 = steadystatevalue_vsm(w, V1, Io1, parasIBR1)
    steadyStateValuesX2, steadyStateValuesU2 = steadystatevalue_vsm(w, V2, Io2, parasIBR2)
    steadyStateValuesXLoad, steadyStateValuesULoad = steadystatevalue_load(w, V3, parasLoad)
    steadyStateValuesX = np.concatenate([steadyStateValuesX1, steadyStateValuesX2, steadyStateValuesXLoad])

    ## Small-signal Modeling
    stateMatrix1 = ssmodel_vsm(wbase, parasIBR1, steadyStateValuesX1, steadyStateValuesU1, 1)
    stateMatrix2 = ssmodel_vsm(wbase, parasIBR2, steadyStateValuesX2, steadyStateValuesU2, 0)
    stateMatrixLoad = ssmodel_load(wbase, parasLoad, steadyStateValuesXLoad, steadyStateValuesULoad)

    # Extract matrices from state-space models
    A1 = stateMatrix1['A']      # (12,12)
    B1 = stateMatrix1['B']      # (12,2)
    Bw1 = stateMatrix1['Bw']    # (12,1)
    C1 = stateMatrix1['C']      # (2,12)
    Cw1 = stateMatrix1['Cw']    # (12,1)

    A2 = stateMatrix2['A']      # (12,12)
    B2 = stateMatrix2['B']      # (12,2)
    Bw2 = stateMatrix2['Bw']    # (12,1)
    C2 = stateMatrix2['C']      # (2,12)

    Aload = stateMatrixLoad['A']    # (2,2)
    Bload = stateMatrixLoad['B']    # (2,2)
    Bloadw = stateMatrixLoad['Bw']  # (2,1)

    # Define coupling matrices based on parasLoad parameters
    Rx = parasLoad['Rx']  # Assuming parasLoad is a dictionary with key 'Rx'
    Ngen1 = Rx * np.eye(2)   # (2,2)
    Ngen2 = Rx * np.eye(2)   # (2,2)
    Nload = -Rx * np.eye(2)  # (2,2)

    # Assemble the overall system matrix Asys using block matrices.
    # Note: We use Cw1.T to ensure conformable multiplication:
    # Bw1 @ Cw1.T: (12,1)@(1,12) -> (12,12), etc.
    block11 = A1 + Bw1 @ Cw1.T + B1 @ Ngen1 @ C1    # (12,12)
    block12 = B1 @ Ngen2 @ C2                         # (12,12)
    block13 = B1 @ Nload                             # (12,2)
    row1 = np.hstack([block11, block12, block13])

    block21 = Bw2 @ Cw1.T + B2 @ Ngen1 @ C1           # (12,12)
    block22 = A2 + B2 @ Ngen2 @ C2                    # (12,12)
    block23 = B2 @ Nload                             # (12,2)
    row2 = np.hstack([block21, block22, block23])

    block31 = Bloadw @ Cw1.T + Bload @ Ngen1 @ C1      # (2,12)
    block32 = Bload @ Ngen2 @ C2                       # (2,12)
    block33 = Aload + Bload @ Nload                    # (2,2)
    row3 = np.hstack([block31, block32, block33])

    Asys = np.vstack([row1, row2, row3])
    # Asys dimensions before deletion: (12+12+2, 12+12+2) = (26,26)

    ## State Variable Labels
    # Convert ssVariables to 1-D arrays and assign labels
    ssVar1 = np.array(stateMatrix1['ssVariables']).flatten()   # Expected length: 12
    ssVar2 = np.array(stateMatrix2['ssVariables']).flatten()   # Expected length: 12
    ssVarLoad = np.array(stateMatrixLoad['ssVariables']).flatten()  # Expected length: 2

    labels = ['IBR1'] * len(ssVar1) + ['IBR2'] * len(ssVar2) + ['Load'] * len(ssVarLoad)
    ssVariables = np.column_stack((np.concatenate([ssVar1, ssVar2, ssVarLoad]), np.array(labels, dtype=object)))
    # ssVariables dimensions before deletion: (26, 2)

    # Remove the first row and column from Asys and the corresponding state variable, as in the MATLAB code.
    Asys = Asys[1:, 1:]           # New shape: (25,25)
    ssVariables = np.delete(ssVariables, 0, axis=0)  # Remove first state label

    ## Eigenvalue Analysis
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag
