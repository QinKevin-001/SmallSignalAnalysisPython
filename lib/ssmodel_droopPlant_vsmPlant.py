import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibrPlant_ibrPlant import pf_func_ibrPlant_ibrPlant
from lib.pf_calc_ibrPlant_ibrPlant import pf_calc_ibrPlant_ibrPlant
from lib.steadystatevalue_droopPlant import steadystatevalue_droopPlant
from lib.steadystatevalue_vsmPlant import steadystatevalue_vsmPlant
from lib.steadystatevalue_line import steadystatevalue_line
from lib.steadystatevalue_load import steadystatevalue_load
from lib.ssmodel_droopPlant import ssmodel_droopPlant
from lib.ssmodel_vsmPlant import ssmodel_vsmPlant
from lib.ssmodel_line import ssmodel_line
from lib.ssmodel_load import ssmodel_load
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_droopPlant_vsmPlant(wbase, parasIBR1, parasIBR2, parasLine1, parasLine2, parasLoad, dominantParticipationFactorBoundary):
    # Power Flow Calculation
    x0 = np.array([1, 0, 0, 0, 1, 1, 1, 1])  # Initial condition
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibrPlant_ibrPlant(x, parasIBR1, parasIBR2, parasLine1, parasLine2, parasLoad),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier  # Convergence flag
    w, V1, V2, V3, Io1, Io2 = pf_calc_ibrPlant_ibrPlant(x, parasLine1, parasLine2, parasLoad)

    # Steady-State Values
    steadyStateValuesX1, steadyStateValuesU1 = steadystatevalue_droopPlant(w, V1, Io1, parasIBR1)
    steadyStateValuesX2, steadyStateValuesU2 = steadystatevalue_vsmPlant(w, V2, Io2, parasIBR2)
    steadyStateValuesXLine1, steadyStateValuesULine1 = steadystatevalue_line(w, V1, V3, parasLine1)
    steadyStateValuesXLine2, steadyStateValuesULine2 = steadystatevalue_line(w, V2, V3, parasLine2)
    steadyStateValuesXLoad, steadyStateValuesULoad = steadystatevalue_load(w, V3, parasLoad)
    steadyStateValuesX = np.concatenate((steadyStateValuesX1, steadyStateValuesX2,
                                         steadyStateValuesXLine1, steadyStateValuesXLine2,
                                         steadyStateValuesXLoad))

    # Small-signal Modeling
    stateMatrix1 = ssmodel_droopPlant(wbase, parasIBR1, steadyStateValuesX1, steadyStateValuesU1, 1)
    stateMatrix2 = ssmodel_vsmPlant(wbase, parasIBR2, steadyStateValuesX2, steadyStateValuesU2, 0)
    stateMatrixLine1 = ssmodel_line(wbase, parasLine1, steadyStateValuesXLine1, steadyStateValuesULine1)
    stateMatrixLine2 = ssmodel_line(wbase, parasLine2, steadyStateValuesXLine2, steadyStateValuesULine2)
    stateMatrixLoad = ssmodel_load(wbase, parasLoad, steadyStateValuesXLoad, steadyStateValuesULoad)

    # Retrieve state-space matrices
    A1, B1, Bw1, C1, Cw1 = stateMatrix1['A'], stateMatrix1['B'], stateMatrix1['Bw'], stateMatrix1['C'], stateMatrix1['Cw']
    A2, B2, Bw2, C2 = stateMatrix2['A'], stateMatrix2['B'], stateMatrix2['Bw'], stateMatrix2['C']
    Aline1, B1line1, B2line1, Bwline1 = stateMatrixLine1['A'], stateMatrixLine1['B1'], stateMatrixLine1['B2'], stateMatrixLine1['Bw']
    Aline2, B1line2, B2line2, Bwline2 = stateMatrixLine2['A'], stateMatrixLine2['B1'], stateMatrixLine2['B2'], stateMatrixLine2['Bw']
    Aload, Bload, Bwload = stateMatrixLoad['A'], stateMatrixLoad['B'], stateMatrixLoad['Bw']

    # Define Coupling Matrices
    Rx = parasLoad['Rx']
    Ngen1 = Rx * np.array([[1, 0], [0, 1]])
    Nline1Gen = -Rx * np.array([[1, 0], [0, 1]])
    Ngen2 = Rx * np.array([[1, 0], [0, 1]])
    Nline2Gen = -Rx * np.array([[1, 0], [0, 1]])
    Nline1Load = Rx * np.array([[1, 0], [0, 1]])
    Nline2Load = Rx * np.array([[1, 0], [0, 1]])
    Nload = -Rx * np.array([[1, 0], [0, 1]])

    # --- Row 1 Blocks (IBR1: 22 rows) ---
    row1_block1 = A1 + Bw1 @ Cw1 + B1 @ Ngen1 @ C1  # (22×22): IBR1 self-dynamics (note: Cw1 is 1×22 so Bw1 @ Cw1 is 22×22)
    row1_block2 = np.zeros((22, 21))  # (22×21): Zero block for IBR1-to-IBR2 coupling
    row1_block3 = B1 @ Nline1Gen  # (22×2): Coupling from IBR1 to Line1
    row1_block4 = np.zeros((22, 2))  # (22×2): Zero block for IBR1-to-Line2 coupling
    row1_block5 = np.zeros((22, 2))  # (22×2): Zero block for IBR1-to-Load coupling
    row1 = np.hstack([row1_block1, row1_block2, row1_block3, row1_block4, row1_block5])  # (22×49): Assemble Row 1

    # --- Row 2 Blocks (IBR2: 21 rows) ---
    row2_block1 = Bw2 @ Cw1  # (21×22): Bw2 (21×1) * Cw1 (1×22)
    row2_block2 = A2 + B2 @ Ngen2 @ C2  # (21×21): IBR2 self-dynamics
    row2_block3 = np.zeros((21, 2))  # (21×2): Zero block for IBR2-to-Load coupling
    row2_block4 = B2 @ Nline2Gen  # (21×2): Coupling from IBR2 to Line2
    row2_block5 = np.zeros((21, 2))  # (21×2): Zero block for IBR2-to-Load coupling
    row2 = np.hstack([row2_block1, row2_block2, row2_block3, row2_block4, row2_block5])  # (21×49): Assemble Row 2

    # --- Row 3 Blocks (Line1: 2 rows) ---
    row3_block1 = Bwline1 @ Cw1 + B1line1 @ Ngen1 @ C1  # (2×22): Line1 coupling from IBR1
    row3_block2 = np.zeros((2, 21))  # (2×21): Zero block for Line1-to-IBR2 coupling
    row3_block3 = Aline1 + B1line1 @ Nline1Gen + B2line1 @ Nline1Load  # (2×2): Line1 self-dynamics & coupling
    row3_block4 = B2line1 @ Nline2Load  # (2×2): Coupling from IBR2 to Line1 via load
    row3_block5 = B2line1 @ Nload  # (2×2): Coupling from Line1 to Load
    row3 = np.hstack([row3_block1, row3_block2, row3_block3, row3_block4, row3_block5])  # (2×49): Assemble Row 3

    # --- Row 4 Blocks (Line2: 2 rows) ---
    row4_block1 = Bwline2 @ Cw1  # (2×22): Line2 coupling from IBR1
    row4_block2 = B1line2 @ Ngen2 @ C2  # (2×21): Coupling from IBR2 to Line2
    row4_block3 = B2line2 @ Nline1Load  # (2×2): Coupling from Line1 to Line2
    row4_block4 = Aline2 + B1line2 @ Nline2Gen + B2line2 @ Nline2Load  # (2×2): Line2 self-dynamics & coupling
    row4_block5 = B2line2 @ Nload  # (2×2): Coupling from Line2 to Load
    row4 = np.hstack([row4_block1, row4_block2, row4_block3, row4_block4, row4_block5])  # (2×49): Assemble Row 4

    # --- Row 5 Blocks (Load: 2 rows) ---
    row5_block1 = Bwload @ Cw1  # (2×22): Load coupling from IBR1
    row5_block2 = np.zeros((2, 21))  # (2×21): Zero block for Load-to-IBR2 coupling
    row5_block3 = Bload @ Nline1Load  # (2×2): Coupling from Line1 to Load
    row5_block4 = Bload @ Nline2Load  # (2×2): Coupling from Line2 to Load
    row5_block5 = Aload + Bload @ Nload  # (2×2): Load self-dynamics
    row5 = np.hstack([row5_block1, row5_block2, row5_block3, row5_block4, row5_block5])  # (2×49): Assemble Row 5

    # --- Assemble the overall system matrix ---
    Asys = np.vstack([row1, row2, row3, row4, row5])  # (49×49): Overall system matrix assembled from 5 rows

    # Directly concatenate the ssVariables as in MATLAB
    # First, ensure all are numpy arrays
    ssVars1 = np.array(stateMatrix1['ssVariables'], dtype=object)
    ssVars2 = np.array(stateMatrix2['ssVariables'], dtype=object)
    ssVarsLine1 = np.array(stateMatrixLine1['ssVariables'], dtype=object)
    ssVarsLine2 = np.array(stateMatrixLine2['ssVariables'], dtype=object)
    ssVarsLoad = np.array(stateMatrixLoad['ssVariables'], dtype=object)

    # Vertical concatenation (similar to MATLAB's [a;b;c])
    try:
        # Try direct concatenation first
        ssVariables = np.vstack([ssVars1, ssVars2, ssVarsLine1, ssVarsLine2, ssVarsLoad])
    except ValueError:
        # If that fails, create a new array with the right shape
        # Based on MATLAB code, we expect 22 IBR1 states, 21 IBR2 states, 2 Line1 states, 2 Line2 states, and 2 Load states
        ssVariables = np.empty((22 + 21 + 2 + 2 + 2, 2), dtype=object)

        # Fill in the first column with state variable names
        # This assumes the first column of each ssVars contains the variable names
        if ssVars1.ndim == 2:
            ssVariables[:22, 0] = ssVars1[:, 0]
        else:
            ssVariables[:22, 0] = ssVars1

        if ssVars2.ndim == 2:
            ssVariables[22:43, 0] = ssVars2[:, 0]
        else:
            ssVariables[22:43, 0] = ssVars2

        if ssVarsLine1.ndim == 2:
            ssVariables[43:45, 0] = ssVarsLine1[:, 0]
        else:
            ssVariables[43:45, 0] = ssVarsLine1

        if ssVarsLine2.ndim == 2:
            ssVariables[45:47, 0] = ssVarsLine2[:, 0]
        else:
            ssVariables[45:47, 0] = ssVarsLine2

        if ssVarsLoad.ndim == 2:
            ssVariables[47:49, 0] = ssVarsLoad[:, 0]
        else:
            ssVariables[47:49, 0] = ssVarsLoad

    # Set the component labels exactly as in the MATLAB code
    ssVariables[:, 1] = np.array([
        'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1',
        'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1', 'IBR1',
        'IBR1', 'IBR1',
        'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2',
        'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2', 'IBR2',
        'IBR2',
        'Line1', 'Line1',
        'Line2', 'Line2',
        'Load', 'Load'
    ], dtype=object)

    # Remove the 10th row and 10th column (index 9) to mimic MATLAB's deletion
    Asys = np.delete(Asys, 9, axis=0)
    Asys = np.delete(Asys, 9, axis=1)
    ssVariables = np.delete(ssVariables, 9, axis=0)

    # Perform eigenvalue analysis
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag