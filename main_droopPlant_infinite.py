# Critical imports
import numpy as np
from lib.ssmodel_droopPlant_infinite import ssmodel_droopPlant_infinite
# Optional imports (plotting & file export)
from plott import plott
from Testing.toCSV import flatten_column_major

def main_droopPlant_infinite(user_params=None):
    # Base angular frequency
    wbase = 2 * np.pi * 60
    parasIBR = {
        'PsetPlant': 1.0, 'QsetPlant': 0.0,
        'wsetPlant': 1.0, 'VsetPlant': 1.0,
        'mpPlant': 0.05, 'mqPlant': 0.05,
        'KpPLLplant': 1.0, 'KiPLLplant': 160,
        'KpPlantP': 0.10, 'KiPlantP': 6.0,
        'KpPlantQ': 0.10, 'KiPlantQ': 6.00,
        'wcpllPlant': 2 * np.pi * 100,
        'wcPlant': 2 * np.pi * 1,
        'wset': 1.0, 'Vset': 1.0,
        'mp': 0.05, 'mq': 0.05,
        'Rt': 0.02, 'Lt': 0.10,
        'Rd': 0.00, 'Cf': 0.05,
        'Rc': 0.10, 'Lc': 0.50,
        'KpV': 0.9, 'KiV': 8.0,
        'KpC': 0.4, 'KiC': 8.0,
        'wc': 2 * np.pi * 5
    }

    # Override parameters with user-defined values
    if user_params:
        for key in parasIBR.keys():
            if key in user_params:
                parasIBR[key] = user_params[key]

    # Store results
    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    # Run the simulation
    dominantParticipationFactorBoundary = 0.01
    Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = (
        ssmodel_droopPlant_infinite(wbase, parasIBR, dominantParticipationFactorBoundary)
    )

    # Store results
    testResults.append([
        parasIBR,
        eigenvalueAnalysisResults['eigs'],
        eigenvalueAnalysisResults['maxRealValue'],
        eigenvalueAnalysisResults['minDampingRatio'],
        eigenvalueAnalysisResults['modalAnalysis'],
        pfExitFlag
    ])

    #plott(testResults)
    # flatten_column_major(testResults)  # Uncomment if needed

    return testResults

if __name__ == "__main__":
    results = main_droopPlant_infinite()
    print(results)  # Print results when running standalone