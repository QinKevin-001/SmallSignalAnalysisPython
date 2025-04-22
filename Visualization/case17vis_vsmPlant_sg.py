import streamlit as st
import numpy as np
import plotly.express as px
from Main import case17main_vsmPlant_sg

# User input Limits
variable_ranges = {
    # VSM Plant parameters
    "PsetPlant": (0.0, 1.0), "QsetPlant": (-1.0, 1.0),
    "ωsetPlant": (1.0, 1.0), "VsetPlant": (0.9, 1.1),
    "KpPLLPlant": (0.1, 10.0), "KiPLLPlant": (0.1, 1000.0),
    "KpPlantP": (0.1, 10.0), "KiPlantP": (0.1, 100.0),
    "KpPlantQ": (0.1, 10.0), "KiPlantQ": (0.1, 100.0),
    "ωcPLLPlant": (float(2 * np.pi * 50), float(2 * np.pi * 1000)),
    "ωcPlant": (float(2 * np.pi * 0.1), float(2 * np.pi * 5)),
    "tDelay": (0.1, 1.0),
    "ωset": (1.0, 1.0), "Vset": (0.9, 1.1),
    "mp": (0.01, 1.0), "mq": (0.01, 1.0),
    "Rt": (0.01, 1.0), "Lt": (0.01, 1.0),
    "Rd": (0.0, 100.0), "Cf": (0.01, 0.20),
    "Rc": (0.01, 1.0), "Lc": (0.01, 1.0),
    "J": (1, 20), "K": (1, 100),
    "τf": (0.01, 0.1),

    # SG parameters
    "Pset_SG": (0.0, 1.0), "Qset_SG": (-1.0, 1.0),
    "ωset_SG": (1.0, 1.0), "Vset_SG": (0.9, 1.1),
    "mp_SG": (0.01, 1.0), "Rs_SG": (0.0, 0.02),
    "Ld_SG": (0.6, 2.3), "Ld1_SG": (0.15, 0.5),
    "Ld2_SG": (0.12, 0.35), "Lq_SG": (0.4, 2.3),
    "Lq1_SG": (0.3, 1.0), "Lq2_SG": (0.12, 0.45),
    "Ll_SG": (0.1, 0.2), "Tdo1_SG": (1.5, 10),
    "Tdo2_SG": (0.01, 0.05), "Tqo1_SG": (0.5, 2),
    "Tqo2_SG": (0.01, 0.09), "H1_SG": (1, 20),
    "D_SG": (0.0, 1.0), "T1_SG": (0.02, 0.10),
    "T2_SG": (0.00, 0.05), "T3_SG": (0.20, 0.50),
    "T4_SG": (0.05, 0.50), "T5_SG": (0.20, 0.50),
    "K1_SG": (0.4, 0.8), "Ke_SG": (100, 500),
    "Ta_SG": (0.5, 2.0), "Ta5_SG": (5.0, 20.0),
    "Te_SG": (0.02, 0.10),

    # Line and Load parameters
    "Rline": (0.01, 1.0), "Lline": (0.01, 1.0),
    "Rload": (0.5, 10.0), "Lload": (0.1, 10.0),
    "Rx": (100.0, 1000.0)
}

