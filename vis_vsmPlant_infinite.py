import streamlit as st
import numpy as np
import plotly.express as px
import main_vsmPlant_infinite  # Import simulation script for VSM Plant Infinite

# Set page layout if desired (uncomment to use wide layout)
# st.set_page_config(layout="wide")

# Updated Variable Limits for VSM Plant Infinite (Case 7)
variable_ranges = {
    "PsetPlant": (0.0, 1.0),
    "QsetPlant": (-1.0, 1.0),
    "wsetPlant": (1.0, 1.0),  # Fixed
    "VsetPlant": (0.9, 1.1),
    "KpPLLplant": (0.1, 10.0),
    "KiPLLplant": (0.1, 1000.0),
    "KpPlantP": (0.1, 10.0),
    "KiPlantP": (0.1, 100.0),
    "KpPlantQ": (0.1, 10.0),
    "KiPlantQ": (0.1, 100.0),
    "wcpllPlant": (round(2 * np.pi * 50, 2), round(2 * np.pi * 1000, 2)),
    "wcPlant": (round(2 * np.pi * 0.1, 2), round(2 * np.pi * 5, 2)),
    "tDelay": (0.1, 1.0),
    "wset": (1.0, 1.0),  # Fixed
    "Vset": (0.9, 1.1),
    "mp": (0.01, 1.00),
    "mq": (0.01, 1.00),
    "Rt": (0.01, 1.0),
    "Lt": (0.01, 1.0),
    "Rd": (0.0, 100.0),
    "Cf": (0.01, 0.20),
    "Rc": (0.01, 1.0),
    "Lc": (0.01, 1.0),
    "J": (1.0, 20.0),
    "K": (1.0, 100.0),
    "tauf": (0.01, 0.1)
}

# Default values (keys updated for consistency)
default_values = {
    "PsetPlant": 0.1,
    "QsetPlant": 0.1,
    "wsetPlant": 1.0,
    "VsetPlant": 1.0,
    "KpPLLplant": 1.8,
    "KiPLLplant": 160.0,
    "KpPlantP": 0.12,
    "KiPlantP": 0.50,
    "KpPlantQ": 1.25,
    "KiPlantQ": 5.00,
    "wcpllPlant": float(2 * np.pi * 100),
    "wcPlant": float(2 * np.pi * 1),
    "tDelay": 0.25,
    "wset": 1.0,
    "Vset": 1.0,
    "mp": 0.05,
    "mq": 0.05,
    "Rt": 0.02,
    "Lt": 0.10,
    "Rd": 10.00,
    "Cf": 0.05,
    "Rc": 0.10,
    "Lc": 0.50,
    "J": 10.0,
    "K": 12.0,
    "tauf": 0.01
}

def get_user_inputs():
    """Creates user input controls for parameter tuning via the sidebar."""
    st.sidebar.header("Simulation Parameters")
    user_params = {}

    for var, (min_val, max_val) in variable_ranges.items():
        # Use the default value if available, otherwise use the mid-point.
        default = default_values.get(var, round((min_val + max_val) / 2.0, 2))
        user_params[var] = st.sidebar.number_input(
            f"{var} ({min_val} to {max_val})",
            min_value=min_val,
            max_value=max_val,
            value=default,
            step=round((max_val - min_val) / 1000, 2)
        )

    return user_params

def run_simulation(user_params):
    """Runs the VSM simulation with the current parameters."""
    return main_vsmPlant_infinite.main_vsmPlant_infinite(user_params)

def visualization(testResults):
    """Generates the eigenvalue and participation factor plots based on simulation output."""
    state_variables = [
        "thetaPlant0", "epsilonPLL0", "wPlant0", "epsilonP0", "epsilonQ0",
        "PoPlant0", "QoPlant0", "Theta0", "Po0", "Qo0", "Phid0", "Phiq0",
        "Gammad0", "Gammaq0", "Iid0", "Iiq0", "Vcd0", "Vcq0", "Iod0", "Ioq0"
    ]

    # The modal analysis data is expected to be stored at index 4 of the second element.
    mode_data_raw = testResults[1][4]

    # If the first entry is a header, skip it.
    if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode':
        modes = mode_data_raw[1:]
    else:
        modes = mode_data_raw

    mode_range = len(modes)

    # Allow user to select a mode for closer inspection.
    selected_mode = st.sidebar.slider("Select a Mode", 1, mode_range, 1)
    mode_index = selected_mode - 1

    parameter_data = testResults[1]
    try:
        eigenvalue_real = np.real(parameter_data[1][mode_index])
        eigenvalue_imag = np.imag(parameter_data[1][mode_index])
    except IndexError:
        st.error("Eigenvalue data is unavailable.")
        return

    try:
        # Participation factors are assumed to be in the 6th entry of each mode's data.
        participation_factors = modes[mode_index][5] if len(modes[mode_index]) > 5 else []
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

    # Layout the plots in two equal columns.
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(f"Participation Factor Distribution for Mode {selected_mode}")
        if factor_magnitudes:
            pie_chart_fig = px.pie(
                names=dominant_state_names,
                values=factor_magnitudes,
                title=f"Participation Factor Distribution for Mode {selected_mode}",
                width=900, height=700
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
            title="Participation Factors Heatmap",
            width=900, height=700
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)

def main():
    """Main function to handle user inputs, simulation, and visualization."""
    st.title("VSM Plant Infinite System Analysis")
    user_params = get_user_inputs()
    testResults = run_simulation(user_params)  # Run simulation with current parameters
    visualization(testResults)                # Generate updated plots

# Expose the main function for multipage navigation.
if __name__ == "__main__":
    main()
