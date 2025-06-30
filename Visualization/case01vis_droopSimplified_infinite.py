import streamlit as st
import numpy as np
import plotly.express as px
from Main import case01main_droopSimplified_infinite

# User input Limits
variable_ranges = {
    "Pset": (0.0, 1.0), "Qset": (-1.0, 1.0),
    "wset": (1.0, 1.0), "Vset": (0.9, 1.1),
    "mp": (0.01, 1.00), "mq": (0.01, 1.00),
    "Rc": (0.01, 1.0),  "Lc": (0.01, 1.0),
    "wc": (round(2 * np.pi * 1, 2), round(2 * np.pi * 20, 2))
}

# Preloaded values
default_values = {
    'Pset': 1.0, 'Qset': 0.0,
    'wset': 1.0, 'Vset': 1.0,
    'mp': 0.05,  'mq': 0.05,
    'Rc': 0.04,  'Lc': 0.20,
    'wc': float(2 * np.pi * 5)
}

# Initialize session state
for key in default_values:
    if key not in st.session_state:
        st.session_state[key] = default_values[key]
if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = 1

def update_param(key):
    st.session_state["needs_rerun"] = True

def get_user_inputs():
    """Creates user input controls inside the Simulation Parameters tab"""
    st.sidebar.header("Simulation Parameters")
    user_params = {}
    for var, (min_val, max_val) in variable_ranges.items():
        step = round((float(max_val) - float(min_val)) / 100, 3)
        # numeric input box
        user_params[var] = st.sidebar.number_input(
            f"{var} ({min_val} to {max_val})",
            min_value=float(min_val),
            max_value=float(max_val),
            value=st.session_state[var],
            step=step,
            key=var,
            on_change=update_param,
            args=(var,),
        )
        if max_val != min_val:
            slider_key = f"{var}_slider"
            slider_val = st.sidebar.slider(
                "",
                min_val, max_val, float(st.session_state[var]),
                step=max(step, 0.001),
                key=slider_key,
                on_change=update_param,
                args=(var,),
            )
            # keep numeric input and slider synchronized
            if slider_val != st.session_state[var]:
                st.session_state[var] = slider_val
                user_params[var] = slider_val
    return user_params

def run_simulation(user_params):
    return case01main_droopSimplified_infinite.main_droopSimplified_infinite(user_params)

def visualization(testResults):
    state_variables = [
        "Theta0", "Po0", "Qo0", "Iod0", "Ioq0"
    ]
    mode_data_raw = testResults[1][4]
    modes = mode_data_raw[1:] if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode' else mode_data_raw
    mode_range = len(modes)

    # Use session state for mode selection
    selected_mode = st.sidebar.slider(
        "Select a Mode",
        1, mode_range,
        st.session_state.selected_mode,
        key="mode_slider"
    )
    st.session_state.selected_mode = selected_mode
    mode_index = selected_mode - 1
    parameter_data = testResults[1]
    mode_data = modes[mode_index]
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

    # Layout for Pie Chart and Heatmap
    col1, col2 = st.columns([1, 1])
    with col1:
        if factor_magnitudes:
            pie_chart_fig = px.pie(
                names=dominant_state_names,
                values=factor_magnitudes,
                title=f"Participation Factor Analysis of Mode {selected_mode}",
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
        mode_labels = list(range(1, mode_range + 1))
        heatmap_fig = px.imshow(
            np.array(heatmap_data).T,
            x=mode_labels,
            y=state_variables,
            labels={
                "x": "Modes",
                "y": "State Variables",
                "color": "Participation Factor"
            },
            color_continuous_scale="Blues",
            title="Participation Factors Heatmap",
            width=900, height=700
        )
        heatmap_fig.update_xaxes(tickmode='linear', tick0=1, dtick=1)
        st.plotly_chart(heatmap_fig, use_container_width=True)

def run_simulation_and_visualization():
    """Runs the simulation and visualization process"""
    user_params = get_user_inputs()
    testResults = run_simulation(user_params)
    visualization(testResults)

def main():
    if "needs_rerun" not in st.session_state:
        st.session_state["needs_rerun"] = False
    run_simulation_and_visualization()
    if st.session_state.get("needs_rerun", False):
        st.session_state["needs_rerun"] = False
        st.rerun()

if __name__ == "__main__":
    main()