# Default values
default_values = {
    # VSM Plant defaults
    "PsetPlant": 0.1, "QsetPlant": 0.0,
    "ωsetPlant": 1.0, "VsetPlant": 1.0,
    "KpPLLPlant": 1.0, "KiPLLPlant": 50.0,
    "KpPlantP": 1.0, "KiPlantP": 10.0,
    "KpPlantQ": 1.0, "KiPlantQ": 10.0,
    "ωcPLLPlant": float(2 * np.pi * 100),
    "ωcPlant": float(2 * np.pi * 1),
    "tDelay": 0.5,
    "ωset": 1.0, "Vset": 1.0,
    "mp": 0.05, "mq": 0.05,
    "Rt": 0.02, "Lt": 0.10,
    "Rd": 0.0, "Cf": 0.05,
    "Rc": 0.10, "Lc": 0.50,
    "J": 10, "K": 50,
    "τf": 0.05,

    # SG defaults
    "Pset_SG": 0.1, "Qset_SG": 0.0,
    "ωset_SG": 1.0, "Vset_SG": 1.0,
    "mp_SG": 0.05, "Rs_SG": 0.0,
    "Ld_SG": 1.0, "Ld1_SG": 0.3,
    "Ld2_SG": 0.2, "Lq_SG": 1.0,
    "Lq1_SG": 0.5, "Lq2_SG": 0.2,
    "Ll_SG": 0.15, "Tdo1_SG": 5.0,
    "Tdo2_SG": 0.03, "Tqo1_SG": 1.0,
    "Tqo2_SG": 0.05, "H1_SG": 5.0,
    "D_SG": 0.5, "T1_SG": 0.05,
    "T2_SG": 0.02, "T3_SG": 0.35,
    "T4_SG": 0.3, "T5_SG": 0.35,
    "K1_SG": 0.5, "Ke_SG": 300,
    "Ta_SG": 1.0, "Ta5_SG": 10.0,
    "Te_SG": 0.06,

    # Line and Load defaults
    "Rline": 0.1, "Lline": 0.1,
    "Rload": 0.9, "Lload": 0.4358,
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
    vsm_plant_tab, sg_tab, line_load_tab = st.sidebar.tabs(["VSM Plant", "SG", "Line & Load"])

    user_params = {}

    # VSM Plant Parameters
    with vsm_plant_tab:
        vsm_params = [param for param in variable_ranges.keys() if
                     not param.endswith('_SG') and param not in ['Rline', 'Lline', 'Rload', 'Lload', 'Rx']]
        for var in vsm_params:
            step = float(round((variable_ranges[var][1] - variable_ranges[var][0]) / 100, 3))
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
            step = float(round((variable_ranges[var][1] - variable_ranges[var][0]) / 100, 3))
            user_params[var] = st.number_input(
                f"{var.replace('_SG', '')} ({variable_ranges[var][0]} to {variable_ranges[var][1]})",
                min_value=float(variable_ranges[var][0]),
                max_value=float(variable_ranges[var][1]),
                value=float(st.session_state[var]),
                step=step,
                key=var,
                on_change=update_param,
                args=(var,)
            )

    # Line & Load Parameters
    with line_load_tab:
        line_load_params = ['Rline', 'Lline', 'Rload', 'Lload', 'Rx']
        for var in line_load_params:
            step = float(round((variable_ranges[var][1] - variable_ranges[var][0]) / 100, 3))
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
    vsm_plant_params = {}
    sg_params = {}
    line_params = {}
    load_params = {}

    for key, value in user_params.items():
        if key.endswith('_SG'):
            sg_params[key.replace('_SG', '')] = value
        elif key in ['Rline', 'Lline']:
            line_params[key] = value
        elif key in ['Rload', 'Lload', 'Rx']:
            load_params[key] = value
        else:
            vsm_plant_params[key] = value

    return {
        'parasVSMPlant': vsm_plant_params,
        'parasSG': sg_params,
        'parasLine': line_params,
        'parasLoad': load_params
    }

def run_simulation(user_params):
    sim_params = prepare_simulation_parameters(user_params)
    return case17main_vsmPlant_sg.main_vsmPlant_sg(sim_params)

def visualization(testResults):
    state_variables = [
        "thetaPlant(IBR1)", "epsilonPLLPlant(IBR1)", "wPlant(IBR1)", "epsilonP(IBR1)",
        "epsilonQ(IBR1)", "PoPlant(IBR1)", "QoPlant(IBR1)", "PsetDelay(IBR1)",
        "QsetDelay(IBR1)", "Tef(IBR1)", "Qof(IBR1)", "Vof(IBR1)", "winv(IBR1)",
        "psif(IBR1)", "iid(IBR1)", "iiq(IBR1)", "vcd(IBR1)", "vcq(IBR1)", "iod(IBR1)",
        "ioq(IBR1)", "theta(SG1)", "wr(SG1)", "psid(SG1)", "psiq(SG1)", "Eq1(SG1)",
        "Ed1(SG1)", "psi1d(SG1)", "psi2q(SG1)", "P1(SG1)", "Pg(SG1)", "Pf(SG1)",
        "P2(SG1)", "vx(SG1)", "Efd(SG1)", "ilineD(Line1)", "ilineQ(Line1)",
        "ilineD(Line2)", "ilineQ(Line2)", "IloadD(Load)", "IloadQ(Load)"
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

    # Display eigenvalue
    try:
        eigenvalue = testResults[1][1][mode_index]
        st.sidebar.write(f"Eigenvalue: {eigenvalue.real:.3f} + {eigenvalue.imag:.3f}j")
    except IndexError:
        st.error("Eigenvalue data unavailable")
        return

    # Layout for Pie Chart and Heatmap
    col1, col2 = st.columns([1, 1])

    with col1:
        # Participation factors pie chart
        mode_data = modes[mode_index]
        if len(mode_data) > 5:
            participation_factors = mode_data[5]
            valid_factors = [
                entry for entry in participation_factors
                if isinstance(entry[0], (int, np.integer)) and 1 <= entry[0] <= len(state_variables)
            ]
            state_locations = [entry[0] for entry in valid_factors]
            factor_magnitudes = [entry[2] for entry in valid_factors]
            dominant_state_names = [state_variables[loc - 1] for loc in state_locations]

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
        # Participation factors heatmap
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