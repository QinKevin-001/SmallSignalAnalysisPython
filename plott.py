import numpy as np
import matplotlib.pyplot as plt

def plott(testResults):
    """
    Plot all eigenvalues from the test results and print each eigenvalue.
    """
    totalNum = len(testResults) - 1
    plt.figure(figsize=(6, 4))

    for i in range(totalNum):
        eigsi = testResults[i + 1][1]  # Extract eigenvalues list for each parameter set
        print(f"Parameter set {i + 1}, mp: {testResults[i + 1][0]}")  # Print the parameter set details

        for eig in eigsi:  # Loop over each eigenvalue in the list
            # Print the real and imaginary parts of the eigenvalue being plotted
            print(f"Eigenvalue: Real part = {np.real(eig)}, Imaginary part = {np.imag(eig)}")

            plt.plot(
                np.real(eig),
                np.imag(eig),
                'd',
                color=(i / totalNum, 0, 0),  # Gradient color
                markersize=8
            )

    plt.xlabel("Real")
    plt.ylabel("Imag")
    plt.xlim([-30, 2])  # Set appropriate range for best visualization
    plt.ylim([-2 * np.pi * 10, 2 * np.pi * 10])  # Set appropriate range for best visualization
    plt.grid(True)
    plt.gca().tick_params(axis='both', which='major', labelsize=14)
    plt.tight_layout()
    plt.show()