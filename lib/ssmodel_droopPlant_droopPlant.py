#DONT TOUCH
import numpy as np
from scipy.optimize import fsolve
from lib.pf_func_ibrPlant_ibrPlant import pf_func_ibrPlant_ibrPlant
from lib.pf_calc_ibrPlant_ibrPlant import pf_calc_ibrPlant_ibrPlant
from lib.steadystatevalue_droopPlant import steadystatevalue_droopPlant
from lib.steadystatevalue_line import steadystatevalue_line
from lib.steadystatevalue_load import steadystatevalue_load
from lib.ssmodel_droopPlant import ssmodel_droopPlant
from lib.ssmodel_line import ssmodel_line
from lib.ssmodel_load import ssmodel_load
from lib.eigenvalue_analysis import eigenvalue_analysis

def ssmodel_droopPlant_droopPlant(wbase, parasIBR1, parasIBR2, parasLine1, parasLine2, parasLoad, dominantParticipationFactorBoundary):
    """Computes the small-signal model for the Droop Plant + Droop Plant system."""
    ## **Power Flow Calculation**
    x0 = np.array([1, 0, 0, 0, 1, 1, 1, 1])  # Initial condition
    x, info, ier, msg = fsolve(  # Solve power flow equations
        lambda x: pf_func_ibrPlant_ibrPlant(x, parasIBR1, parasIBR2, parasLine1, parasLine2, parasLoad),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier  # Convergence status

    # **Calculate Power Flow**
    w, V1, V2, V3, Io1, Io2 = pf_calc_ibrPlant_ibrPlant(x, parasLine1, parasLine2, parasLoad)  # Power flow outputs

    ## **Steady-State Values**
    steadyStateValuesX1, steadyStateValuesU1 = steadystatevalue_droopPlant(w, V1, Io1, parasIBR1)  # Droop Plant 1
    steadyStateValuesX2, steadyStateValuesU2 = steadystatevalue_droopPlant(w, V2, Io2, parasIBR2)  # Droop Plant 2
    steadyStateValuesXLine1, steadyStateValuesULine1 = steadystatevalue_line(w, V1, V3, parasLine1)  # Line 1
    steadyStateValuesXLine2, steadyStateValuesULine2 = steadystatevalue_line(w, V2, V3, parasLine2)  # Line 2
    steadyStateValuesXLoad, steadyStateValuesULoad = steadystatevalue_load(w, V3, parasLoad)  # Load

    # **Combine steady-state values**
    steadyStateValuesX = np.concatenate([
        steadyStateValuesX1, steadyStateValuesX2,
        steadyStateValuesXLine1, steadyStateValuesXLine2,
        steadyStateValuesXLoad
    ])  # Concatenate all steady-state state vectors

    ## **Small-Signal Modeling**
    stateMatrix1 = ssmodel_droopPlant(wbase, parasIBR1, steadyStateValuesX1, steadyStateValuesU1, 1)  # Droop Plant 1 model
    stateMatrix2 = ssmodel_droopPlant(wbase, parasIBR2, steadyStateValuesX2, steadyStateValuesU2, 0)  # Droop Plant 2 model
    stateMatrixLine1 = ssmodel_line(wbase, parasLine1, steadyStateValuesXLine1, steadyStateValuesULine1)  # Line 1 model
    stateMatrixLine2 = ssmodel_line(wbase, parasLine2, steadyStateValuesXLine2, steadyStateValuesULine2)  # Line 2 model
    stateMatrixLoad = ssmodel_load(wbase, parasLoad, steadyStateValuesXLoad, steadyStateValuesULoad)  # Load model

    # **Extract matrices**
    A1, B1, Bw1, C1, Cw1 = stateMatrix1['A'], stateMatrix1['B'], stateMatrix1['Bw'], stateMatrix1['C'], stateMatrix1['Cw']  # Droop Plant 1 matrices
    A2, B2, Bw2, C2 = stateMatrix2['A'], stateMatrix2['B'], stateMatrix2['Bw'], stateMatrix2['C']  # Droop Plant 2 matrices
    Aline1, B1line1, B2line1, Bwline1 = stateMatrixLine1['A'], stateMatrixLine1['B1'], stateMatrixLine1['B2'], stateMatrixLine1['Bw']  # Line 1 matrices
    Aline2, B1line2, B2line2, Bwline2 = stateMatrixLine2['A'], stateMatrixLine2['B1'], stateMatrixLine2['B2'], stateMatrixLine2['Bw']  # Line 2 matrices
    Aload, Bload, Bwload = stateMatrixLoad['A'], stateMatrixLoad['B'], stateMatrixLoad['Bw']  # Load matrices

    # **Define Coupling Matrices**
    Rx = parasLoad['Rx']  # Extract coupling scalar from parasLoad
    Ngen1, Ngen2 = Rx * np.eye(2), Rx * np.eye(2)  # Coupling for droop plants
    Nline1Gen, Nline2Gen = -Rx * np.eye(2), -Rx * np.eye(2)  # Coupling from droop to lines (negative sign)
    Nline1Load, Nline2Load, Nload = Rx * np.eye(2), Rx * np.eye(2), -Rx * np.eye(2)  # Coupling for lines to load and load self-coupling

    # --- Row 1 Blocks ---
    row1_block1 = A1 + Bw1 @ Cw1 + B1 @ Ngen1 @ C1  # (22,22): Droop Plant 1 self-dynamics (A1 + Bw1*Cw1 + B1*Ngen1*C1)
    row1_block2 = np.zeros((22, 22))  # (22,22): Zero block for Droop Plant 1 to Droop Plant 2 coupling (unused)
    row1_block3 = B1 @ Nline1Gen  # (22,2): Coupling from Droop Plant 1 to Line 1 (B1*Nline1Gen)
    row1_block4 = np.zeros((22, 2))  # (22,2): Zero block for Droop Plant 1 to Line 2 coupling (unused)
    row1_block5 = np.zeros((22, 2))  # (22,2): Zero block for Droop Plant 1 to Load coupling (unused)
    row1 = np.hstack([row1_block1, row1_block2, row1_block3, row1_block4, row1_block5])  # (22,50): Assemble Row 1

    # --- Row 2 Blocks ---
    row2_block1 = Bw2 @ Cw1  # (22,22): Coupling block for Droop Plant 2 (Bw2*Cw1)
    row2_block2 = A2 + B2 @ Ngen2 @ C2  # (22,22): Droop Plant 2 self-dynamics (A2 + B2*Ngen2*C2)
    row2_block3 = np.zeros((22, 2))  # (22,2): Zero block for Droop Plant 2 to Line 1 coupling (unused)
    row2_block4 = B2 @ Nline2Gen  # (22,2): Coupling from Droop Plant 2 to Line 2 (B2*Nline2Gen)
    row2_block5 = np.zeros((22, 2))  # (22,2): Zero block for Droop Plant 2 to Load coupling (unused)
    row2 = np.hstack([row2_block1, row2_block2, row2_block3, row2_block4, row2_block5])  # (22,50): Assemble Row 2

    # --- Row 3 Blocks (Line 1) ---
    row3_block1 = Bwline1 @ Cw1 + B1line1 @ Ngen1 @ C1  # (2,22): Line 1 self dynamics and coupling from Droop Plant 1 (Bwline1*Cw1 + B1line1*Ngen1*C1)
    row3_block2 = np.zeros((2, 22))  # (2,22): Zero block for Line 1 to Droop Plant 2 coupling (unused)
    row3_block3 = Aline1 + B1line1 @ Nline1Gen + B2line1 @ Nline1Load  # (2,2): Line 1 self dynamics and coupling (Aline1 + B1line1*Nline1Gen + B2line1*Nline1Load)
    row3_block4 = B2line1 @ Nline2Load  # (2,2): Coupling from Droop Plant 2 to Line 1 via load (B2line1*Nline2Load)
    row3_block5 = B2line1 @ Nload  # (2,2): Coupling from Line 1 to Load (B2line1*Nload)
    row3 = np.hstack([row3_block1, row3_block2, row3_block3, row3_block4, row3_block5])  # (2,50): Assemble Row 3

    # --- Row 4 Blocks (Line 2) ---
    row4_block1 = Bwline2 @ Cw1  # (2,22): Line 2 coupling from droop plant(s) (Bwline2*Cw1)
    row4_block2 = B1line2 @ Ngen2 @ C2  # (2,22): Coupling from Droop Plant 2 to Line 2 (B1line2*Ngen2*C2)
    row4_block3 = B2line2 @ Nline1Load  # (2,2): Coupling from Line 1 to Line 2 (B2line2*Nline1Load)
    row4_block4 = Aline2 + B1line2 @ Nline2Gen + B2line2 @ Nline2Load  # (2,2): Line 2 self dynamics and coupling (Aline2 + B1line2*Nline2Gen + B2line2*Nline2Load)
    row4_block5 = B2line2 @ Nload  # (2,2): Coupling from Line 2 to Load (B2line2*Nload)
    row4 = np.hstack([row4_block1, row4_block2, row4_block3, row4_block4, row4_block5])  # (2,50): Assemble Row 4

    # --- Row 5 Blocks (Load) ---
    row5_block1 = Bwload @ Cw1  # (2,22): Load coupling from droop plants (Bwload*Cw1)
    row5_block2 = np.zeros((2, 22))  # (2,22): Zero block for Load to Droop Plant 2 (unused)
    row5_block3 = Bload @ Nline1Load  # (2,2): Coupling from Line 1 to Load (Bload*Nline1Load)
    row5_block4 = Bload @ Nline2Load  # (2,2): Coupling from Line 2 to Load (Bload*Nline2Load)
    row5_block5 = Aload + Bload @ Nload  # (2,2): Load self dynamics (Aload + Bload*Nload)
    row5 = np.hstack([row5_block1, row5_block2, row5_block3, row5_block4, row5_block5])  # (2,50): Assemble Row 5

    # --- Assemble the overall system matrix ---
    Asys = np.vstack([row1, row2, row3, row4, row5])  # (50,50): Overall system matrix assembled from 5 rows of blocks

    ## **State Variable Labels**
    # Helper: force any array into a column vector (flattening any extra dimensions)
    def ensure_column(x):  # Convert input to a column vector containing all elements
        arr = np.array(x)
        return arr.flatten().reshape(-1, 1)

    ssVar1 = ensure_column(stateMatrix1['ssVariables'])  # IBR1 state variables as column vector
    ssVar2 = ensure_column(stateMatrix2['ssVariables'])  # IBR2 state variables as column vector
    ssVarLine1 = ensure_column(stateMatrixLine1['ssVariables'])  # Line1 state variables as column vector
    ssVarLine2 = ensure_column(stateMatrixLine2['ssVariables'])  # Line2 state variables as column vector
    ssVarLoad = ensure_column(stateMatrixLoad['ssVariables'])  # Load state variables as column vector

    ssVariables = np.concatenate([ssVar1, ssVar2, ssVarLine1, ssVarLine2, ssVarLoad], axis=0)  # (TotalStates,1): Concatenate all state variables

    # **Assign Labels to State Variables**
    labels = (  # Create a list of labels corresponding to each state variable
        ['IBR1'] * ssVar1.shape[0] +
        ['IBR2'] * ssVar2.shape[0] +
        ['Line1'] * ssVarLine1.shape[0] +
        ['Line2'] * ssVarLine2.shape[0] +
        ['Load'] * ssVarLoad.shape[0]
    )
    ssVariables = np.column_stack((ssVariables, np.array(labels, dtype=object)))  # (TotalStates,2): Append labels as a second column

    ## **Remove Unwanted Row/Column (Based on MATLAB Code)**
    Asys = np.delete(Asys, 9, axis=0)  # Remove row 10 from Asys
    Asys = np.delete(Asys, 9, axis=1)  # Remove column 10 from Asys
    ssVariables = np.delete(ssVariables, 9, axis=0)  # Remove the corresponding state variable

    ## **Eigenvalue Analysis**
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)  # Perform eigenvalue analysis

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag
