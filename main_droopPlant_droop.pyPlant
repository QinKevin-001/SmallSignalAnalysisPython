#critical imports

#optional imports

def main_droopPlant_droopPlant(user_params=None):
    #parameters
    wbase = 2 * np.pi * 60
    parasIBR1 = {
        'PsetPlant': 0.1, 'QsetPlant': 0.0,  # plant-level setpoints
        'wsetPlant': 1.0, 'VsetPlant': 1.0,  # plant-level setpoints
        'mpPlant': 1.00, 'mqPlant': 1.00,  # plant-level droop gains
        'KpPLLplant': 1.8, 'KiPLLplant': 160,  # plant-level PLL PI gains
        'KpPlantP': 0.10, 'KiPlantP': 6.00,  # plant-level active loop PI gains
        'KpPlantQ': 0.10, 'KiPlantQ': 6.00,  # plant-level reactive loop PI gains
        'wcpllPlant': 2 * np.pi * 100,  # plant-level PLL frequency filter cut-off frequency
        'wcPlant': 2 * np.pi * 1,  # plant-level power filter cut-off frequency
        'tDelay': 0.25,  # communication delay
        'wset': 1.0, 'Vset': 1.0,  # inverter-level setpoints
        'mp': 0.05, 'mq': 0.05,  # inverter-level droop gains
        'Rt': 0.02, 'Lt': 0.10,  # inverter LCL filter
        'Rd': 0.00, 'Cf': 0.05,  # inverter LCL filter
        'Rc': 0.10/4, 'Lc': 0.50/4,  # inverter LCL filter
        'KpV': 0.9, 'KiV': 8.0, #inverter-level voltage loop PI gains
        'KpC': 0.4, 'KiC':8.0,  #inverter-level current loop PI gains
        'wc': 2 * np.pi * 5 #inverter-level power filter cut-off frequency

    }

    parasIBR2 = {
        'PsetPlant': 0.1, 'Qset': 0.0,  # plant-level setpoints
        'wsetPlant': 1.0, 'VsetPlant': 1.0,  # plant-level setpoints
        'mpPlant': 1.00, 'mqPlant': 1.00,  # plant-level droop gains
        'KpPLLplant': 1.8, 'KiPLLplant': 160,  # plant-level PLL PI gains
        'KpPlantP': 0.10, 'KiPlantP': 6.00,  # plant-level active loop PI gains
        'KpPlantQ': 0.10, 'KiPlantQ': 6.00,  # plant-level reactive loop PI gains
        'wcpllPlant': 2 * np.pi * 100,  # plant-level PLL frequency filter cut-off frequency
        'wcPlant': 2 * np.pi * 1,  # plant-level power filter cut-off frequency
        'tDelay': 0.25,  # communication delay
        'wset': 1.0, 'Vset': 1.0,  # inverter-level setpoints
        'mp': 0.05, 'mq': 0.05,  # inverter-level droop gains
        'Rt': 0.02, 'Lt': 0.10,  # inverter LCL filter
        'Rd': 0.00, 'Cf': 0.05,  # inverter LCL filter
        'Rc': 0.10 / 4, 'Lc': 0.50 / 4,  # inverter LCL filter
        'KpV': 0.9, 'KiV': 8.0,  # inverter-level voltage loop PI gains
        'KpC': 0.4, 'KiC': 8.0,  # inverter-level current loop PI gains
        'wc': 2 * np.pi * 5  # inverter-level power filter cut-off frequency

    }

    parasLine1 = {
        'Rline': 0.10/4, 'Lline': 0.50/4,   #line parameters
    }

    parasLine2 = {
        'Rline': 0.10/4, 'Lline': 0.50/4,   #line parameters
    }

    parasLoad = {
        'Rload': 0.90, 'Lload': 0.4358, #load parameters
        'LoadRx': 100   #virtual resistance
    }




    # If user-defined parameters exist, update the default dictionary
    if user_params:
        for key in parasIBR1.keys():
            if key in user_params:
                parasIBR1[key] = user_params[key]

    if user_params:
        for key in parasIBR2.keys():
            if key in user_params:
                parasIBR2[key] = user_params[key]

    if user_params:
        for key in parasLine1.keys():
            if key in user_params:
                parasLine1[key] = user_params[key]

    if user_params:
        for key in parasLine2.keys():
            if key in user_params:
                parasLine2[key] = user_params[key]

    if user_params:
        for key in parasLoad.keys():
            if key in user_params:
                parasLoad[key] = user_params[key]

    # Column Names
    testResults = [["Parameter", "Eigenvalues", "maxRealValue", "minDampingRatio", "modalAnalysis", "pfExitFlag"]]

    # Run the simulation for a single set of parameters
    dominantParticipationFactorBoundary = 0.01
    Asys, steadyStateValuesX, eigenvalueAnalysisResults, pfExitFlag = (
        ssmodel_droop_droop(wbase, parasIBR1, parasIBR2, parasLine1, parasLine2, parasLoad, dominantParticipationFactorBoundary)
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
    results = main_droopPlant_droopPlant()
    print(results)
