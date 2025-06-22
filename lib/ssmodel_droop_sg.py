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
    # Power Flow Calculation
    x0 = np.array([1, 0, 0, 1, 1, 1])
    parasLine1 = {
        'Rline' : parasIBR['Rc'],
        'Lline' : parasIBR['Lc']
    }
    parasLine2 = {
        'Rline' : parasLineSG['Rline'],
        'Lline' : parasLineSG['Lline']
    }
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibr_sg(x, parasIBR, parasSG, parasLine1, parasLine2, parasLoad),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier
    w, V1, V2, V3, Io1, Io2 = pf_calc_ibr_sg(x, parasLine1, parasLine2, parasLoad)
    # Steady-State Values
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
    # Small-signal Modeling
    stateMatrix1 = ssmodel_droop(wbase, parasIBR, steadyStateValuesX1, steadyStateValuesU1, 1)
    stateMatrix2 = ssmodel_sg(wbase, parasSG, steadyStateValuesX2, steadyStateValuesU2, 0)
    stateMatrixLine = ssmodel_line(wbase, parasLineSG, steadyStateValuesXLine, steadyStateValuesULine)
    stateMatrixLoad = ssmodel_load(wbase, parasLoad, steadyStateValuesXLoad, steadyStateValuesULoad)
    A1, B1, Bw1, C1, Cw1 = stateMatrix1['A'], stateMatrix1['B'], stateMatrix1['Bw'], stateMatrix1['C'], stateMatrix1['Cw']
    A2, B2, Bw2, C2 = stateMatrix2['A'], stateMatrix2['B'], stateMatrix2['Bw'], stateMatrix2['C']
    Aline, B1line, B2line, Bwline = stateMatrixLine['A'], stateMatrixLine['B1'], stateMatrixLine['B2'], stateMatrixLine['Bw']
    Aload, Bload, Bwload = stateMatrixLoad['A'], stateMatrixLoad['B'], stateMatrixLoad['Bw']
    Rx = parasLoad['Rx']
    Ngen1   = Rx * np.eye(2)
    Nline1  = Rx * np.eye(2)
    Nload   = -Rx * np.eye(2)
    Ngen2   = Rx * np.eye(2)
    Nline2  = -Rx * np.eye(2)
    # Construct the overall system matrix
    row1 = np.hstack([
        A1 + Bw1 @ Cw1.T + B1 @ Ngen1 @ C1,
        np.zeros((13, 14)),
        B1 @ Nline1,
        B1 @ Nload
    ])
    row2 = np.hstack([
        Bw2 @ Cw1.T,
        A2 + B2 @ Ngen2 @ C2,
        B2 @ Nline2,
        np.zeros((14, 2))
    ])
    row3 = np.hstack([
        Bwline @ Cw1.T + B2line @ Ngen1 @ C1,
        B1line @ Ngen2 @ C2,
        Aline + B2line @ Nline1 + B1line @ Nline2,
        B2line @ Nload
    ])
    row4 = np.hstack([
        Bwload @ Cw1.T + Bload @ Ngen1 @ C1,
        np.zeros((2, 14)),
        Bload @ Nline1,
        Aload + Bload @ Nload
    ])
    Asys = np.vstack([row1, row2, row3, row4])
    # State Variable Labels
    def ensure_column(x):
        arr = np.array(x)
        return arr.flatten().reshape(-1, 1)
    ssVar1 = np.array(stateMatrix1['ssVariables']).flatten()
    ssVar2 = np.array(stateMatrix2['ssVariables']).flatten()
    ssVarLine = np.array(stateMatrixLine['ssVariables']).flatten()
    ssVarLoad = np.array(stateMatrixLoad['ssVariables']).flatten()
    ssVariables = np.concatenate([ssVar1, ssVar2, ssVarLine, ssVarLoad], axis=0)
    labels = (
            ['IBR1'] * len(ssVar1) +
            ['SG1'] * len(ssVar2) +
            ['LineSG'] * len(ssVarLine) +
            ['Load'] * len(ssVarLoad)
    )
    ssVariables = np.column_stack((ssVariables, np.array(labels, dtype=object)))
    Asys = Asys[1:, 1:]
    ssVariables = ssVariables[1:, :]
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag
