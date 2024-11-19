import numpy as np
from scipy import linalg

def eigenvalue_analysis(Asys, ssVariables, dominantParticipationFactorBoundary):
    eigenvalueAnalysisResults = {}
    j = 0

    # Initialization
    eigenvalueAnalysisResults['modalAnalysis'] = [
        ["Mode", "Real Part", "Imag Part", "Oscillatory Frequency", "Damping Ratio", "Participation Factor", "Dominant Subpart"]
    ]

    # Modal Analysis
    eigs, Rvmat = linalg.eig(Asys)  # Returns eigenvalues and right eigenvectors
    maxRealValue = np.max(np.real(eigs))
    eigenvalueAnalysisResults['eigs'] = eigs
    eigenvalueAnalysisResults['maxRealValue'] = maxRealValue

    for i, eigi in enumerate(eigs):
        realParti = np.real(eigi)
        imagParti = np.imag(eigi)

        if imagParti >= 0:
            j += 1
            dampedOmega = np.sqrt(realParti**2 + imagParti**2)
            dampingRatio = -realParti / dampedOmega
            oscillatoryFrequency = abs(imagParti) / (2 * np.pi)

            modalAnalysis = [
                f"Mode {j}",
                realParti,
                imagParti,
                oscillatoryFrequency,
                dampingRatio,
                None,  # Placeholder for participation factor data
                None   # Placeholder for dominant subpart
            ]

            # Participation Factor Analysis
            participationFactorData = [
                ["State Location", "Participation Factor in Complex", "Participation Factor in Magnitude", "Dominant State Name", "Dominant Subpart"]
            ]

            # Calculate participation factors
            for k, rv in enumerate(Rvmat[:, i]):
                pf_magnitude = abs(rv)
                if pf_magnitude >= dominantParticipationFactorBoundary:
                    participationFactorData.append([
                        k,
                        rv,
                        pf_magnitude,
                        ssVariables[k],
                        None  # Placeholder for dominant subpart
                    ])

            modalAnalysis[5] = participationFactorData
            subPartsInfo = set(row[4] for row in participationFactorData[1:])
            modalAnalysis[6] = ' & '.join(filter(None, subPartsInfo))

            eigenvalueAnalysisResults['modalAnalysis'].append(modalAnalysis)

    minDampingRatio = min(row[4] for row in eigenvalueAnalysisResults['modalAnalysis'][1:])
    eigenvalueAnalysisResults['minDampingRatio'] = minDampingRatio

    return eigenvalueAnalysisResults