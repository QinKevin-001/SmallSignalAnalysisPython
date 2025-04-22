import streamlit as st
import numpy as np
import plotly.express as px
from Main import case17main_vsmPlant_sg

# Variable ranges for VSM Plant + SG System
variable_ranges = {
    # VSM Plant parameters
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
    "mp": (0.01, 1.0),
    "mq": (0.01, 1.0),
    "Rt": (0.01, 1.0),
    "Lt": (0.01, 1.0),
    "Rd": (0.0, 100.0),
    "Cf": (0.01, 0.20),
    "Rc": (0.01, 1.0),
    "Lc": (0.01, 1.0),
    "J": (1, 20),
    "K": (1, 100),
    "τf": (0.01, 0.1),

    # Load parameters
    "Rload": (0.5, 10.0),
    "Lload": (0.1, 10.0),
    "Rx": (100.0, 1000.0),

    # SG parameters
    "Pset_SG": (0.0, 1.0),
    "Qset_SG": (-1.0, 1.0),
    "ωset_SG": (1.0, 1.0),
    "Vset_SG": (0.9, 1.1),
    "mp_SG": (0.01, 1.0),
    "Rs_SG": (0.0, 0.02),
    "Ld_SG": (0.6, 2.3),
    "Ld1_SG": (0.15, 0.5),
    "Ld2_SG": (0.12, 0.35),
    "Lq_SG": (0.4, 2.3),
    "Lq1_SG": (0.3, 1.0),
    "Lq2_SG": (0.12, 0.45),
    "Ll_SG": (0.1, 0.2),
    "Tdo1_SG": (1.5, 10),
    "Tdo2_SG": (0.01, 0.05),
    "Tqo1_SG": (0.5, 2),
    "Tqo2_SG": (0.01, 0.09),
    "H1_SG": (1, 20),
    "D_SG": (0.0, 1.0),
    "T1_SG": (0.02, 0.10),
    "T2_SG": (0.00, 0.05),
    "T3_SG": (0.20, 0.50),
    "T4_SG": (0.05, 0.50),
    "T5_SG": (0.20, 0.50),
    "K1_SG": (0.4, 0.8),
    "Ke_SG": (100, 500),
    "Ta_SG": (0.5, 2.0),
    "Ta5_SG": (5.0, 20.0),
    "Te_SG": (0.02, 0.10),

    # Line parameters
    "Rline": (0.01, 1.0),
    "Lline": (0.01, 1.0)
}

# Default values for VSM Plant + SG System
default_values = {
    # VSM Plant defaults
    "PsetPlant": 0.1,
    "QsetPlant": 0.0,
    "ωsetPlant": 1.0,
    "VsetPlant": 1.0,
    "KpPLLPlant": 1.0,
    "KiPLLPlant": 50.0,
    "KpPlantP": 1.0,
    "KiPlantP": 10.0,
    "KpPlantQ": 1.0,
    "KiPlantQ": 10.0,
    "ωcPLLPlant": float(2 * np.pi * 100),
    "ωcPlant": float(2 * np.pi * 1),
    "tDelay": 0.5,
    "ωset": 1.0,
    "Vset": 1.0,
    "mp": 0.05,
    "mq": 0.05,
    "Rt": 0.02,
    "Lt": 0.10,
    "Rd": 0.0,
    "Cf": 0.05,
    "Rc": 0.10,
    "Lc": 0.50,
    "J": 10,
    "K": 50,
    "τf": 0.05,

    # Load defaults
    "Rload": 0.9,
    "Lload": 0.4358,
    "Rx": 100,

    # SG defaults
    "Pset_SG": 0.1,
    "Qset_SG": 0.0,
    "ωset_SG": 1.0,
    "Vset_SG": 1.0,
    "mp_SG": 0.05,
    "Rs_SG": 0.0,
    "Ld_SG": 1.0,
    "Ld1_SG": 0.3,
    "Ld2_SG": 0.2,
    "Lq_SG": 1.0,
    "Lq1_SG": 0.5,
    "Lq2_SG": 0.2,
    "Ll_SG": 0.15,
    "Tdo1_SG": 5.0,
    "Tdo2_SG": 0.03,
    "Tqo1_SG": 1.0,
    "Tqo2_SG": 0.05,
    "H1_SG": 5.0,
    "D_SG": 0.5,
    "T1_SG": 0.05,
    "T2_SG": 0.02,
    "T3_SG": 0.35,
    "T4_SG": 0.3,
    "T5_SG": 0.35,
    "K1_SG": 0.5,
    "Ke_SG": 300,
    "Ta_SG": 1.0,
    "Ta5_SG": 10.0,
    "Te_SG": 0.06,

    # Line defaults
    "Rline": 0.1,
    "Lline": 0.1
}

