# DONT TOUCH
import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibr_sg import pf_func_ibr_sg
from lib.pf_calc_ibr_sg import pf_calc_ibr_sg
from lib.steadystatevalue_droop import steadystatevalue_droop
from lib.steadystatevalue_sg import steadystatevalue_sg
from lib.steadystatevalue_line import steadystatevalue_line
from lib.steadystatevalue_load import steadystatevalue_load
from lib.ssmodel_droop import ssmodel_droop
from lib.ssmodel_sg import ssmodel_sg
from lib.ssmodel_line import ssmodel_line
from lib.ssmodel_load import ssmodel_load
from lib.eigenvalue_analysis import eigenvalue_analysis


def ssmodel_droop_sg(wbase, parasIBR, parasSG, parasLineSG, parasLoad, dominantParticipationFactorBoundary):
    ## Power Flow Calculation
    x0 = np.array([1, 0, 0, 1, 1, 1])
    # Define parasLine1 and parasLine2 based on input parameters
    parasLine1 = {}
    if isinstance(parasIBR, dict):
        parasLine1['Rline'] = parasIBR['Rc']
        parasLine1['Lline'] = parasIBR['Lc']
    else:
        parasLine1['Rline'] = parasIBR.Rc
        parasLine1['Lline'] = parasIBR.Lc

    parasLine2 = {}
    if isinstance(parasLineSG, dict):
        parasLine2['Rline'] = parasLineSG['Rline']
        parasLine2['Lline'] = parasLineSG['Lline']
    else:
        parasLine2['Rline'] = parasLineSG.Rline
        parasLine2['Lline'] = parasLineSG.Lline

    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibr_sg(x, parasIBR, parasSG, parasLine1, parasLine2, parasLoad),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier  # Convergence status

    # Calculate Power Flow outputs
    w, V1, V2, V3, Io1, Io2 = pf_calc_ibr_sg(x, parasLine1, parasLine2, parasLoad)

    ## Steady-State Values
    steadyStateValuesX1, steadyStateValuesU1 = steadystatevalue_droop(w, V1, Io1, parasIBR)
    steadyStateValuesX2, steadyStateValuesU2 = steadystatevalue_sg(w, V2, Io2, parasSG)
    steadyStateValuesXLine, steadyStateValuesULine = steadystatevalue_line(w, V2, V3, parasLineSG)
    steadyStateValuesXLoad, steadyStateValuesULoad = steadystatevalue_load(w, V3, parasLoad)
    steadyStateValuesX = np.concatenate([
        steadyStateValuesX1,
        steadyStateValuesX2,
        steadyStateValuesXLine,
        steadyStateValuesXLoad
    ])

    ## Small-signal Modeling
    stateMatrix1 = ssmodel_droop(wbase, parasIBR, steadyStateValuesX1, steadyStateValuesU1, 1)
    stateMatrix2 = ssmodel_sg(wbase, parasSG, steadyStateValuesX2, steadyStateValuesU2, 0)
    stateMatrixLine = ssmodel_line(wbase, parasLineSG, steadyStateValuesXLine, steadyStateValuesULine)
    stateMatrixLoad = ssmodel_load(wbase, parasLoad, steadyStateValuesXLoad, steadyStateValuesULoad)

    # Extract matrices from state-space models
    # Expected dimensions (from printed sizes):
    # stateMatrix1: A1 (13,13), B1 (13,2), Bw1 (13,1), C1 (2,13), Cw1 (13,1)
    A1   = stateMatrix1['A']
    B1   = stateMatrix1['B']
    Bw1  = stateMatrix1['Bw']
    C1   = stateMatrix1['C']
    Cw1  = stateMatrix1['Cw']

    # stateMatrix2: A2 (14,14), B2 (14,2), Bw2 (14,1), C2 (2,14)
    A2   = stateMatrix2['A']
    B2   = stateMatrix2['B']
    Bw2  = stateMatrix2['Bw']
    C2   = stateMatrix2['C']

    # stateMatrixLine: Aline (2,2), B1line (2,2), B2line (2,2), Bwline (2,1)
    Aline   = stateMatrixLine['A']
    B1line  = stateMatrixLine['B1']
    B2line  = stateMatrixLine['B2']
    Bwline  = stateMatrixLine['Bw']

    # stateMatrixLoad: Aload (2,2), Bload (2,2), Bwload (2,1)
    Aload   = stateMatrixLoad['A']
    Bload   = stateMatrixLoad['B']
    Bwload  = stateMatrixLoad['Bw']

    # Define coupling matrices based on parasLoad parameters
    Rx = parasLoad['Rx'] if isinstance(parasLoad, dict) else parasLoad.Rx
    Ngen1   = Rx * np.eye(2)
    Nline1  = Rx * np.eye(2)
    Nload   = -Rx * np.eye(2)
    Ngen2   = Rx * np.eye(2)
    Nline2  = -Rx * np.eye(2)

    # Assemble the overall system matrix Asys using block matrices.
    # Use .T on Cw matrices to ensure conformable multiplication.
    # Row 1 (13 rows; columns: 13 + 14 + 2 + 2 = 31)
    row1 = np.hstack([
        A1 + Bw1 @ Cw1.T + B1 @ Ngen1 @ C1,    # (13,13)
        np.zeros((13, 14)),                    # (13,14)
        B1 @ Nline1,                           # (13,2)
        B1 @ Nload                             # (13,2)
    ])
    # Row 2 (14 rows; 31 columns)
    row2 = np.hstack([
        Bw2 @ Cw1.T,                           # (14,13)
        A2 + B2 @ Ngen2 @ C2,                   # (14,14)
        B2 @ Nline2,                           # (14,2)
        np.zeros((14, 2))                       # (14,2)
    ])
    # Row 3 (2 rows; 31 columns)
    row3 = np.hstack([
        Bwline @ Cw1.T + B2line @ Ngen1 @ C1,    # (2,13)
        B1line @ Ngen2 @ C2,                     # (2,14)
        Aline + B2line @ Nline1 + B1line @ Nline2, # (2,2)
        B2line @ Nload                          # (2,2)
    ])
    # Row 4 (2 rows; 31 columns)
    row4 = np.hstack([
        Bwload @ Cw1.T + Bload @ Ngen1 @ C1,     # (2,13)
        np.zeros((2, 14)),                      # (2,14)
        Bload @ Nline1,                         # (2,2)
        Aload + Bload @ Nload                    # (2,2)
    ])

    Asys = np.vstack([row1, row2, row3, row4])
    # Asys dimensions before deletion: (13+14+2+2, 31) = (31,31)

    ## State Variable Labels
    ssVar1    = np.array(stateMatrix1['ssVariables']).flatten()
    ssVar2    = np.array(stateMatrix2['ssVariables']).flatten()
    ssVarLine = np.array(stateMatrixLine['ssVariables']).flatten()
    ssVarLoad = np.array(stateMatrixLoad['ssVariables']).flatten()

    # Build labels dynamically to match the actual state variable lengths:
    labels = (['IBR1'] * len(ssVar1) +
              ['SG1'] * len(ssVar2) +
              ['LineSG'] * len(ssVarLine) +
              ['Load'] * len(ssVarLoad))
    ssVariables = np.column_stack((
        np.concatenate([ssVar1, ssVar2, ssVarLine, ssVarLoad]),
        np.array(labels, dtype=object)
    ))
    # Remove the first row and first column from Asys and remove the corresponding state variable label
    Asys = Asys[1:, 1:]
    ssVariables = np.delete(ssVariables, 0, axis=0)

    ## Eigenvalue Analysis
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag
