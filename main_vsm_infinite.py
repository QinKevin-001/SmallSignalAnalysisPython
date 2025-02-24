#critical imports
import numpy as np
from lib.ssmodel_vsm_infinite import ssmodel_vsm_infinite
#optional imports
from plott import plott
from Testing.toCSV import flatten_column_major

def main_vsm_infinite(user_params=None):
    #parameters
    wbase = 2 * np.pi * 60
    parasIBR = {
        'Pset':0.1, 'Qset':0.0, #setpoints
        'wset':1.0, 'Vset':1.0,  #setpoints
        'mp':0.05, 'mq':0.05,   #droop gains
        'Rt':0.02, 'Lt':0.10,   #LCL filter
        'Rd':0.00, 'Cf':0.05,   #LCL filter
        'Rc':0.10, 'Lc':0.50,   #LCL filter
        'J':10.0,   #intertia constant
        'K':12.0,    #reactive loop control parameter
        'tauf': 0.01    #power filter time constant
    }

    # If user-defined parameters exist, update the default dictionary
    if user_params:
        for key in parasIBR.keys():
            if key in user_params:
                parasIBR[key] = user_params[key]

    # Column Names
    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    # Run the simulation for a single set of parameters
    dominantParticipationFactorBoundary = 0.01
    Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = (
        ssmodel_vsm_infinite(wbase, parasIBR, dominantParticipationFactorBoundary)
    )

    # Store the results
    testResults.append([
        parasIBR,  # Store the full parameter dictionary for reference
        eigenvalueAnalysisResults['eigs'],
        eigenvalueAnalysisResults['maxRealValue'],
        eigenvalueAnalysisResults['minDampingRatio'],
        eigenvalueAnalysisResults['modalAnalysis'],
        pfExitFlag
    ])

    #plott(testResults)
    flatten_column_major(testResults)

    return testResults  # Now it only returns results without calling visualization

if __name__ == "__main__":
    results = main_vsm_infinite()
    print(results)
