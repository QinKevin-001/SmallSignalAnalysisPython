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
    x, info, ier, msg = fsolve(
        lambda x: pf_func_ibrPlant_ibrPlant(x, parasIBR1, parasIBR2, parasLine1, parasLine2, parasLoad),
        x0,
        xtol=1e-6,
        maxfev=500,
        full_output=True
    )
    pfExitFlag = ier  # Convergence status

    # **Calculate Power Flow**
    w, V1, V2, V3, Io1, Io2 = pf_calc_ibrPlant_ibrPlant(x, parasLine1, parasLine2, parasLoad)

    ## **Steady-State Values**
    steadyStateValuesX1, steadyStateValuesU1 = steadystatevalue_droopPlant(w, V1, Io1, parasIBR1)
    steadyStateValuesX2, steadyStateValuesU2 = steadystatevalue_droopPlant(w, V2, Io2, parasIBR2)
    steadyStateValuesXLine1, steadyStateValuesULine1 = steadystatevalue_line(w, V1, V3, parasLine1)
    steadyStateValuesXLine2, steadyStateValuesULine2 = steadystatevalue_line(w, V2, V3, parasLine2)
    steadyStateValuesXLoad, steadyStateValuesULoad = steadystatevalue_load(w, V3, parasLoad)

    # **Combine steady-state values**
    steadyStateValuesX = np.concatenate([
        steadyStateValuesX1, steadyStateValuesX2,
        steadyStateValuesXLine1, steadyStateValuesXLine2,
        steadyStateValuesXLoad
    ])

    ## **Small-Signal Modeling**
    stateMatrix1 = ssmodel_droopPlant(wbase, parasIBR1, steadyStateValuesX1, steadyStateValuesU1, 1)
    stateMatrix2 = ssmodel_droopPlant(wbase, parasIBR2, steadyStateValuesX2, steadyStateValuesU2, 0)
    stateMatrixLine1 = ssmodel_line(wbase, parasLine1, steadyStateValuesXLine1, steadyStateValuesULine1)
    stateMatrixLine2 = ssmodel_line(wbase, parasLine2, steadyStateValuesXLine2, steadyStateValuesULine2)
    stateMatrixLoad = ssmodel_load(wbase, parasLoad, steadyStateValuesXLoad, steadyStateValuesULoad)

    # **Extract matrices**
    A1, B1, Bw1, C1, Cw1 = stateMatrix1['A'], stateMatrix1['B'], stateMatrix1['Bw'], stateMatrix1['C'], stateMatrix1['Cw']
    A2, B2, Bw2, C2 = stateMatrix2['A'], stateMatrix2['B'], stateMatrix2['Bw'], stateMatrix2['C']
    Aline1, B1line1, B2line1, Bwline1 = stateMatrixLine1['A'], stateMatrixLine1['B1'], stateMatrixLine1['B2'], stateMatrixLine1['Bw']
    Aline2, B1line2, B2line2, Bwline2 = stateMatrixLine2['A'], stateMatrixLine2['B1'], stateMatrixLine2['B2'], stateMatrixLine2['Bw']
    Aload, Bload, Bwload = stateMatrixLoad['A'], stateMatrixLoad['B'], stateMatrixLoad['Bw']

    # **Define Coupling Matrices**
    Rx = parasLoad['Rx']
    Ngen1, Ngen2 = Rx * np.eye(2), Rx * np.eye(2)
    Nline1Gen, Nline2Gen = -Rx * np.eye(2), -Rx * np.eye(2)
    Nline1Load, Nline2Load, Nload = Rx * np.eye(2), Rx * np.eye(2), -Rx * np.eye(2)

    # Fix Bw1 @ Cw1 by transposing Cw1
    Bw1_Cw1 = Bw1 @ Cw1.T  # Now has shape (20, 20)

    # Ensure B1 @ Ngen1 @ C1 has shape (20,20)
    B1_Ngen1_C1 = B1 @ Ngen1 @ C1  # This is correct

    # Now construct Asys correctly
    Asys = np.block([
        [A1 + Bw1_Cw1 + B1_Ngen1_C1, np.zeros((20, 20)), B1 @ Nline1Gen, np.zeros((20, 2)), np.zeros((20, 2))],
        [Bw2 @ Cw1.T, A2 + B2 @ Ngen2 @ C2, np.zeros((20, 2)), B2 @ Nline2Gen, np.zeros((20, 2))],
        [Bwline1 @ Cw1.T + B1line1 @ Ngen1 @ C1, np.zeros((2, 20)), Aline1 + B1line1 @ Nline1Gen + B2line1 @ Nline1Load,
         B2line1 @ Nline2Load, B2line1 @ Nload],
        [Bwline2 @ Cw1.T, B1line2 @ Ngen2 @ C2, B2line2 @ Nline1Load,
         Aline2 + B1line2 @ Nline2Gen + B2line2 @ Nline2Load, B2line2 @ Nload],
        [Bwload @ Cw1.T, np.zeros((2, 20)), Bload @ Nline1Load, Bload @ Nline2Load, Aload + Bload @ Nload]
    ])

    ## **State Variable Labels**
    ssVariables = np.concatenate([
        stateMatrix1['ssVariables'],
        stateMatrix2['ssVariables'],
        stateMatrixLine1['ssVariables'],
        stateMatrixLine2['ssVariables'],
        stateMatrixLoad['ssVariables']
    ])

    # **Assign Labels to State Variables**
    labels = (
        ['IBR1'] * len(stateMatrix1['ssVariables']) +
        ['IBR2'] * len(stateMatrix2['ssVariables']) +
        ['Line1'] * len(stateMatrixLine1['ssVariables']) +
        ['Line2'] * len(stateMatrixLine2['ssVariables']) +
        ['Load'] * len(stateMatrixLoad['ssVariables'])
    )
    ssVariables = np.column_stack((ssVariables, np.array(labels, dtype=object)))

    ## **Remove Unwanted Row/Column (Based on MATLAB Code)**
    Asys = np.delete(Asys, 9, axis=0)  # Remove row 10
    Asys = np.delete(Asys, 9, axis=1)  # Remove column 10
    ssVariables = np.delete(ssVariables, 9, axis=0)

    ## **Eigenvalue Analysis**
    eigenvalueAnalysisResults = eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary)

    return Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag
