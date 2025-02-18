# Test confirmed

import streamlit as st
import numpy as np
import plotly.express as px
import main_droopPlant_droopPlant  # Import simulation script

# ----------------- 📌 Define Parameter Limits ----------------- #
variable_ranges = {
    "PsetPlant": (0.0, 1.0),
    "QsetPlant": (-1.0, 1.0),
    "ωsetPlant": (1.0, 1.0),
    "VsetPlant": (0.9, 1.1),
    "KpPLLPlant": (0.1, 10.0),
    "KiPLLPlant": (0.1, 1000.0),
    "KpPlantP": (0.1, 10.0),
    "KiPlantP": (0.1, 100.0),
    "KpPlantQ": (0.1, 10.0),
    "KiPlantQ": (0.1, 100.0),
    "ωcPLLPlant": (float(2 * np.pi * 50), float(2 * np.pi * 1000)),
    "ωcPlant": (float(2 * np.pi * 0.1), float(2 * np.pi * 5)),
    "tDelay": (0.1, 1.0),
    "Vset": (0.9, 1.1),
    "mp": (0.01, 1.00),
    "mq": (0.01, 1.00),
    "Rt": (0.01, 1.0),
    "Lt": (0.01, 1.0),
    "Rd": (0.0, 100.0),
    "Cf": (0.01, 0.20),
    "Rc": (0.01, 1.0),
    "Lc": (0.01, 1.0),
    "KpV": (0.1, 10.0),
    "KiV": (0.1, 1000.0),
    "KpC": (0.1, 10.0),
    "KiC": (0.1, 1000.0),
    "ωc": (float(2 * np.pi * 1), float(2 * np.pi * 20)),
    "Rload": (0.5, 10.0),
    "Lload": (0.1, 10.0),
    "Rx": (100.0, 1000.0),
    "Rline": (0.01, 1.0),
    "Lline": (0.01, 1.0)
}

# Default values from `main_droopPlant_droopPlant.py`
default_values = {
    "PsetPlant": 0.1, "QsetPlant": 0.0,
    "ωsetPlant": 1.0, "VsetPlant": 1.0,
    "KpPLLPlant": 1.8, "KiPLLPlant": 160.0,
    "KpPlantP": 0.1, "KiPlantP": 6.0,
    "KpPlantQ": 0.1, "KiPlantQ": 6.0,
    "ωcPLLPlant": float(2 * np.pi * 100),
    "ωcPlant": float(2 * np.pi * 1),
    "tDelay": 0.25,
    "Vset": 1.0, "mp": 0.05, "mq": 0.05,
    "Rt": 0.02, "Lt": 0.10,
    "Rd": 0.00, "Cf": 0.05,
    "Rc": 0.10, "Lc": 0.50,
    "KpV": 0.9, "KiV": 8.0,
    "KpC": 0.4, "KiC": 8.0,
    "ωc": float(2 * np.pi * 5),
    "Rload": 0.9, "Lload": 0.4358, "Rx": 100,
    "Rline": 0.10, "Lline": 0.50
}


# ----------------- 📌 Sidebar: Simulation Parameters ----------------- #
def get_user_inputs():
    """Creates user input controls inside the Simulation Parameters tab."""
    if "user_params" not in st.session_state:
        st.session_state["user_params"] = {key: default_values[key] for key in variable_ranges}

    user_params = {}

    st.sidebar.header("Simulation Parameters")
    for var, (min_val, max_val) in variable_ranges.items():
        user_params[var] = st.sidebar.number_input(
            f"{var} ({min_val} to {max_val})",
            min_value=float(min_val),
            max_value=float(max_val),
            value=float(st.session_state["user_params"].get(var, default_values[var])),
            step=round((float(max_val) - float(min_val)) / 100, 3),
            key=f"param_{var}"
        )

    st.session_state["user_params"] = user_params
    return user_params


# ----------------- 📌 Simulation Execution ----------------- #
def run_simulation(user_params):
    """Runs the simulation using the selected parameters."""
    return main_droopPlant_droopPlant.main_droopPlant_droopPlant(user_params)


# ----------------- 📌 Visualization ----------------- #
def visualization(testResults):
    """Generates plots based on testResults."""
    st.title("Droop Plant + Droop Plant System Analysis")
    st.write("Analyzing stability and modal response of the Droop Plant + Droop Plant system.")

    st.subheader("Eigenvalue Analysis")
    st.write("Real and Imaginary parts of dominant eigenvalues:")

    eigenvalues = testResults[1][1]
    st.write(eigenvalues)


# ----------------- 📌 Run Simulation & Visualization ----------------- #
def run_simulation_and_visualization():
    """Runs the simulation and displays results."""
    user_params = get_user_inputs()
    testResults = run_simulation(user_params)
    visualization(testResults)


# ----------------- 📌 Add the `main()` Function ----------------- #
def main():
    st.title("DroopPlant + DroopPlant System Analysis")
    run_simulation_and_visualization()


# Ensure it runs when called from `vis_main.py`
if __name__ == "__main__":
    main()
