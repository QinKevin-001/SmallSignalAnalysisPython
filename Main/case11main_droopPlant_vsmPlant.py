#critical imports
import numpy as np
from lib.ssmodel_droopPlant_vsmPlant import ssmodel_droopPlant_vsmPlant
#optional imports
from plott import plott
from Testing.toCSV import flatten_column_major

def main_droopPlant_vsmPlant(user_params=None):
    #parameters
    wbase = 2 * np.pi * 60
    parasIBR1 = {
        'PsetPlant': 0.1, 'QsetPlant': 0.1,  # plant-level setpoints
        'wsetPlant': 1.0, 'VsetPlant': 1.0,  # plant-level setpoints
        'mpPlant': 1.00, 'mqPlant': 1.00,  # plant-level droop gains
        'KpPLLplant': 1.8/10, 'KiPLLplant': 160/10,  # plant-level PLL PI gains
        'KpPlantP': 0.25, 'KiPlantP': 1.00,  # plant-level active loop PI gains
        'KpPlantQ': 1.25, 'KiPlantQ': 5.00,  # plant-level reactive loop PI gains
        'wcpllPlant': 2 * np.pi * 100,  # plant-level PLL frequency filter cut-off frequency
        'wcPlant': 2 * np.pi * 2,  # plant-level power filter cut-off frequency
        'tDelay': 0.15,  # communication delay
        'wset': 1.0, 'Vset': 1.0,  # inverter-level setpoints
        'mp': 0.05, 'mq': 0.05,  # inverter-level droop gains
        'Rt': 0.02, 'Lt': 0.10,  #LCL filter
        'Rd': 10.00, 'Cf': 0.05,  #LCL filter
        'Rc': 0.01, 'Lc': 0.05,  #LCL filter
        'KpV': 4.0, 'KiV': 15.0, #inverter-level voltage loop PI gains
        'KpC': 0.4, 'KiC':8.0,  #inverter-level current loop PI gains
        'wc': 2 * np.pi * 5 #inverter-level power filter cut-off frequency

    }

    parasIBR2 = {
        'PsetPlant': 0.1, 'QsetPlant': 0.1,  # plant-level setpoints
        'wsetPlant': 1.0, 'VsetPlant': 1.0,  # plant-level setpoints
        'mpPlant': 1.00, 'mqPlant': 1.00,  # plant-level droop gains
        'KpPLLplant': 1.8, 'KiPLLplant': 160,  # plant-level PLL PI gains
        'KpPlantP': 0.12, 'KiPlantP': 0.50,  # plant-level active loop PI gains
        'KpPlantQ': 1.25, 'KiPlantQ': 5.00,  # plant-level reactive loop PI gains
        'wcpllPlant': 2 * np.pi * 100,  # plant-level PLL frequency filter cut-off frequency
        'wcPlant': 2 * np.pi * 1,  # plant-level power filter cut-off frequency
        'tDelay': 0.25,  # communication delay
        'wset': 1.0, 'Vset': 1.0,  # inverter-level setpoints
        'mp': 0.05, 'mq': 0.05,  # inverter-level droop gains
        'Rt': 0.02, 'Lt': 0.10,  #LCL filter
        'Rd': 10.00, 'Cf': 0.05,  #LCL filter
        'Rc': 0.01, 'Lc': 0.05,  #LCL filter
        'J': 10.0,  #inverter-level inertia constant
        'K': 12.0,  #inverter-level reactive loop control parameter
        'tauf': 0.01    #inverter-level power filter time constant

    }

    parasLine1 = {
        'Rline': 0.02, 'Lline': 0.10, #line parameters

    }

    parasLine2 = {
        'Rline': 0.02, 'Lline': 0.10,  #line parameters

    }

    parasLoad = {
        'Rload': 0.90, 'Lload': 0.4358,  #load parameters
        'Rx': 100   #virtual resistancce

    }

    # If user-defined parameters exist, update the default dictionary
    if user_params:
        if 'parasIBR1' in user_params:
            parasIBR1.update({k: float(v) for k, v in user_params['parasIBR1'].items()})
        if 'parasIBR2' in user_params:
            parasIBR2.update({k: float(v) for k, v in user_params['parasIBR2'].items()})
        if 'parasLine1' in user_params:
            parasLine1.update({k: float(v) for k, v in user_params['parasLine1'].items()})
        if 'parasLine2' in user_params:
            parasLine2.update({k: float(v) for k, v in user_params['parasLine2'].items()})
        if 'parasLoad' in user_params:
            parasLoad.update({k: float(v) for k, v in user_params['parasLoad'].items()})

    # Column Names
    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    # Run the simulation for a single set of parameters
    dominantParticipationFactorBoundary = 0.01
    Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = (
        ssmodel_droopPlant_vsmPlant(wbase, parasIBR1, parasIBR2, parasLine1, parasLine2, parasLoad, dominantParticipationFactorBoundary)
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
    results = main_droopPlant_vsmPlant()
    print(results)
