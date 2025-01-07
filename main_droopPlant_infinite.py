#Test confirmed

#Critical imports
import numpy as np
from lib.ssmodel_droopPlant_infinite import ssmodel_droopPlant_infinite
from visualization import visualization

#Optional imports (plotting & file export)
from plott import plott
from toCSV import flatten_column_major

def main_droopPlant_infinite():
    # Parameters
    wbase = 2 * np.pi * 60
    parasIBR = {
        'PsetPlant': 1.0, 'QsetPlant': 0.0,  # plant-level setpoints
        'wsetPlant': 1.0, 'VsetPlant': 1.0,  # plant-level setpoints
        'mpPlant': 1.00, 'mqPlant': 1.00,  # plant-level droop gains
        'KpPLLplant': 1.8, 'KiPLLplant': 160,  # plant-level PLL PI gains
        'KpPlantP': 0.10, 'KiPlantP': 6.0,  # plant-level active loop PI gains
        'KpPlantQ': 0.10, 'KiPlantQ': 6.00,  # plant-level reactive loop PI gains
        'wcpllPlant': 2 * np.pi * 100,  # plant-level PLL frequency filter cut-off frequency
        'wcPlant': 2 * np.pi * 1,  # plant-level power filter cut-off frequency
        'wset': 1.0, 'Vset': 1.0,  # inverter-level setpoints
        'mp': 0.05, 'mq': 0.05,  # inverter-level droop gains
        'Rt': 0.02, 'Lt': 0.10,  # inverter LCL filter
        'Rd': 0.00, 'Cf': 0.05,  # inverter LCL filter
        'Rc': 0.10, 'Lc': 0.50,  # inverter LCL filter
        'KpV': 0.9, 'KiV': 8.0,  # inverter-level voltage loop PI gains
        'KpC': 0.4, 'KiC': 8.0,  # inverter-level current loop PI gains
        'wc': 2 * np.pi * 5,  # inverter-level power filter cut-off frequency
    }

    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    for i in range(1, 11):
        # Interested Parameter
        parasIBR['PsetPlant'] = 0.1 * i

        # Small-signal Stability Analysis
        dominantParticipationFactorBoundary = 0.10
        Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = ssmodel_droopPlant_infinite(wbase, parasIBR, dominantParticipationFactorBoundary)
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
    main_droopPlant_infinite()

