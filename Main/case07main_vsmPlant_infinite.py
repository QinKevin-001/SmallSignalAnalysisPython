#DONT TOUCH
# Critical imports
import numpy as np
from lib.ssmodel_vsmPlant_infinite import ssmodel_vsmPlant_infinite
# Optional imports (plotting & file export)
from plott import plott
from Testing.toCSV import flatten_column_major

def main_vsmPlant_infinite(user_params=None):
    # Base angular frequency
    wbase = 2 * np.pi * 60

    # Parameters
    parasIBR = {
        # plant-level setpoints
        'PsetPlant': 0.1, 'QsetPlant': 0.1,
        'wsetPlant': 1.0, 'VsetPlant': 1.0,
        # plant-level droop gains
        'mpPlant': 0.05, 'mqPlant': 0.05,
        # plant-level PLL PI gains
        'KpPLLplant': 1.8, 'KiPLLplant': 160,
        # plant-level active loop PI gains
        'KpPlantP': 0.12, 'KiPlantP': 0.50,
        # plant-level reactive loop PI gains
        'KpPlantQ': 1.25, 'KiPlantQ': 5.00,
        # plant-level PLL frequency filter cut-off frequency
        'wcpllPlant': 2 * np.pi * 100,
        # plant-level power filter cut-off frequency
        'wcPlant': 2 * np.pi * 1,
        # Communication delay
        'tDelay': 0.25,
        # inverter-level setpoints
        'wset': 1.0, 'Vset': 1.0,
        # inverter-level droop gains
        'mp': 0.05, 'mq': 0.05,
        # inverter LCL filter
        'Rt': 0.02, 'Lt': 0.10,
        'Rd': 10.00, 'Cf': 0.05,
        'Rc': 0.10, 'Lc': 0.50,
        # inverter-level inertia constant
        'J': 10.0,
        # inverter-level reactive loop control parameter
        'K': 12.0,
        # inverter-level power filter time constant
        'tauf': 0.01
    }

    # Override parameters with user-defined values if provided
    if user_params:
        for key in parasIBR.keys():
            if key in user_params:
                parasIBR[key] = user_params[key]

    # Run the small-signal stability analysis
    dominantParticipationFactorBoundary = 0.01
    Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = ssmodel_vsmPlant_infinite(
        wbase, parasIBR, dominantParticipationFactorBoundary
    )

    # Store results (header + one row of results)
    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]
    testResults.append([
        parasIBR,
        eigenvalueAnalysisResults['eigs'],
        eigenvalueAnalysisResults['maxRealValue'],
        eigenvalueAnalysisResults['minDampingRatio'],
        eigenvalueAnalysisResults['modalAnalysis'],
        pfExitFlag
    ])

    #plott(testResults)
    #flatten_column_major(testResults)

    return testResults


if __name__ == "__main__":
    results = main_vsmPlant_infinite()
    print(results)
