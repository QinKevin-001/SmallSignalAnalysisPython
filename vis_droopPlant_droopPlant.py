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
default_values = {key: (min_val + max_val) / 2 for key, (min_val, max_val) in variable_ranges.items()}


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

    st.subheader("Participation Factor Distribution")
    mode_data_raw = testResults[1][4]
    modes = mode_data_raw[1:] if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode' else mode_data_raw
    mode_range = len(modes)

    if mode_range > 0:
        participation_factors = modes[0][5] if len(modes[0]) > 5 else []
        valid_factors = [(entry[0], float(entry[2])) for entry in participation_factors if isinstance(entry[0], int)]

        if valid_factors:
            factor_magnitudes = [entry[1] for entry in valid_factors]
            dominant_state_names = [f"State {entry[0]}" for entry in valid_factors]

            pie_chart_fig = px.pie(
                names=dominant_state_names,
                values=factor_magnitudes,
                title="Participation Factors",
                width=800,
                height=600
            )
            st.plotly_chart(pie_chart_fig, use_container_width=True)


# ----------------- 📌 Run Simulation & Visualization ----------------- #
def run_simulation_and_visualization():
    """Runs the simulation and displays results."""
    user_params = get_user_inputs()
    testResults = run_simulation(user_params)
    visualization(testResults)


# ----------------- 📌 Main Function ----------------- #
def main():
    st.title("DroopPlant + DroopPlant System Analysis")
    run_simulation_and_visualization()


# Ensure it runs when called from `vis_main.py`
if __name__ == "__main__":
    main()
