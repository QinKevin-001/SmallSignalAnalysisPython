#Critical imports
import numpy as np
from lib.ssmodel_droopSimplified_infinite import ssmodel_droopSimplified_infinite
#Optional imports (plotting & file export)
from plott import plott
from visualization import visualization
from Testing.toCSV import flatten_column_major

def main_droopSimplified_infinite():
    # Parameters
    wbase = 2 * np.pi * 60
    parasIBR = {
        'Pset': 1.0, 'Qset': 0.0,  # setpoints
        'wset': 1.0, 'Vset': 1.0,  # setpoints
        'mp': 0.05,  'mq': 0.05,   # droop gains
        'Rc': 0.04,  'Lc': 0.20,   # LCL filter
        'wc': 2 * np.pi * 5  # power filter cut-off frequency
    }

    # Column Names
    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    for i in range(1, 11):
        # Interested Parameter
        parasIBR['wc'] = 2 * np.pi * (1.1 - 0.1 * i)
        # Small-signal Stability Analysis
        dominantParticipationFactorBoundary = 0.10
        Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = (
            ssmodel_droopSimplified_infinite(wbase, parasIBR, dominantParticipationFactorBoundary))
        # Output results
        testResults.append([
            parasIBR['wc'],  # Interested parameter
            eigenvalueAnalysisResults['eigs'],  # Eigenvalues
            eigenvalueAnalysisResults['maxRealValue'],  # Maximum real part of eigenvalues
            eigenvalueAnalysisResults['minDampingRatio'],  # Minimum damping ratio
            eigenvalueAnalysisResults['modalAnalysis'],  # Modal analysis results
            pfExitFlag  # Participation factor exit flag
        ])

    plott(testResults)
    visualization(testResults)
    #flatten_column_major(testResults)


if __name__ == "__main__":
    main_droopSimplified_infinite()