#critical imports

#optional imports

def main_droopPlant_sg(user_params=None):
    #parameters
    wbase = 2 * np.pi * 60
    parasIBR = {
        'PsetPlant': 0.1, 'Qset': 0.0,  # plant-level setpoints
        'wsetPlant': 1.0, 'VsetPlant': 1.0,  # plant-level setpoints
        'mpPlant': 1.00, 'mqPlant': 1.00,  # plant-level droop gains
        'KpPLLplant': 1.8/10, 'KiPLLplant': 160/10,  # plant-level PLL PI gains
        'KpPlantP': 0.15, 'KiPlantP': 0.80,  # plant-level active loop PI gains
        'KpPlantQ': 0.10, 'KiPlantQ': 3.00,  # plant-level reactive loop PI gains
        'wcpllPlant': 2 * np.pi * 100,  # plant-level PLL frequency filter cut-off frequency
        'wcPlant': 2 * np.pi * 1,  # plant-level power filter cut-off frequency
        'tDelay': 0.25,  # communication delay
        'wset': 1.0, 'Vset': 1.0,  # inverter-level setpoints
        'mp': 0.05, 'mq': 0.05,  # inverter-level droop gains
        'Rt': 0.02, 'Lt': 0.10,  #LCL filter
        'Rd': 0.00, 'Cf': 0.05,  #LCL filter
        'Rc': 0.10, 'Lc': 0.50,  #LCL filter
        'KpV': 1.0, 'KiV': 10.0, #inverter-level voltage loop PI gains
        'KpC': 0.4, 'KiC':8.0,  #inverter-level current loop PI gains
        'wc': 2 * np.pi * 5 #inverter-level power filter cut-off frequency

    }

    parasSG = {
        'Pset': 0.1, 'Qset': 0.0,  # setpoints
        'wset': 1.0, 'Vset': 1,  # setpoints
        'mp': 0.05, 'mq': np.inf,  # droop gains
        'Rs': 0,  # SG parameters
        'Ld': 1.855, 'Ld1': 0.226, 'Ld2': 0.165,  # SG parameters
        'Lq': 0.936, 'Lq1': 0.300, 'Lq2': 0.165,  # SG parameters
        'Ll': 0.100,  # SG parameters
        'Tdo1': 8.71, 'Tdo2': 0.05,  # time constants
        'Tqo1': 0.70, 'Tqo2': 0.04,  # time constants
        'H': 5.0,  # inertia constant
        'D': 0.0,  # damping coefficient
        'T1': 0.05, 'T2': 0.00, 'T3': 0.30, 'T4': 0.15, 'T5': 0.30,  # time constants
        'K1': 0.60, 'K2': 0.40, 'Ke': 200,  # Gains
        'Ta': 1.00, 'Tb': 10.0, 'Te': 0.05  # time constants

    }
    # Now assign Kg after 'mp' is available
    parasSG['Kg'] = 1 / parasSG['mp']  # frequency droop parameters

    parasLine1 = {
        'Rline': 0.10, 'Lline': 0.50, #line parameters

    }

    parasLine2 = {
        'Rline': 0.10, 'Lline': 0.50,  #line parameters

    }

    parasLoad = {
        'Rload': 0.90, 'Lload': 0.4358,  #load parameters
        'Rx': 100   #virtual resistancce

    }

    # If user-defined parameters exist, update the default dictionary
    if user_params:
        for key in parasIBR.keys():
            if key in user_params:
                parasIBR[key] = user_params[key]

    if user_params:
        for key in parasSG.keys():
            if key in user_params:
                parasSG[key] = user_params[key]

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
        ssmodel_droopPlant_sg(wbase, parasIBR, parasSG, parasLine1, parasLine2, parasLoad, dominantParticipationFactorBoundary)
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
    results = main_droopPlant_sg()
    print(results)
