import numpy as np
from lib import ssmodel_droopSimplified_infinite
from plott import plott

def main_droopSimplified_infinite():
    # Parameters
    wbase = 2 * np.pi * 60

    parasIBR = {
        'Pset': 1.0,
        'Qset': 0.0,
        'wset': 1.0,
        'Vset': 1.0,
        'mp': 0.05,
        'mq': 0.05,
        'Rc': 0.04,
        'Lc': 0.20,
        'wc': 2 * np.pi * 5  # Initial power filter cut-off frequency
    }

    # Prepare results container
    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    for i in range(10):
        # Update the interested parameter
        parasIBR['wc'] = 2 * np.pi * (1.1 - 0.1 * i)

        # Small-signal Stability Analysis
        dominantParticipationFactorBoundary = 0.10
        Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = ssmodel_droopSimplified_infinite(wbase, parasIBR, dominantParticipationFactorBoundary)

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

if __name__ == "__main__":
    main_droopSimplified_infinite()