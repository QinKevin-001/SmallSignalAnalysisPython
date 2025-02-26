#Slight difference, could be from the solver difference
#DONT TOUCH
import numpy as np
from lib.ssmodel_droopPlant_infinite import ssmodel_droopPlant_infinite
from plott import plott
from Testing.toCSV import flatten_column_major

def main_droopPlant_infinite(user_params=None):
    # Define parameters exactly as in the MATLAB script:
    wbase = 2 * np.pi * 60
    parasIBR = {
        'PsetPlant': 1.0,  'QsetPlant': 0.0,
        'wsetPlant': 1.0,  'VsetPlant': 1.0,
        'mpPlant': 0.05,   'mqPlant': 0.05,
        'KpPLLplant': 1.8, 'KiPLLplant': 160,
        'KpPlantP': 0.10,  'KiPlantP': 6.0,
        'KpPlantQ': 0.10,  'KiPlantQ': 6.0,
        'wcpllPlant': 2 * np.pi * 100, 'wcPlant': 2 * np.pi * 5,
        'tDelay': 0.25,
        'wset': 1.0,       'Vset': 1.0,
        'mp': 0.05,        'mq': 0.05,
        'Rt': 0.02,        'Lt': 0.10,
        'Rd': 0.00,        'Cf': 0.05,
        'Rc': 0.04,        'Lc': 0.20,
        'KpV': 1.8,        'KiV': 16.0,
        'KpC': 0.4,        'KiC': 12.0,
        'wc': 2 * np.pi * 5
    }

    # Allow user parameters to override defaults
    if user_params:
        parasIBR.update(user_params)

    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    dominantParticipationFactorBoundary = 0.01
    Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = ssmodel_droopPlant_infinite(
        wbase, parasIBR, dominantParticipationFactorBoundary
    )

    # Store results in a structure similar to MATLAB's output
    testResults.append([
        parasIBR['wc'],
        eigenvalueAnalysisResults['eigs'],
        eigenvalueAnalysisResults['maxRealValue'],
        eigenvalueAnalysisResults['minDampingRatio'],
        eigenvalueAnalysisResults['modalAnalysis'],
        pfExitFlag
    ])

    flatten_column_major(testResults)
    # Optionally, call plott(testResults)

    return testResults

if __name__ == "__main__":
    results = main_droopSimplified_infinite()
    print(results)