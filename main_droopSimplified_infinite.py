#DONT TOUCH
import numpy as np
from lib.ssmodel_droopSimplified_infinite import ssmodel_droopSimplified_infinite
# Optional imports (plotting & file export)
from plott import plott
from Testing.toCSV import flatten_column_major

def main_droopSimplified_infinite(user_params=None):
    # Parameters
    wbase = 2 * np.pi * 60
    parasIBR = {
        'Pset': 1.0, 'Qset': 0.0,  # setpoints
        'wset': 1.0, 'Vset': 1.0,  # setpoints
        'mp': 0.05,  'mq': 0.05,   # droop gains
        'Rc': 0.04,  'Lc': 0.20,   # LCL filter
        'wc': 2 * np.pi * 5  # power filter cut-off frequency
    }

    # If user-defined parameters exist, update the default dictionary
    if user_params:
        for key in parasIBR.keys():
            if key in user_params:
                parasIBR[key] = user_params[key]

    # Column Names
    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    # Run the simulation for a single set of parameters
    dominantParticipationFactorBoundary = 0.10
    Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = (
        ssmodel_droopSimplified_infinite(wbase, parasIBR, dominantParticipationFactorBoundary)
    )

    # Store the results: (to match MATLAB)
    testResults.append([
        parasIBR['wc'],
        eigenvalueAnalysisResults['eigs'],
        eigenvalueAnalysisResults['maxRealValue'],
        eigenvalueAnalysisResults['minDampingRatio'],
        eigenvalueAnalysisResults['modalAnalysis'],
        pfExitFlag
    ])

    # plott(testResults)
    flatten_column_major(testResults)

    return testResults

if __name__ == "__main__":
    results = main_droopSimplified_infinite()
    print(results)  # Print results when running standalone