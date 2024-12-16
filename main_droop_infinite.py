#Critical imports
import numpy as np
from lib.ssmodel_droop_infinite import ssmodel_droop_infinite
#Optional imports (plotting & file export)
from plott import plott
from toCSV import flatten_column_major
from visualization import visualization

def main_droop_infinite():
    # Parameters
    wbase = 2 * np.pi * 60
    parasIBR = {
        'Pset': 1.0, 'Qset': 0.0,  # setpoints
        'wset': 1.0, 'Vset': 1.0,  # setpoints
        'mp': 0.05,  'mq': 0.05,  # droop gains
        'Rt': 0.02,  'Lt': 0.10,  # LCL filter
        'Rd': 0.00,  'Cf': 0.05,  # LCL filter
        'Rc': 0.04,  'Lc': 0.20,  # LCL filter
        'KpV': 1.8,  'KiV': 16.0,  # voltage loop PI gains
        'KpC': 0.4,  'KiC': 12.0,  # current loop PI gains
        'wc': 2 * np.pi * 5  # power filter cut-off frequency
    }

    # Column Names
    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    for i in range(1, 11):
        # Interested Parameter
        parasIBR['mp'] = 0.11 - 0.01 * i
        # Small-signal Stability Analysis
        dominantParticipationFactorBoundary = 0.10
        Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = (
            ssmodel_droop_infinite(wbase, parasIBR, dominantParticipationFactorBoundary))
        # Output
        testResults.append([
            parasIBR['mp'],
            eigenvalueAnalysisResults['eigs'],
            eigenvalueAnalysisResults['maxRealValue'],
            eigenvalueAnalysisResults['minDampingRatio'],
            eigenvalueAnalysisResults['modalAnalysis'],
            pfExitFlag
        ])

    plott(testResults)
    visualization(testResults)
    #flatten_column_major(testResults)

if __name__ == "__main__":
    main_droop_infinite()