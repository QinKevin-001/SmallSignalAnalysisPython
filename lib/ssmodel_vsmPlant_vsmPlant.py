import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibrPlant_ibrPlant import pf_func_ibrPlant_ibrPlant
from lib.pf_calc_ibrPlant_ibrPlant import pf_calc_ibrPlant_ibrPlant
from lib.steadystatevalue_vsmPlant import steadystatevalue_vsmPlant
from lib.steadystatevalue_line import steadystatevalue_line
from lib.steadystatevalue_load import steadystatevalue_load
from lib.ssmodel_vsmPlant import ssmodel_vsmPlant
from lib.ssmodel_line import ssmodel_line
from lib.ssmodel_load import ssmodel_load
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_vsmPlant_vsmPlant(wbase, parasIBR1, parasIBR2, parasLine1, parasLine2, parasLoad,
                              dominantParticipationFactorBoundary):
    x0 = np.array([1, 0, 0, 0, 1, 1, 1, 1])
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibrPlant_ibrPlant(x, parasIBR1, parasIBR2, parasLine1, parasLine2, parasLoad),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier
    w, V1, V2, V3, Io1, Io2 = pf_calc_ibrPlant_ibrPlant(x, parasLine1, parasLine2, parasLoad)
    steadyStateValuesX1, steadyStateValuesU1 = steadystatevalue_vsmPlant(w, V1, Io1, parasIBR1)
    steadyStateValuesX2, steadyStateValuesU2 = steadystatevalue_vsmPlant(w, V2, Io2, parasIBR2)
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
    stateMatrix1 = ssmodel_vsmPlant(wbase, parasIBR1, steadyStateValuesX1, steadyStateValuesU1, 1)
    stateMatrix2 = ssmodel_vsmPlant(wbase, parasIBR2, steadyStateValuesX2, steadyStateValuesU2, 0)
    stateMatrixLine1 = ssmodel_line(wbase, parasLine1, steadyStateValuesXLine1, steadyStateValuesULine1)
    stateMatrixLine2 = ssmodel_line(wbase, parasLine2, steadyStateValuesXLine2, steadyStateValuesULine2)
    stateMatrixLoad = ssmodel_load(wbase, parasLoad, steadyStateValuesXLoad, steadyStateValuesULoad)

    A1 = stateMatrix1['A']
    B1 = stateMatrix1['B']
    Bw1 = stateMatrix1['Bw']
    C1 = stateMatrix1['C']
    Cw1 = stateMatrix1['Cw']
    A2 = stateMatrix2['A']
    B2 = stateMatrix2['B']
    Bw2 = stateMatrix2['Bw']
    C2 = stateMatrix2['C']
    Aline1 = stateMatrixLine1['A']
    B1line1 = stateMatrixLine1['B1']
    B2line1 = stateMatrixLine1['B2']
    Bwline1 = stateMatrixLine1['Bw']
    Aline2 = stateMatrixLine2['A']
    B1line2 = stateMatrixLine2['B1']
    B2line2 = stateMatrixLine2['B2']
    Bwline2 = stateMatrixLine2['Bw']
    Aload = stateMatrixLoad['A']
    Bload = stateMatrixLoad['B']
    Bwload = stateMatrixLoad['Bw']
    Rx = parasLoad['Rx']
    Ngen1 = Rx * np.eye(2)
    Nline1Gen = -Rx * np.eye(2)
    Ngen2 = Rx * np.eye(2)
    Nline2Gen = -Rx * np.eye(2)
    Nline1Load = Rx * np.eye(2)
    Nline2Load = Rx * np.eye(2)
    Nload = -Rx * np.eye(2)

    # Row 1
    row1_block1 = A1 + Bw1 @ Cw1 + B1 @ Ngen1 @ C1
    row1_block2 = np.zeros((21, 21))
    row1_block3 = B1 @ Nline1Gen
    row1_block4 = np.zeros((21, 2))
    row1_block5 = np.zeros((21, 2))
    row1 = np.hstack([row1_block1, row1_block2, row1_block3, row1_block4, row1_block5])
    # Row 2
    row2_block1 = Bw2 @ Cw1
    row2_block2 = A2 + B2 @ Ngen2 @ C2
    row2_block3 = np.zeros((21, 2))
    row2_block4 = B2 @ Nline2Gen
    row2_block5 = np.zeros((21, 2))
    row2 = np.hstack([row2_block1, row2_block2, row2_block3, row2_block4, row2_block5])
    # Row 3
    row3_block1 = Bwline1 @ Cw1 + B1line1 @ Ngen1 @ C1
    row3_block2 = np.zeros((2, 21))
    row3_block3 = Aline1 + B1line1 @ Nline1Gen + B2line1 @ Nline1Load
    row3_block4 = B2line1 @ Nline2Load
    row3_block5 = B2line1 @ Nload
    row3 = np.hstack([row3_block1, row3_block2, row3_block3, row3_block4, row3_block5])
    # Row 4
    row4_block1 = Bwline2 @ Cw1
    row4_block2 = B1line2 @ Ngen2 @ C2
    row4_block3 = B2line2 @ Nline1Load
    row4_block4 = Aline2 + B1line2 @ Nline2Gen + B2line2 @ Nline2Load
    row4_block5 = B2line2 @ Nload
    row4 = np.hstack([row4_block1, row4_block2, row4_block3, row4_block4, row4_block5])
    # Row 5
    row5_block1 = Bwload @ Cw1
    row5_block2 = np.zeros((2, 21))
    row5_block3 = Bload @ Nline1Load
    row5_block4 = Bload @ Nline2Load
    row5_block5 = Aload + Bload @ Nload
    row5 = np.hstack([row5_block1, row5_block2, row5_block3, row5_block4, row5_block5])
    Asys = np.vstack([row1, row2, row3, row4, row5])
    ssVar1 = np.array(stateMatrix1['ssVariables']).flatten()
    ssVar2 = np.array(stateMatrix2['ssVariables']).flatten()
    ssVarLine1 = np.array(stateMatrixLine1['ssVariables']).flatten()
    ssVarLine2 = np.array(stateMatrixLine2['ssVariables']).flatten()
    ssVarLoad = np.array(stateMatrixLoad['ssVariables']).flatten()
    labels = (['IBR1'] * len(ssVar1) +
              ['IBR2'] * len(ssVar2) +
              ['Line1'] * len(ssVarLine1) +
              ['Line2'] * len(ssVarLine2) +
              ['Load'] * len(ssVarLoad))
    ssVariables = np.column_stack((np.concatenate([ssVar1, ssVar2, ssVarLine1, ssVarLine2, ssVarLoad]),
                                   np.array(labels, dtype=object)))
    Asys = np.delete(Asys, 9, axis=0)
    Asys = np.delete(Asys, 9, axis=1)
    ssVariables = np.delete(ssVariables, 9, axis=0)
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag
