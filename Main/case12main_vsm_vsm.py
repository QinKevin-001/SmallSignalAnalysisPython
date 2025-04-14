#critical imports
import numpy as np
from lib.ssmodel_vsm_vsm import ssmodel_vsm_vsm
# Optional imports (plotting & file export)
from plott import plott
from Testing.toCSV import flatten_column_major

def main_vsm_vsm(user_params=None):
    #parameters
    wbase = 2 * np.pi * 60
    parasIBR1 = {
        'Pset': 0.1, 'Qset': 0.0,  #setpoints
        'wset': 1.0, 'Vset': 1.0,  #setpoints
        'mp': 0.05, 'mq': 0.05,  #droop gains
        'Rt': 0.02, 'Lt': 0.10,  # inverter LCL filter
        'Rd': 0.00, 'Cf': 0.05,  # inverter LCL filter
        'Rc': 0.10, 'Lc': 0.50,  # inverter LCL filter
        'J': 10.0,  #inertia constant
        'K': 12.0,  #reactive loop control parameter
        'tauf': 0.02    #power filter time constant

    }

    parasIBR2 = {
        'Pset': 0.1, 'Qset': 0.0,  #setpoints
        'wset': 1.0, 'Vset': 1.0,  #setpoints
        'mp': 0.05, 'mq': 0.05,  #droop gains
        'Rt': 0.02, 'Lt': 0.10,  # inverter LCL filter
        'Rd': 0.00, 'Cf': 0.05,  # inverter LCL filter
        'Rc': 0.10, 'Lc': 0.50,  # inverter LCL filter
        'J': 10.0,  #inertia constant
        'K': 12.0,  #reactive loop control parameter
        'tauf': 0.01    #power filter time constant

    }

    parasLoad = {
        'Rload': 0.90, 'Lload': 0.4358, #load parameters
        'Rx': 100   #virtual resistance
    }


    # If user-defined parameters exist, update the default dictionary
    if user_params:
        for key in parasIBR1.keys():
            if key in user_params:
                parasIBR1[key] = user_params[key]

    if user_params:
        for key in parasIBR2.keys():
            if key in user_params:
                parasIBR2[key] = user_params[key]

    if user_params:
        for key in parasLoad.keys():
            if key in user_params:
                parasLoad[key] = user_params[key]

    # Column Names
    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    # Run the simulation for a single set of parameters
    dominantParticipationFactorBoundary = 0.01
    Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = (
        ssmodel_vsm_vsm(wbase, parasIBR1, parasIBR2, parasLoad, dominantParticipationFactorBoundary)
    )

    # Store the results
    testResults.append([
        parasIBR1,  # Store the full parameter dictionary for reference
        eigenvalueAnalysisResults['eigs'],
        eigenvalueAnalysisResults['maxRealValue'],
        eigenvalueAnalysisResults['minDampingRatio'],
        eigenvalueAnalysisResults['modalAnalysis'],
        pfExitFlag
    ])

    #plott(testResults)
    #flatten_column_major(testResults)

    return testResults  # Now it only returns results without calling visualization

if __name__ == "__main__":
    results = main_vsm_vsm()
    print(results)