def init_session_state():
    """Initialize session state variables"""
    if "needs_rerun" not in st.session_state:
        st.session_state.needs_rerun = False
    if "selected_mode" not in st.session_state:
        st.session_state.selected_mode = 1

    # Initialize all parameters in session state
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

def update_param(key):
    """Callback for parameter updates"""
    st.session_state.needs_rerun = True

def get_user_inputs():
    """Creates user input controls for parameter tuning"""
    st.sidebar.header("Simulation Parameters")

    # Create tabs for different parameter groups
    vsm_tab, sg_tab, line_tab, load_tab = st.sidebar.tabs([
        "VSM Plant", "SG", "Line", "Load"
    ])

    user_params = {}

    # VSM Plant Parameters
    with vsm_tab:
        st.header("VSM Plant Parameters")

        # Plant control parameters
        st.subheader("Control Parameters")
        control_params = [
            "PsetPlant", "QsetPlant", "ωsetPlant", "VsetPlant",
            "KpPLLPlant", "KiPLLPlant", "KpPlantP", "KiPlantP",
            "KpPlantQ", "KiPlantQ", "ωcPLLPlant", "ωcPlant", "tDelay"
        ]
        for param in control_params:
            min_val, max_val = variable_ranges[param]
            step = (float(max_val) - float(min_val)) / 100.0
            user_params[param] = st.number_input(
                f"{param}",
                min_value=float(min_val),
                max_value=float(max_val),
                value=float(st.session_state[param]),
                step=step,
                key=param,
                on_change=update_param,
                args=(param,)
            )

        # VSM parameters
        st.subheader("VSM Parameters")
        vsm_params = [
            "ωset", "Vset", "mp", "mq", "Rt", "Lt", "Rd",
            "Cf", "Rc", "Lc", "J", "K", "τf"
        ]
        for param in vsm_params:
            min_val, max_val = variable_ranges[param]
            step = (float(max_val) - float(min_val)) / 100.0
            user_params[param] = st.number_input(
                f"{param}",
                min_value=float(min_val),
                max_value=float(max_val),
                value=float(st.session_state[param]),
                step=step,
                key=param,
                on_change=update_param,
                args=(param,)
            )

    # SG Parameters
    with sg_tab:
        st.header("Synchronous Generator Parameters")

        # Machine parameters
        st.subheader("Machine Parameters")
        sg_machine_params = [
            "Pset_SG", "Qset_SG", "ωset_SG", "Vset_SG", "mp_SG",
            "Rs_SG", "Ld_SG", "Ld1_SG", "Ld2_SG", "Lq_SG",
            "Lq1_SG", "Lq2_SG", "Ll_SG", "H1_SG", "D_SG"
        ]
        for param in sg_machine_params:
            min_val, max_val = variable_ranges[param]
            step = (float(max_val) - float(min_val)) / 100.0
            user_params[param] = st.number_input(
                f"{param}",
                min_value=float(min_val),
                max_value=float(max_val),
                value=float(st.session_state[param]),
                step=step,
                key=param,
                on_change=update_param,
                args=(param,)
            )

        # Control parameters
        st.subheader("Control Parameters")
        sg_control_params = [
            "Tdo1_SG", "Tdo2_SG", "Tqo1_SG", "Tqo2_SG",
            "T1_SG", "T2_SG", "T3_SG", "T4_SG", "T5_SG",
            "K1_SG", "Ke_SG", "Ta_SG", "Ta5_SG", "Te_SG"
        ]
        for param in sg_control_params:
            min_val, max_val = variable_ranges[param]
            step = (float(max_val) - float(min_val)) / 100.0
            user_params[param] = st.number_input(
                f"{param}",
                min_value=float(min_val),
                max_value=float(max_val),
                value=float(st.session_state[param]),
                step=step,
                key=param,
                on_change=update_param,
                args=(param,)
            )

    # Line Parameters
    with line_tab:
        st.header("Line Parameters")
        line_params = ["Rline", "Lline"]
        for param in line_params:
            min_val, max_val = variable_ranges[param]
            step = (float(max_val) - float(min_val)) / 100.0
            user_params[param] = st.number_input(
                f"{param}",
                min_value=float(min_val),
                max_value=float(max_val),
                value=float(st.session_state[param]),
                step=step,
                key=param,
                on_change=update_param,
                args=(param,)
            )

    # Load Parameters
    with load_tab:
        st.header("Load Parameters")
        load_params = ["Rload", "Lload", "Rx"]
        for param in load_params:
            min_val, max_val = variable_ranges[param]
            step = (float(max_val) - float(min_val)) / 100.0
            user_params[param] = st.number_input(
                f"{param}",
                min_value=float(min_val),
                max_value=float(max_val),
                value=float(st.session_state[param]),
                step=step,
                key=param,
                on_change=update_param,
                args=(param,)
            )

    return user_params

