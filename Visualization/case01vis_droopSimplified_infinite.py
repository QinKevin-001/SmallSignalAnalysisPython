import streamlit as st
import numpy as np
import plotly.express as px
from Main import case01main_droopSimplified_infinite

# User input Limits
variable_ranges = {
    "Pset": (0.0, 1.0),
    "Qset": (-1.0, 1.0),
    "wset": (1.0, 1.0),
    "Vset": (0.9, 1.1),
    "mp": (0.01, 1.00),
    "mq": (0.01, 1.00),
    "Rc": (0.01, 1.0),
    "Lc": (0.01, 1.0),
    "wc": (round(2 * np.pi * 1, 2), round(2 * np.pi * 20, 2))
}

# Preloaded values
default_values = {
    'Pset': 1.0, 'Qset': 0.0,
    'wset': 1.0, 'Vset': 1.0,
    'mp': 0.05, 'mq': 0.05,
    'Rc': 0.04, 'Lc': 0.20,
    'wc': float(2 * np.pi * 5)
}

# Initialize session state
if "user_params" not in st.session_state:
    st.session_state.user_params = default_values.copy()
    # Initialize input values in session state
    for var in default_values:
        st.session_state[f"input_{var}"] = default_values[var]

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = 1


def get_user_inputs():
    """Creates user input controls inside the Simulation Parameters tab"""
    st.sidebar.header("Simulation Parameters")

    user_params = {}
    for var, (min_val, max_val) in variable_ranges.items():
        value = st.sidebar.number_input(
            f"{var} ({min_val} to {max_val})",
            min_value=float(min_val),
            max_value=float(max_val),
            value=float(st.session_state.user_params[var]),
            step=round((float(max_val) - float(min_val)) / 100, 3),
            key=f"input_{var}"
        )
        user_params[var] = value
        st.session_state.user_params[var] = value

    return user_params


def run_simulation(user_params):
    """Calls case01main_droopSimplified_infinite.py with updated parameters"""
    return case01main_droopSimplified_infinite.main_droopSimplified_infinite(user_params)


def visualization(testResults):
    """Generates plots based on testResults"""
    state_variables = [
        "Theta0", "Po0", "Qo0", "Iod0", "Ioq0"
    ]

    mode_data_raw = testResults[1][4]

    if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode':
        modes = mode_data_raw[1:]
    else:
        modes = mode_data_raw

    mode_range = len(modes)

    # Use session state for mode selection
    st.session_state.selected_mode = st.sidebar.slider(
        "Select a Mode",
        1, mode_range,
        st.session_state.selected_mode
    )
    mode_index = st.session_state.selected_mode - 1

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

    # Layout for Pie Chart and Heatmap
    col1, col2 = st.columns([1, 1])

    with col1:
        if factor_magnitudes:
            pie_chart_fig = px.pie(
                names=dominant_state_names,
                values=factor_magnitudes,
                title=f"Participation Factor Analysis of Mode {st.session_state.selected_mode}",
                width=900, height=700
            )
            st.plotly_chart(pie_chart_fig, use_container_width=True)
        else:
            st.warning("No participation factor data available for this mode.")

    with col2:
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


def run_simulation_and_visualization():
    """Runs the simulation and visualization process"""
    user_params = get_user_inputs()
    testResults = run_simulation(user_params)
    visualization(testResults)


def main():
    run_simulation_and_visualization()


if __name__ == "__main__":
    main()