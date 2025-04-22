import streamlit as st
import numpy as np
import plotly.express as px
from Main import case08main_droop_droop

# User input Limits
variable_ranges = {
    # IBR1 parameters
    "Pset": (0.0, 1.0), "Qset": (-1.0, 1.0),
    "wset": (1.0, 1.0), "Vset": (0.9, 1.1),
    "mp": (0.01, 1.00), "mq": (0.01, 1.00),
    "Rt": (0.01, 1.0),  "Lt": (0.01, 1.0),
    "Rd": (0.0, 100.0), "Cf": (0.01, 0.20),
    "Rc": (0.01, 1.0),  "Lc": (0.01, 1.0),
    "KpV": (0.1, 10.0), "KiV": (0.1, 1000.0),
    "KpC": (0.1, 10.0), "KiC": (0.1, 1000.0),
    "wc": (float(2 * np.pi * 1), float(2 * np.pi * 20)),
    # IBR2 parameters
    "Pset_IBR2": (0.0, 1.0), "Qset_IBR2": (-1.0, 1.0),
    "wset_IBR2": (1.0, 1.0), "Vset_IBR2": (0.9, 1.1),
    "mp_IBR2": (0.01, 1.00), "mq_IBR2": (0.01, 1.00),
    "Rt_IBR2": (0.01, 1.0),  "Lt_IBR2": (0.01, 1.0),
    "Rd_IBR2": (0.0, 100.0), "Cf_IBR2": (0.01, 0.20),
    "Rc_IBR2": (0.01, 1.0),  "Lc_IBR2": (0.01, 1.0),
    "KpV_IBR2": (0.1, 10.0), "KiV_IBR2": (0.1, 1000.0),
    "KpC_IBR2": (0.1, 10.0), "KiC_IBR2": (0.1, 1000.0),
    "wc_IBR2": (float(2 * np.pi * 1), float(2 * np.pi * 20)),
    # Load parameters
    "Rload": (0.5, 10.0),    "Lload": (0.1, 10.0),
    "Rx": (100.0, 1000.0)
}

# Default values
default_values = {
    # IBR1 parameters
    "Pset": 0.1,      "Qset": 0.0,
    "wset": 1.0,      "Vset": 1.0,
    "mp": 0.05,       "mq": 0.05,
    "Rt": 0.02,       "Lt": 0.10,
    "Rd": 0.00,       "Cf": 0.05,
    "Rc": 0.10,       "Lc": 0.50,
    "KpV": 4.0,       "KiV": 15.0,
    "KpC": 0.4,       "KiC": 8.0,
    "wc": float(2 * np.pi * 5),
    # IBR2 parameters
    "Pset_IBR2": 0.1, "Qset_IBR2": 0.0,
    "wset_IBR2": 1.0, "Vset_IBR2": 1.0,
    "mp_IBR2": 0.05,  "mq_IBR2": 0.05,
    "Rt_IBR2": 0.02,  "Lt_IBR2": 0.10,
    "Rd_IBR2": 0.00,  "Cf_IBR2": 0.05,
    "Rc_IBR2": 0.10,  "Lc_IBR2": 0.50,
    "KpV_IBR2": 4.0,  "KiV_IBR2": 15.0,
    "KpC_IBR2": 0.4,  "KiC_IBR2": 8.0,
    "wc_IBR2": float(2 * np.pi * 5),
    # Load parameters
    "Rload": 0.9,     "Lload": 0.4358,
    "Rx": 100.0
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
    # Create tabs for different parameter groups
    ibr1_tab, ibr2_tab, load_tab = st.sidebar.tabs(["IBR1", "IBR2", "Load"])
    user_params = {}
    # IBR1 Parameters
    with ibr1_tab:
        ibr1_params = [param for param in variable_ranges.keys() if
                      not param.endswith('_IBR2') and param not in ['Rload', 'Lload', 'Rx']]
        for var in ibr1_params:
            step = float(round((float(variable_ranges[var][1]) - float(variable_ranges[var][0])) / 100, 3))
            user_params[var] = st.number_input(
                f"{var} ({variable_ranges[var][0]} to {variable_ranges[var][1]})",
                min_value=float(variable_ranges[var][0]),
                max_value=float(variable_ranges[var][1]),
                value=float(st.session_state[var]),
                step=step,
                key=var,
                on_change=update_param,
                args=(var,)
            )
    # IBR2 Parameters
    with ibr2_tab:
        ibr2_params = [param for param in variable_ranges.keys() if param.endswith('_IBR2')]
        for var in ibr2_params:
            step = float(round((float(variable_ranges[var][1]) - float(variable_ranges[var][0])) / 100, 3))
            user_params[var] = st.number_input(
                f"{var.replace('_IBR2', '')} ({variable_ranges[var][0]} to {variable_ranges[var][1]})",
                min_value=float(variable_ranges[var][0]),
                max_value=float(variable_ranges[var][1]),
                value=float(st.session_state[var]),
                step=step,
                key=var,
                on_change=update_param,
                args=(var,)
            )
    # Load Parameters
    with load_tab:
        load_params = ['Rload', 'Lload', 'Rx']
        for var in load_params:
            step = float(round((float(variable_ranges[var][1]) - float(variable_ranges[var][0])) / 100, 3))
            user_params[var] = st.number_input(
                f"{var} ({variable_ranges[var][0]} to {variable_ranges[var][1]})",
                min_value=float(variable_ranges[var][0]),
                max_value=float(variable_ranges[var][1]),
                value=float(st.session_state[var]),
                step=step,
                key=var,
                on_change=update_param,
                args=(var,)
            )
    return user_params

def prepare_simulation_parameters(user_params):
    """Prepares the parameters in the format expected by the simulation function."""
    ibr1_params = {}
    ibr2_params = {}
    load_params = {}

    for key, value in user_params.items():
        if key.endswith('_IBR2'):
            ibr2_params[key.replace('_IBR2', '')] = value
        elif key in ['Rload', 'Lload', 'Rx']:
            load_params[key] = value
        else:
            ibr1_params[key] = value

    return {
        'parasIBR1': ibr1_params,
        'parasIBR2': ibr2_params,
        'parasLoad': load_params
    }

def run_simulation(user_params):
    sim_params = prepare_simulation_parameters(user_params)
    return case08main_droop_droop.main_droop_droop(sim_params)

def visualization(testResults):
    state_variables = [
        'Po(IBR1)', 'Qo(IBR1)', 'phid(IBR1)', 'phiq(IBR1)', 'gammad(IBR1)', 'gammaq(IBR1)', 'iid(IBR1)',
        'iiq(IBR1)', 'vcd(IBR1)', 'vcq(IBR1)', 'iod(IBR1)', 'ioq(IBR1)',
        'theta(IBR2)', 'Po(IBR2)', 'Qo(IBR2)', 'phid(IBR2)', 'phiq(IBR2)', 'gammad(IBR2)', 'gammaq(IBR2)', 'iid(IBR2)',
        'iiq(IBR2)', 'vcd(IBR2)', 'vcq(IBR2)', 'iod(IBR2)', 'ioq(IBR2)',
        'iloadD(Load)', 'iloadQ(Load)'
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
            mode_participation = modes[mode_idx][5]
            for entry in mode_participation:
                if isinstance(entry[0], (int, np.integer)) and 1 <= entry[0] <= len(state_variables):
                    mode_values[entry[0] - 1] = entry[2]
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