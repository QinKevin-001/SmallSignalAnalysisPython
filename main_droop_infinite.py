# Critical imports
import numpy as np
from lib.ssmodel_droop_infinite import ssmodel_droop_infinite
# Optional imports (plotting & file export)
from plott import plott
from Testing.toCSV import flatten_column_major

def main_droop_infinite(user_params=None):
    """
    Runs the small-signal stability simulation.
    If user_params is provided, it overrides the default parameters.
    """
    # Base angular frequency
    wbase = 2 * np.pi * 60

    # Default parameters
    parasIBR = {
        'Pset': 1.0, 'Qset': 0.0,  # setpoints
        'wset': 1.0, 'Vset': 1.0,  # setpoints
        'mp': 0.05, 'mq': 0.05,  # droop gains
        'Rt': 0.02, 'Lt': 0.10,  # LCL filter
        'Rd': 0.00, 'Cf': 0.05,  # LCL filter
        'Rc': 0.04, 'Lc': 0.20,  # LCL filter
        'KpV': 1.8, 'KiV': 16.0,  # voltage loop PI gains
        'KpC': 0.4, 'KiC': 12.0,  # current loop PI gains
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
        ssmodel_droop_infinite(wbase, parasIBR, dominantParticipationFactorBoundary)
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
    # flatten_column_major(testResults)  # Uncomment if needed

    return testResults  # Now it only returns results without calling visualization

if __name__ == "__main__":
    results = main_droop_infinite()
    print(results)  # Print results when running standalone
