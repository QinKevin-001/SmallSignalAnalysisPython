import streamlit as st
import numpy as np
import plotly.express as px
import main_droop_infinite  # Import simulation script without circular dependency

# Updated Variable Limits
variable_ranges = {
    "Pset": (0.0, 1.0),
    "Qset": (-1.0, 1.0),
    "ωset": (1.0, 1.0),  # Fixed
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
    "ωc": (round(2 * np.pi * 1, 2), round(2 * np.pi * 20, 2))  # Rounded 6.28 to 125.66
}

# Default values (from `main_droop_infinite.py`)
default_values = {
    "Pset": 1.0, "Qset": 0.0,
    "ωset": 1.0, "Vset": 1.0,
    "mp": 0.05, "mq": 0.05,
    "Rt": 0.02, "Lt": 0.10,
    "Rd": 0.00, "Cf": 0.05,
    "Rc": 0.10, "Lc": 0.50,
    "KpV": 1.8, "KiV": 160,
    "KpC": 0.4, "KiC": 8.0,
    "ωc": float(2 * np.pi * 5)
}

def get_user_inputs():
    """Creates user input controls for variable tuning inside the 'Simulation Parameters' tab."""
    st.sidebar.header("Simulation Parameters")
    user_params = {}

    for var, (min_val, max_val) in variable_ranges.items():
        user_params[var] = st.sidebar.number_input(
            f"{var} ({min_val} to {max_val})",
            min_value=min_val,
            max_value=max_val,
            value=default_values[var],  # Use predefined default values
            step=round((max_val - min_val) / 100, 3)
        )

    # Store the user parameters in the session state
    st.session_state["user_params"] = user_params
    return user_params

def run_simulation(user_params):
    """Runs the simulation using the parameters selected by the user."""
    return main_droop_infinite.main_droop_infinite(user_params)

def visualization(testResults):
    """Generates plots based on testResults."""
    state_variables = [
        "Theta0", "Po0", "Qo0", "Phid0", "Phiq0", "Gammad0", "Gammaq0",
        "Iid0", "Iiq0", "Vcd0", "Vcq0", "Iod0", "Ioq0"
    ]

    mode_data_raw = testResults[1][4]

    if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode':
        modes = mode_data_raw[1:]
    else:
        modes = mode_data_raw

    mode_range = len(modes)

    selected_mode = st.sidebar.slider("Select a Mode", 1, mode_range, 1)
    mode_index = selected_mode - 1

    parameter_data = testResults[1]
    try:
        mode_data = modes[mode_index]
    except IndexError:
        st.error("Mode data is unavailable.")
        return

    try:
        eigenvalue_real = np.real(parameter_data[1][mode_index])
        eigenvalue_imag = np.imag(parameter_data[1][mode_index])
    except IndexError:
        st.error("Eigenvalue data is unavailable.")
        return

    try:
        participation_factors = mode_data[5] if len(mode_data) > 5 else []
        if participation_factors:
            valid_factors = [
                entry for entry in participation_factors
                if isinstance(entry[0], (int, np.integer)) and 1 <= entry[0] <= len(state_variables)
            ]
            state_locations = [entry[0] for entry in valid_factors]
            factor_magnitudes = [entry[2] for entry in valid_factors]
            dominant_state_names = [state_variables[loc - 1] for loc in state_locations]
        else:
            factor_magnitudes = []
            dominant_state_names = []
    except (IndexError, ValueError, TypeError):
        st.error("Error parsing participation factors.")
        return

    # Layout for Pie Chart and Heatmap (Full Width)
    col1, col2 = st.columns([1, 1])  # Equal width columns

    with col1:
        st.subheader(f"Participation Factor Distribution for Mode {selected_mode}")
        if factor_magnitudes:
            pie_chart_fig = px.pie(
                names=dominant_state_names,
                values=factor_magnitudes,
                title=f"Participation Factor Distribution for Mode {selected_mode}",
                width=1000, height=800  # Increased size
            )
            st.plotly_chart(pie_chart_fig, use_container_width=True)
        else:
            st.warning("No participation factor data available for this mode.")

    with col2:
        st.subheader("Heatmap of Participation Factors for All Modes")
        heatmap_data = []
        for mode_idx in range(mode_range):
            mode_values = np.zeros(len(state_variables))
            try:
                mode_participation = modes[mode_idx][5]
                for entry in mode_participation:
                    if isinstance(entry[0], (int, np.integer)) and 1 <= entry[0] <= len(state_variables):
                        mode_values[entry[0] - 1] = entry[2]
            except (IndexError, ValueError):
                pass
            heatmap_data.append(mode_values)

        mode_labels = [f"Mode {i + 1}" for i in range(mode_range)]
        heatmap_fig = px.imshow(
            np.array(heatmap_data).T,
            x=mode_labels,
            y=state_variables,
            labels={"color": "Participation Factor"},
            color_continuous_scale="Blues",
            title=f"Participation Factors Heatmap",
            width=1000, height=800  # Increased size
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)

def run_simulation_and_visualization():
    """Runs the simulation and updates the visualization dynamically."""
    user_params = st.session_state.get("user_params", None)

    if user_params is not None:
        testResults = run_simulation(user_params)
        visualization(testResults)

def main():
    """Main function to handle user input, simulation, and visualization dynamically."""
    st.title("Droop Infinite System Analysis")
    run_simulation_and_visualization()  # Run only simulation & visualization

if __name__ == "__main__":
    main()
