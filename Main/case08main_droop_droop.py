#DONT TOUCH
#critical imports
import numpy as np
from lib.ssmodel_droop_droop import ssmodel_droop_droop
#optional imports
from plott import plott
from Testing.toCSV import flatten_column_major

def main_droop_droop(user_params=None):
    #parameters
    wbase = 2 * np.pi * 60
    parasIBR1 = {
        'Pset':0.1, 'Qset':0.0, #setpoints
        'wset':1.0, 'Vset':1.0,  #setpoints
        'mp':0.05, 'mq':0.05,   #droop gains
        'Rt':0.02, 'Lt':0.10,   #LCL filter
        'Rd':0.00, 'Cf':0.05,   #LCL filter
        'Rc':0.10, 'Lc':0.50,   #LCL filter
        'KpV':4.0, 'KiV':15.0,  #voltage loop PI gains
        'KpC':0.4, 'KiC':8.0,   #current loop PI gains
        'wc':2 * np.pi * 5  #power filter cut-off frequency

    }

    parasIBR2 = {
        'Pset': 0.1, 'Qset': 0.0,  # setpoints
        'wset': 1.0, 'Vset': 1.0,  # setpoints
        'mp': 0.05, 'mq': 0.05,  # droop gains
        'Rt': 0.02, 'Lt': 0.10,  # LCL filter
        'Rd': 0.00, 'Cf': 0.05,  # LCL filter
        'Rc': 0.10, 'Lc': 0.50,  # LCL filter
        'KpV': 4.0, 'KiV': 15.0,  # voltage loop PI gains
        'KpC': 0.4, 'KiC': 8.0,  # current loop PI gains
        'wc': 2 * np.pi * 5  # power filter cut-off frequency

    }

    parasLoad = {
        'Rload': 0.9, 'Lload': 0.4358,  #load parameters
        'Rx': 100   #virtual resistance
    }

    # If user-defined parameters exist, update the default dictionary
    if user_params:
        if 'parasIBR1' in user_params:
            parasIBR1.update({k: float(v) for k, v in user_params['parasIBR1'].items()})
        if 'parasIBR2' in user_params:
            parasIBR2.update({k: float(v) for k, v in user_params['parasIBR2'].items()})
        if 'parasLoad' in user_params:
            parasLoad.update({k: float(v) for k, v in user_params['parasLoad'].items()})

    # Column Names
    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    # Run the simulation for a single set of parameters
    dominantParticipationFactorBoundary = 0.01
    Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = (
        ssmodel_droop_droop(wbase, parasIBR1, parasIBR2, parasLoad, dominantParticipationFactorBoundary)
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
    results = main_droop_droop()
    print(results)
