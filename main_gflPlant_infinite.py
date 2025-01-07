# Critical imports
import numpy as np
from lib.ssmodel_gflPlant_infinite import ssmodel_gflPlant_infinite
# Optional imports (plotting & file export)
from plott import plott
from visualization import visualization
from Testing.toCSV import flatten_column_major


def main_gflPlant_infinite():
    # Parameters
    wbase = 2 * np.pi * 60
    parasIBR = {
        'PsetPlant': 1.0, 'QsetPlant': 0.0,  # plant-level setpoints
        'wsetPlant': 1.0, 'VsetPlant': 1.0,  # plant-level setpoints
        'mpPlant': 1.00, 'mqPlant': 1.00,  # plant-level droop gains
        'KpPLLplant': 1.8, 'KiPLLplant': 160,  # plant-level PLL PI gains
        'KpPlantP': 0.25, 'KiPlantP': 9.0,  # plant-level active loop PI gains
        'KpPlantQ': 0.20, 'KiPlantQ': 20.0,  # plant-level reactive loop PI gains
        'wcpllPlant': 2 * np.pi * 100,  # plant-level PLL frequency filter cut-off frequency
        'wcPlant': 2 * np.pi * 1,  # plant-level power filter cut-off frequency
        'wset': 1.0, 'Vset': 1.0,  # inverter-level setpoints
        'mp': 1.00, 'mq': 1.00,  # inverter-level droop gains
        'Rt': 0.02, 'Lt': 0.10,  # inverter LCL filter
        'Rd': 0.00, 'Cf': 0.05,  # inverter LCL filter
        'Rc': 0.10, 'Lc': 0.50,  # inverter LCL filter
        'KpL': 1.8, 'KiL': 160 * 2,  # inverter-level PLL PI gains
        'KpS': 0.2, 'KiS': 5.0,  # inverter-level power loop PI gains
        'KpC': 0.4, 'KiC': 8.0,  # inverter-level current loop PI gains
        'wcpll': 2 * np.pi * 100,  # inverter-level PLL frequency filter cut-off frequency
        'wc': 2 * np.pi * 5,  # inverter-level power filter cut-off frequency
    }

    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    for i in range(1, 11):
        # Interested Parameter
        parasIBR['PsetPlant'] = 0.1 * i

        # Small-signal Stability Analysis
        dominantParticipationFactorBoundary = 0.10
        Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = (
            ssmodel_gflPlant_infinite(wbase, parasIBR, dominantParticipationFactorBoundary))

        # Output
        testResults.append([
            parasIBR['PsetPlant'],
            eigenvalueAnalysisResults['eigs'],
            eigenvalueAnalysisResults['maxRealValue'],
            eigenvalueAnalysisResults['minDampingRatio'],
            eigenvalueAnalysisResults['modalAnalysis'],
            pfExitFlag
        ])

    #plott(testResults)
    #visualization(testResults)
    flatten_column_major(testResults)


if __name__ == "__main__":
    main_gflPlant_infinite()
