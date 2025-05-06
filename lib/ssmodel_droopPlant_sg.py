import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibrPlant_sg import pf_func_ibrPlant_sg
from lib.pf_calc_ibrPlant_sg import pf_calc_ibrPlant_sg
from lib.steadystatevalue_droopPlant import steadystatevalue_droopPlant
from lib.steadystatevalue_sg import steadystatevalue_sg
from lib.steadystatevalue_line import steadystatevalue_line
from lib.steadystatevalue_load import steadystatevalue_load
from lib.ssmodel_droopPlant import ssmodel_droopPlant
from lib.ssmodel_sg import ssmodel_sg
from lib.ssmodel_line import ssmodel_line
from lib.ssmodel_load import ssmodel_load
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_droopPlant_sg(wbase, parasIBR, parasSG, parasLine1, parasLine2, parasLoad, dominantParticipationFactorBoundary):
    ## Power Flow Calculation
    x0 = np.array([1, 0, 0, 0, 1, 1, 1, 1])
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibrPlant_sg(x, parasIBR, parasSG, parasLine1, parasLine2, parasLoad),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier
    w, V1, V2, V3, Io1, Io2 = pf_calc_ibrPlant_sg(x, parasLine1, parasLine2, parasLoad)
    steadyStateValuesX1, steadyStateValuesU1 = steadystatevalue_droopPlant(w, V1, Io1, parasIBR)
    steadyStateValuesX2, steadyStateValuesU2 = steadystatevalue_sg(w, V2, Io2, parasSG)
    steadyStateValuesXLine1, steadyStateValuesULine1 = steadystatevalue_line(w, V1, V3, parasLine1)
    steadyStateValuesXLine2, steadyStateValuesULine2 = steadystatevalue_line(w, V2, V3, parasLine2)
    steadyStateValuesXLoad, steadyStateValuesULoad = steadystatevalue_load(w, V3, parasLoad)
    steadyStateValuesX = np.concatenate([
        steadyStateValuesX1,
        steadyStateValuesX2,
        steadyStateValuesXLine1,
        steadyStateValuesXLine2,
        steadyStateValuesXLoad
    ])
    stateMatrix1 = ssmodel_droopPlant(wbase, parasIBR, steadyStateValuesX1, steadyStateValuesU1, 1)
    stateMatrix2 = ssmodel_sg(wbase, parasSG, steadyStateValuesX2, steadyStateValuesU2, 0)
    stateMatrixLine1 = ssmodel_line(wbase, parasLine1, steadyStateValuesXLine1, steadyStateValuesULine1)
    stateMatrixLine2 = ssmodel_line(wbase, parasLine2, steadyStateValuesXLine2, steadyStateValuesULine2)
    stateMatrixLoad = ssmodel_load(wbase, parasLoad, steadyStateValuesXLoad, steadyStateValuesULoad)

    # Extract matrices from state-space models (sizes as provided)
    A1   = stateMatrix1['A']
    B1   = stateMatrix1['B']
    Bw1  = stateMatrix1['Bw']
    C1   = stateMatrix1['C']
    Cw1  = stateMatrix1['Cw']

    A2   = stateMatrix2['A']
    B2   = stateMatrix2['B']
    Bw2  = stateMatrix2['Bw']
    C2   = stateMatrix2['C']

    Aline1   = stateMatrixLine1['A']
    B1line1  = stateMatrixLine1['B1']
    B2line1  = stateMatrixLine1['B2']
    Bwline1  = stateMatrixLine1['Bw']

    Aline2   = stateMatrixLine2['A']
    B1line2  = stateMatrixLine2['B1']
    B2line2  = stateMatrixLine2['B2']
    Bwline2  = stateMatrixLine2['Bw']

    Aload   = stateMatrixLoad['A']
    Bload   = stateMatrixLoad['B']
    Bwload  = stateMatrixLoad['Bw']

    Rx = parasLoad['Rx'] if isinstance(parasLoad, dict) else parasLoad.Rx
    Ngen1    = Rx * np.eye(2)
    Nline1Gen = -Rx * np.eye(2)
    Ngen2    = Rx * np.eye(2)
    Nline2Gen = -Rx * np.eye(2)
    Nline1Load = Rx * np.eye(2)
    Nline2Load = Rx * np.eye(2)
    Nload    = -Rx * np.eye(2)
    # Row 1: 14 rows, blocks:
    row1 = np.hstack([
        A1 + Bw1 @ Cw1 + B1 @ Ngen1 @ C1,
        np.zeros((22, 14)),
        B1 @ Nline1Gen,
        np.zeros((22, 2)),
        np.zeros((22, 2))
    ])
    # Row 2: 14 rows, blocks:
    row2 = np.hstack([
        Bw2 @ Cw1,
        A2 + B2 @ Ngen2 @ C2,
        np.zeros((14, 2)),
        B2 @ Nline2Gen,
        np.zeros((14, 2))
    ])
    # Row 3: 2 rows, blocks:
    row3 = np.hstack([
        Bwline1 @ Cw1 + B1line1 @ Ngen1 @ C1,
        np.zeros((2, 14)),
        Aline1 + B1line1 @ Nline1Gen + B2line1 @ Nline1Load,
        B2line1 @ Nline2Load,
        B2line1 @ Nload
    ])
    # Row 4: 2 rows, blocks:
    row4 = np.hstack([
        Bwline2 @ Cw1,
        B1line2 @ Ngen2 @ C2,
        B2line2 @ Nline1Load,
        Aline2 + B1line2 @ Nline2Gen + B2line2 @ Nline2Load,
        B2line2 @ Nload
    ])
    # Row 5: 2 rows, blocks:
    row5 = np.hstack([
        Bwload @ Cw1,
        np.zeros((2, 14)),
        Bload @ Nline1Load,
        Bload @ Nline2Load,
        Aload + Bload @ Nload
    ])
    Asys = np.vstack([row1, row2, row3, row4, row5])
    ssVar1    = np.array(stateMatrix1['ssVariables']).flatten()
    ssVar2    = np.array(stateMatrix2['ssVariables']).flatten()
    ssVarLine1 = np.array(stateMatrixLine1['ssVariables']).flatten()
    ssVarLine2 = np.array(stateMatrixLine2['ssVariables']).flatten()
    ssVarLoad  = np.array(stateMatrixLoad['ssVariables']).flatten()
    labels = (['IBR1'] * len(ssVar1) +
              ['SG1'] * len(ssVar2) +
              ['Line1'] * len(ssVarLine1) +
              ['Line2'] * len(ssVarLine2) +
              ['Load'] * len(ssVarLoad))
    ssVariables = np.column_stack((
        np.concatenate([ssVar1, ssVar2, ssVarLine1, ssVarLine2, ssVarLoad]),
        np.array(labels, dtype=object)
    ))
    Asys = np.delete(Asys, 9, axis=0)   # Remove row with index 9 (10th row)
    Asys = np.delete(Asys, 9, axis=1)   # Remove column with index 9 (10th column)
    ssVariables = np.delete(ssVariables, 9, axis=0)
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag
