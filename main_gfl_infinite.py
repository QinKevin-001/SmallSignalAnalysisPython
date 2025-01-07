# Critical imports
import numpy as np
from lib.ssmodel_gfl_infinite import ssmodel_gfl_infinite
# Optional imports (plotting & file export)
from plott import plott
from visualization import visualization
from Testing.toCSV import flatten_column_major

def main_gfl_infinite():
    # Parameters
    wbase = 2 * np.pi * 60
    parasIBR = {
        'Pset': 0.1, 'Qset': 0.0,  # setpoints
        'wset': 1.0, 'Vset': 1.0,  # setpoints
        'mp': 1.00, 'mq': 1.00,    # droop gains
        'Rt': 0.02, 'Lt': 0.10,    # LCL filter
        'Rd': 0.00, 'Cf': 0.05,    # LCL filter
        'Rc': 0.10, 'Lc': 0.50,    # LCL filter
        'KpL': 1.8, 'KiL': 160 * 2,  # PLL PI gains
        'KpS': 0.2, 'KiS': 5.0,    # power loop PI gains
        'KpC': 0.4, 'KiC': 8.0,    # current loop PI gains
        'wcpll': 2 * np.pi * 100,  # PLL frequency filter cut-off frequency
        'wc': 2 * np.pi * 5        # power filter cut-off frequency
    }

    # Column Names
    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    for i in range(1, 11):
        # Interested Parameter
        parasIBR['Pset'] = 0.1 * i
        # Small-signal Stability Analysis
        dominantParticipationFactorBoundary = 0.10
        Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = (
            ssmodel_gfl_infinite(wbase, parasIBR, dominantParticipationFactorBoundary)
        )
        # Output
        testResults.append([
            parasIBR['Pset'],
            eigenvalueAnalysisResults['eigs'],
            eigenvalueAnalysisResults['maxRealValue'],
            eigenvalueAnalysisResults['minDampingRatio'],
            eigenvalueAnalysisResults['modalAnalysis'],
            pfExitFlag
        ])

    #plott(testResults)
    #visualization(testResults)
    flatten_column_major(testResults)

if __name__ == "__main__":
    main_gfl_infinite()
