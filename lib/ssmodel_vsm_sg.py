import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibr_sg import pf_func_ibr_sg
from lib.pf_calc_ibr_sg import pf_calc_ibr_sg
from lib.steadystatevalue_vsm import steadystatevalue_vsm
from lib.steadystatevalue_sg import steadystatevalue_sg
from lib.steadystatevalue_line import steadystatevalue_line
from lib.steadystatevalue_load import steadystatevalue_load
from lib.ssmodel_vsm import ssmodel_vsm
from lib.ssmodel_sg import ssmodel_sg
from lib.ssmodel_line import ssmodel_line
from lib.ssmodel_load import ssmodel_load
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_vsm_sg(wbase, parasIBR, parasSG, parasLineSG, parasLoad, dominantParticipationFactorBoundary):
    x0 = np.array([1, 0, 0, 1, 1, 1])
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
    pfExitFlag = ier
    w, V1, V2, V3, Io1, Io2 = pf_calc_ibr_sg(x, parasLine1, parasLine2, parasLoad)
    steadyStateValuesX1, steadyStateValuesU1 = steadystatevalue_vsm(w, V1, Io1, parasIBR)
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
    stateMatrix1 = ssmodel_vsm(wbase, parasIBR, steadyStateValuesX1, steadyStateValuesU1, 1)
    stateMatrix2 = ssmodel_sg(wbase, parasSG, steadyStateValuesX2, steadyStateValuesU2, 0)
    stateMatrixLine = ssmodel_line(wbase, parasLineSG, steadyStateValuesXLine, steadyStateValuesULine)
    stateMatrixLoad = ssmodel_load(wbase, parasLoad, steadyStateValuesXLoad, steadyStateValuesULoad)

    # Extract matrices from state-space models with updated dimensions:
    A1 = stateMatrix1['A']
    B1 = stateMatrix1['B']
    Bw1 = stateMatrix1['Bw']
    C1 = stateMatrix1['C']
    Cw1 = stateMatrix1['Cw']

    # SG
    A2 = stateMatrix2['A']
    B2 = stateMatrix2['B']
    Bw2 = stateMatrix2['Bw']
    C2 = stateMatrix2['C']

    # Line (using load matrices for the line model)
    Aline = stateMatrixLine['A']
    B1line = stateMatrixLine['B1']
    B2line = stateMatrixLine['B2']
    Bwline = stateMatrixLine['Bw']

    # Load
    Aload = stateMatrixLoad['A']
    Bload = stateMatrixLoad['B']
    Bwload = stateMatrixLoad['Bw']

    Rx = parasLoad['Rx'] if isinstance(parasLoad, dict) else parasLoad.Rx
    Ngen1 = Rx * np.eye(2)
    Nline1 = Rx * np.eye(2)
    Nload = -Rx * np.eye(2)
    Ngen2 = Rx * np.eye(2)
    Nline2 = -Rx * np.eye(2)

    # Row 1:
    row1 = np.hstack([
        A1 + Bw1 @ Cw1.T + B1 @ Ngen1 @ C1,
        np.zeros((12, 14)),
        B1 @ Nline1,
        B1 @ Nload
    ])
    # Row 2:
    row2 = np.hstack([
        Bw2 @ Cw1.T,
        A2 + B2 @ Ngen2 @ C2,
        B2 @ Nline2,
        np.zeros((14, 2))
    ])
    # Row 3:
    row3 = np.hstack([
        Bwline @ Cw1.T + B2line @ Ngen1 @ C1,
        B1line @ Ngen2 @ C2,
        Aline + B2line @ Nline1 + B1line @ Nline2,
        B2line @ Nload
    ])
    # Row 4:
    row4 = np.hstack([
        Bwload @ Cw1.T + Bload @ Ngen1 @ C1,
        np.zeros((2, 14)),
        Bload @ Nline1,
        Aload + Bload @ Nload
    ])

    Asys = np.vstack([row1, row2, row3, row4])
    Asys = Asys[1:, 1:]
    ssVar1 = np.array(stateMatrix1['ssVariables']).flatten()
    ssVar2 = np.array(stateMatrix2['ssVariables']).flatten()
    ssVarLine = np.array(stateMatrixLine['ssVariables']).flatten()
    ssVarLoad = np.array(stateMatrixLoad['ssVariables']).flatten()
    labels = (['IBR1'] * len(ssVar1) +
              ['SG1'] * len(ssVar2) +
              ['LineSG'] * len(ssVarLine) +
              ['Load'] * len(ssVarLoad))
    ssVariables = np.column_stack((np.concatenate([ssVar1, ssVar2, ssVarLine, ssVarLoad]),
                                   np.array(labels, dtype=object)))
    ssVariables = np.delete(ssVariables, 0, axis=0)
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag
