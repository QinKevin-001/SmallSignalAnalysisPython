import streamlit as st
import numpy as np
import plotly.express as px
from Main import case09main_droopPlant_droopPlant

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
    "ωset": (1.0, 1.0),
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
    "Rx": (100, 1000),
    "Rline": (0.01, 1.0),
    "Lline": (0.01, 1.0)
}

# Default values from `case09main_droopPlant_droopPlant.py`
default_values = {
    "PsetPlant": 0.1, "QsetPlant": 0.0, "ωsetPlant": 1.0, "VsetPlant": 1.0,
    "KpPLLPlant": 1.8, "KiPLLPlant": 160.0, "KpPlantP": 0.1, "KiPlantP": 6.0,
    "KpPlantQ": 0.1, "KiPlantQ": 6.0, "ωcPLLPlant": float(2 * np.pi * 100),
    "ωcPlant": float(2 * np.pi * 1), "tDelay": 0.25, "ωset": 1.0,
    "Vset": 1.0, "mp": 0.05, "mq": 0.05, "Rt": 0.02, "Lt": 0.10,
    "Rd": 0.00, "Cf": 0.05, "Rc": 0.10 / 4, "Lc": 0.50 / 4,
    "KpV": 0.9, "KiV": 8.0, "KpC": 0.4, "KiC": 8.0,
    "ωc": float(2 * np.pi * 5), "Rload": 0.90, "Lload": 0.4358,
    "Rx": 100, "Rline": 0.10 / 4, "Lline": 0.50 / 4
}


# ----------------- 📌 Sidebar: Simulation Parameters ----------------- #
def get_user_inputs():
    """Creates user input controls inside the Simulation Parameters tab, ensuring unique widget keys."""

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


# ----------------- 📌 Sidebar: Mode Selection ----------------- #
def get_mode_selection(mode_range):
    """Creates a mode selection dropdown inside the sidebar."""
    st.sidebar.header("Mode Selection")
    selected_mode = st.sidebar.slider("Select a Mode", 1, mode_range, 1, key="mode_slider")
    return selected_mode - 1  # Convert to zero-based index


# ----------------- 📌 Simulation Execution ----------------- #
def run_simulation(user_params):
    """Runs the simulation using the selected parameters."""
    return case09main_droopPlant_droopPlant.main_droopPlant_droopPlant(user_params)


# ----------------- 📌 Visualization ----------------- #
def visualization(testResults):
    """Generates the eigenvalue and participation factor plots based on simulation output."""
    state_variables = [
        'epsilonPLLPlant(IBR1)', 'wPlant(IBR1)', 'epsilonP(IBR1)', 'epsilonQ(IBR1)', 'PoPlant(IBR1)', 'QoPlant(IBR1)',
        'PsetDelay(IBR1)', 'QsetDelay(IBR1)', 'theta(IBR1)', 'Po(IBR1)', 'Qo(IBR1)', 'phid(IBR1)', 'phiq(IBR1)',
        'gammad(IBR1)', 'gammaq(IBR1)', 'iid(IBR1)', 'iiq(IBR1)', 'vcd(IBR1)', 'vcq(IBR1)', 'iod(IBR1)', 'ioq(IBR1)',
        'thetaPlant(IBR2)', 'epsilonPLLPlant(IBR2)', 'wPlant(IBR2)', 'epsilonP(IBR2)', 'epsilonQ(IBR2)', 'PoPlant(IBR2)',
        'QoPlant(IBR2)', 'PsetDelay(IBR2)', 'QsetDelay(IBR2)', 'theta(IBR2)', 'Po(IBR2)', 'Qo(IBR2)', 'phid(IBR2)',
        'phiq(IBR2)', 'gammad(IBR2)', 'gammaq(IBR2)', 'iid(IBR2)', 'iiq(IBR2)', 'vcd(IBR2)', 'vcq(IBR2)', 'iod(IBR2)', 'ioq(IBR2)',
        'ilineD(Line1)', 'ilineQ(Line1)'
        'ilineD(Line2)', 'ilineQ(Line2)'
        'iloadD(Load)', 'iloadQ(Load)'
    ]

    # The modal analysis data is expected to be stored at index 4 of the second element
    mode_data_raw = testResults[1][4]

    # If the first entry is a header, skip it
    if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode':
        modes = mode_data_raw[1:]
    else:
        modes = mode_data_raw

    mode_range = len(modes)

    # Allow user to select a mode for closer inspection
    selected_mode = st.sidebar.slider(
        "Select a Mode",
        1,
        mode_range,
        1,
        key="mode_selector"  # Add unique key for mode selector
    )
    mode_index = selected_mode - 1

    parameter_data = testResults[1]
    try:
        eigenvalue_real = np.real(parameter_data[1][mode_index])
        eigenvalue_imag = np.imag(parameter_data[1][mode_index])
    except IndexError:
        st.error("Eigenvalue data is unavailable.")
        return

    try:
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

    # Layout the plots in two equal columns
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

# ----------------- 📌 Run Simulation & Visualization ----------------- #
def run_simulation_and_visualization():
    """Runs the simulation and visualization process, ensuring parameters are not duplicated."""
    user_params = get_user_inputs()  # Get user parameters
    testResults = run_simulation(user_params)  # Run simulation
    visualization(testResults)  # Show visualization

# ----------------- 📌 Main Page Layout ----------------- #
def main():
    st.title("Droop Plant + Droop Plant System Analysis")
    run_simulation_and_visualization()


if __name__ == "__main__":
    main()
