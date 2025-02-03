# Critical imports
import numpy as np
from lib.ssmodel_gfl_infinite import ssmodel_gfl_infinite
# Optional imports (plotting & file export)
from plott import plott
from Testing.toCSV import flatten_column_major

def main_gfl_infinite(user_params=None):
    # Parameters
    wbase = 2 * np.pi * 60
    parasIBR = {
        'Pset': 0.1, 'Qset': 0.0,  # setpoints
        'wset': 1.0, 'Vset': 1.0,  # setpoints
        'mp': 1.00, 'mq': 1.00,    # droop gains
        'Rt': 0.02, 'Lt': 0.10,    # LCL filter
        'Rd': 0.00, 'Cf': 0.05,    # LCL filter
        'Rc': 0.10, 'Lc': 0.50,    # LCL filter
        'KpL': 1.8, 'KiL': 160 * 2,  # PLL PI gains
        'KpS': 0.2, 'KiS': 5.0,    # power loop PI gains
        'KpC': 0.4, 'KiC': 8.0,    # current loop PI gains
        'wcpll': 2 * np.pi * 100,  # PLL frequency filter cut-off frequency
        'wc': 2 * np.pi * 5        # power filter cut-off frequency
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
        ssmodel_gfl_infinite(wbase, parasIBR, dominantParticipationFactorBoundary)
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

    plott(testResults)
    #flatten_column_major(testResults)

    return testResults  # Now it only returns results without calling visualization

if __name__ == "__main__":
    results = main_gfl_infinite()
    print(results)