def prepare_simulation_parameters(user_params):
    """Prepares parameters for simulation"""
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
    """Runs the simulation"""
    sim_params = prepare_simulation_parameters(user_params)
    return case17main_vsmPlant_sg.main_vsmPlant_sg(sim_params)

def visualization(results):
    """Creates visualization of simulation results"""
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

    mode_data = results[1][4]
    if isinstance(mode_data[0], list) and mode_data[0][0] == 'Mode':
        modes = mode_data[1:]
    else:
        modes = mode_data

    mode_range = len(modes)

    # Mode selection with session state
    selected_mode = st.sidebar.slider(
        "Select Mode",
        1, mode_range,
        st.session_state.selected_mode,
        key="mode_slider"
    )
    st.session_state.selected_mode = selected_mode
    mode_index = selected_mode - 1

    # Display eigenvalue
    try:
        eigenvalue = results[1][1][mode_index]
        st.sidebar.write(f"Eigenvalue: {eigenvalue.real:.3f} + {eigenvalue.imag:.3f}j")
    except IndexError:
        st.error("Eigenvalue data unavailable")
        return

    # Create visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Participation factors pie chart
        mode_data = modes[mode_index]
        if len(mode_data) > 5:
            participation_factors = mode_data[5]
            valid_factors = [
                (entry[0], float(entry[2]))
                for entry in participation_factors
                if isinstance(entry[0], (int, np.integer))
                and 1 <= entry[0] <= len(state_variables)
            ]

            if valid_factors:
                magnitudes = [f[1] for f in valid_factors]
                states = [state_variables[f[0]-1] for f in valid_factors]

                fig_pie = px.pie(
                    values=magnitudes,
                    names=states,
                    title=f"Mode {selected_mode} Participation Factors"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.warning("No valid participation factors for this mode")

    with col2:
        # Participation factors heatmap
        heatmap_data = np.zeros((len(state_variables), mode_range))
        for idx, mode in enumerate(modes):
            if len(mode) > 5:
                for entry in mode[5]:
                    if isinstance(entry[0], (int, np.integer)) and 1 <= entry[0] <= len(state_variables):
                        heatmap_data[entry[0]-1, idx] = float(entry[2])

        fig_heatmap = px.imshow(
            heatmap_data,
            labels=dict(x="Mode", y="State Variable", color="Participation Factor"),
            x=[f"Mode {i+1}" for i in range(mode_range)],
            y=state_variables,
            aspect="auto"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

def main():
    st.title("VSM Plant + SG System Analysis")

    # Initialize session state
    init_session_state()

    # Main application flow
    user_params = get_user_inputs()
    results = run_simulation(user_params)
    visualization(results)

    # Handle rerun if needed
    if st.session_state.needs_rerun:
        st.session_state.needs_rerun = False
        st.rerun()

if __name__ == "__main__":
    main()