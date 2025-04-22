import streamlit as st
import numpy as np
import plotly.express as px
from Main import case15main_droopPlant_sg

# [Keep your existing variable_ranges and default_values dictionaries]

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
    ibr_tab, sg_tab, line_tab, load_tab = st.sidebar.tabs([
        "IBR (Droop Plant)", "SG", "Line Parameters", "Load Parameters"
    ])

    user_params = {}

    # IBR Parameters
    with ibr_tab:
        # Plant Parameters
        st.header("Plant Parameters")
        plant_params = [param for param in variable_ranges.keys()
                       if "Plant" in param and not param.endswith('_SG')]
        for var in plant_params:
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

        # Controller Parameters
        st.header("Controller Parameters")
        ctrl_params = [param for param in variable_ranges.keys()
                      if not "Plant" in param and not param.endswith('_SG')
                      and not param.startswith('Rline') and not param.startswith('Lline')
                      and param not in ['Rload', 'Lload', 'Rx']]
        for var in ctrl_params:
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

    # SG Parameters
    with sg_tab:
        sg_params = [param for param in variable_ranges.keys() if param.endswith('_SG')]
        for var in sg_params:
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

    # Line Parameters
    with line_tab:
        line_params = ['Rline1', 'Lline1', 'Rline2', 'Lline2']
        for var in line_params:
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
    ibr_params = {}
    sg_params = {}
    line1_params = {}
    line2_params = {}
    load_params = {}

    for key, value in user_params.items():
        if key.endswith('_SG'):
            sg_params[key.replace('_SG', '')] = value
        elif key.startswith('Rline1') or key.startswith('Lline1'):
            line1_params[key] = value
        elif key.startswith('Rline2') or key.startswith('Lline2'):
            line2_params[key] = value
        elif key in ['Rload', 'Lload', 'Rx']:
            load_params[key] = value
        else:
            ibr_params[key] = value

    return {
        'parasIBR': ibr_params,
        'parasSG': sg_params,
        'parasLine1': line1_params,
        'parasLine2': line2_params,
        'parasLoad': load_params
    }

def run_simulation(user_params):
    sim_params = prepare_simulation_parameters(user_params)
    return case15main_droopPlant_sg.main_droopPlant_sg(sim_params)

def visualization(testResults):
    state_variables = [
        "thetaPlant(IBR1)", "epsilonPLLPlant(IBR1)", "wPlant(IBR1)", "epsilonP(IBR1)", "epsilonQ(IBR1)",
        "PoPlant(IBR1)", "QoPlant(IBR1)", "PsetDelay(IBR1)", "QsetDelay(IBR1)", "Po(IBR1)", "Qo(IBR1)",
        "phid(IBR1)", "phiq(IBR1)", "gammad(IBR1)", "gammaq(IBR1)", "iid(IBR1)", "iiq(IBR1)", "vcd(IBR1)",
        "vcq(IBR1)", "iod(IBR1)", "ioq(IBR1)",
        "theta(SG1)", "wr(SG1)", "psid(SG1)", "psiq(SG1)", "Eq1(SG1)", "Ed1(SG1)", "psi1d(SG1)",
        "psi2q(SG1)", "P1(SG1)", "Pg(SG1)", "Pf(SG1)", "P2(SG1)", "vx(SG1)", "Efd(SG1)",
        "ilineD(Line1)", "ilineQ(Line1)", "ilineD(Line2)", "ilineQ(Line2)",
        "iloadD(Load)", "iloadQ(Load)"
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
            labels={"x": "Modes", "y": "State Variables", "color": "Participation Factor"},
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