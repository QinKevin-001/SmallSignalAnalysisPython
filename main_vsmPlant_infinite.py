#critical imports

#optional imports

def main_vsmPlant_infinite(user_params=None):
    #parameters
    wbase = 2 * np.pi * 60
    parasIBR = {
        'PsetPlant':0.1, 'Qset':0.1, #plant-level setpoints
        'wsetPlant':1.0, 'VsetPlant':1.0,  #plant-level setpoints
        'mpPlant':0.05, 'mqPlant':0.05,   #plant-level droop gains
        'KpPLLplant':1.8, 'KiPLLplant':160,  #plant-level PLL PI gains
        'KpPlantP':0.12, 'KiPlantP':0.50,   #plant-level active loop PI gains
        'KpPlantQ':1.25, 'KiPlantQ':5.00,   #plant-level reactive loop PI gains
        'wcpllPlant': 2 * np.pi * 100,   #plant-level PLL frequency filter cut-off frequency
        'wcPlant': 2 * np.pi * 1,   #plant-level power filter cut-off frequency
        'tDelay':0.25,  #communication delay
        'wset':1.0, 'Vset':1.0,  #inverter-level setpoints
        'mp':0.05, 'mq':0.05,   #inverter-level droop gains
        'Rt':0.02, 'Lt':0.10,   #inverter LCL filter
        'Rd':10.00, 'Cf':0.05,   #inverter LCL filter
        'Rc':0.10, 'Lc':0.50,   #inverter LCL filter
        'J':10.0,   #inverter-level intertia constant
        'K':12.0,    #inverter-level reactive loop control parameter
        'tauf': 0.01    #inverter-level power filter time constant
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
        ssmodel_vsmPlant_infinite(wbase, parasIBR, dominantParticipationFactorBoundary)
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

    #plott(testResults)
    #flatten_column_major(testResults)

    return testResults  # Now it only returns results without calling visualization

if __name__ == "__main__":
    results = main_vsmPlant_infinite()
    print(results)
