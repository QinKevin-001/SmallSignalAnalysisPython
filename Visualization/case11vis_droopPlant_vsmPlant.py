import streamlit as st
import numpy as np
import plotly.express as px
from Main import case11main_droopPlant_vsmPlant

# Variable ranges for Droop Plant + VSM Plant System
variable_ranges = {
    # IBR1 Plant-level parameters
    "PsetPlant": (0.0, 1.0), "QsetPlant": (-1.0, 1.0),
    "wsetPlant": (1.0, 1.0), "VsetPlant": (0.9, 1.1),
    "mpPlant": (0.01, 1.00), "mqPlant": (0.01, 1.00),
    "KpPLLPlant": (0.1, 10.0), "KiPLLPlant": (0.1, 1000.0),
    "KpPlantP": (0.1, 10.0), "KiPlantP": (0.1, 100.0),
    "KpPlantQ": (0.1, 10.0), "KiPlantQ": (0.1, 100.0),
    "wcPLLPlant": (float(2 * np.pi * 50), float(2 * np.pi * 1000)),
    "wcPlant": (float(2 * np.pi * 0.1), float(2 * np.pi * 5)),
    "tDelay": (0.1, 1.0),
    # IBR1 System parameters
    "wset": (1.0, 1.0), "Vset": (0.9, 1.1),
    "mp": (0.01, 1.0), "mq": (0.01, 1.0),
    "Rt": (0.01, 1.0), "Lt": (0.01, 1.0),
    "Rd": (0.0, 100.0), "Cf": (0.01, 0.20),
    "Rc": (0.01, 1.0), "Lc": (0.01, 1.0),
    "KpV": (0.1, 10.0), "KiV": (0.1, 1000.0),
    "KpC": (0.1, 10.0), "KiC": (0.1, 1000.0),
    "wc": (float(2 * np.pi * 1), float(2 * np.pi * 20)),
    # IBR2 Plant-level parameters (with _IBR2 suffix)
    "PsetPlant_IBR2": (0.0, 1.0), "QsetPlant_IBR2": (-1.0, 1.0),
    "wsetPlant_IBR2": (1.0, 1.0), "VsetPlant_IBR2": (0.9, 1.1),
    "mpPlant_IBR2": (0.01, 1.00), "mqPlant_IBR2": (0.01, 1.00),
    "KpPLLPlant_IBR2": (0.1, 10.0), "KiPLLPlant_IBR2": (0.1, 1000.0),
    "KpPlantP_IBR2": (0.1, 10.0), "KiPlantP_IBR2": (0.1, 100.0),
    "KpPlantQ_IBR2": (0.1, 10.0), "KiPlantQ_IBR2": (0.1, 100.0),
    "wcPLLPlant_IBR2": (float(2 * np.pi * 50), float(2 * np.pi * 1000)),
    "wcPlant_IBR2": (float(2 * np.pi * 0.1), float(2 * np.pi * 5)),
    "tDelay_IBR2": (0.1, 1.0),
    # IBR2 System parameters
    "wset_IBR2": (1.0, 1.0), "Vset_IBR2": (0.9, 1.1),
    "mp_IBR2": (0.01, 1.0), "mq_IBR2": (0.01, 1.0),
    "Rt_IBR2": (0.01, 1.0), "Lt_IBR2": (0.01, 1.0),
    "Rd_IBR2": (0.0, 100.0), "Cf_IBR2": (0.01, 0.20),
    "Rc_IBR2": (0.01, 1.0), "Lc_IBR2": (0.01, 1.0),
    "J_IBR2": (1, 20), "K_IBR2": (1, 100),
    "tauf_IBR2": (0.01, 0.1),
    # Line1 parameters
    "Rline1": (0.01, 1.0),
    "Lline1": (0.01, 1.0),
    # Line2 parameters
    "Rline2": (0.01, 1.0),
    "Lline2": (0.01, 1.0),
    # Load parameters
    "Rload": (0.5, 10.0),
    "Lload": (0.1, 10.0),
    "Rx": (100.0, 1000.0)
}

# Default values
default_values = {
    # IBR1 Plant-level parameters
    "PsetPlant": 0.1, "QsetPlant": 0.1,
    "wsetPlant": 1.0, "VsetPlant": 1.0,
    "mpPlant": 1.00, "mqPlant": 1.00,
    "KpPLLPlant": 1.8/10, "KiPLLPlant": 160/10,
    "KpPlantP": 0.25, "KiPlantP": 1.00,
    "KpPlantQ": 1.25, "KiPlantQ": 5.00,
    "wcPLLPlant": 2 * np.pi * 100,
    "wcPlant": 2 * np.pi * 1,
    "tDelay": 0.25,
    # IBR1 System parameters
    "wset": 1.0," Vset": 1.0,
    "mp": 0.05, "mq": 0.05,
    "Rt": 0.02, "Lt": 0.10,
    "Rd": 10.00, "Cf": 0.05,
    "Rc": 0.01, "Lc": 0.05,
    "KpV": 4.0, "KiV": 15.0,
    "KpC": 0.4, "KiC": 8.0,
    "wc": 2 * np.pi * 5,
    # IBR2 Plant-level parameters
    "PsetPlant_IBR2": 0.1, "QsetPlant_IBR2": 0.1,
    "wsetPlant_IBR2": 1.0, "VsetPlant_IBR2": 1.0,
    "mpPlant_IBR2": 1.00, "mqPlant_IBR2": 1.00,
    "KpPLLPlant_IBR2": 1.8, "KiPLLPlant_IBR2": 160,
    "KpPlantP_IBR2": 0.12, "KiPlantP_IBR2": 0.50,
    "KpPlantQ_IBR2": 1.25, "KiPlantQ_IBR2": 5.00,
    "wcPLLPlant_IBR2": 2 * np.pi * 100,
    "wcPlant_IBR2": 2 * np.pi * 1,
    "tDelay_IBR2": 0.25,
    # IBR2 System parameters
    "wset_IBR2": 1.0, "Vset_IBR2": 1.0,
    "mp_IBR2": 0.05, "mq_IBR2": 0.05,
    "Rt_IBR2": 0.02, "Lt_IBR2": 0.10, 
    "Rd_IBR2": 10.00, "Cf_IBR2": 0.05,
    "Rc_IBR2": 0.01, "Lc_IBR2": 0.05,
    "J_IBR2": 10.0, "K_IBR2": 12.0,
    "tauf_IBR2": 0.01,
    # Line1 parameters
    "Rline1": 0.02,
    "Lline1": 0.10,
    # Line2 parameters
    "Rline2": 0.02,
    "Lline2": 0.10,
    # Load parameters
    "Rload": 0.90,
    "Lload": 0.4358,
    "Rx": 100
}

# Initialize session state
for key in default_values:
    if key not in st.session_state:
        st.session_state[key] = default_values[key]
if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = 1
if "needs_rerun" not in st.session_state:
    st.session_state.needs_rerun = False

def update_param(key):
    st.session_state.needs_rerun = True

def create_parameter_input(col, var, prefix=""):
    """Creates a number input for a parameter in the given column"""
    min_val, max_val = variable_ranges[var]
    step = float(round((float(max_val) - float(min_val)) / 100, 3))
    display_name = var.replace(prefix, '') if prefix else var
    return col.number_input(
        f"{display_name} ({min_val:.3f} to {max_val:.3f})",
        min_value=float(min_val),
        max_value=float(max_val),
        value=float(st.session_state[var]),
        step=step,
        key=var,
        on_change=update_param,
        args=(var,)
    )

def get_user_inputs():
    """Creates user input controls with parameters stacked two in a row"""
    st.sidebar.header("Simulation Parameters")
    # Create tabs for different parameter groups
    ibr1_tab, ibr2_tab, line_tab, load_tab = st.sidebar.tabs([
        "IBR1 (Droop Plant)",
        "IBR2 (VSM Plant)",
        "Line Parameters",
        "Load Parameters"
    ])
    user_params = {}
    # IBR1 Parameters
    with ibr1_tab:
        st.header("Plant Level Parameters")
        ibr1_plant_params = [param for param in variable_ranges.keys()
                            if not param.endswith('_IBR2') and not param.startswith('Rline')
                            and not param.startswith('Lline') and param not in ['Rload', 'Lload', 'Rx']
                            and 'Plant' in param]
        for i in range(0, len(ibr1_plant_params), 2):
            col1, col2 = st.columns(2)
            user_params[ibr1_plant_params[i]] = create_parameter_input(col1, ibr1_plant_params[i])
            if i + 1 < len(ibr1_plant_params):
                user_params[ibr1_plant_params[i+1]] = create_parameter_input(col2, ibr1_plant_params[i+1])
        st.header("System Level Parameters")
        ibr1_sys_params = [param for param in variable_ranges.keys()
                          if not param.endswith('_IBR2') and not param.startswith('Rline')
                          and not param.startswith('Lline') and param not in ['Rload', 'Lload', 'Rx']
                          and 'Plant' not in param]
        for i in range(0, len(ibr1_sys_params), 2):
            col1, col2 = st.columns(2)
            user_params[ibr1_sys_params[i]] = create_parameter_input(col1, ibr1_sys_params[i])
            if i + 1 < len(ibr1_sys_params):
                user_params[ibr1_sys_params[i+1]] = create_parameter_input(col2, ibr1_sys_params[i+1])
    # IBR2 Parameters
    with ibr2_tab:
        st.header("Plant Level Parameters")
        ibr2_plant_params = [param for param in variable_ranges.keys()
                            if param.endswith('_IBR2') and 'Plant' in param]
        for i in range(0, len(ibr2_plant_params), 2):
            col1, col2 = st.columns(2)
            user_params[ibr2_plant_params[i]] = create_parameter_input(col1, ibr2_plant_params[i], '_IBR2')
            if i + 1 < len(ibr2_plant_params):
                user_params[ibr2_plant_params[i+1]] = create_parameter_input(col2, ibr2_plant_params[i+1], '_IBR2')
        st.header("System Level Parameters")
        ibr2_sys_params = [param for param in variable_ranges.keys()
                          if param.endswith('_IBR2') and 'Plant' not in param]
        for i in range(0, len(ibr2_sys_params), 2):
            col1, col2 = st.columns(2)
            user_params[ibr2_sys_params[i]] = create_parameter_input(col1, ibr2_sys_params[i], '_IBR2')
            if i + 1 < len(ibr2_sys_params):
                user_params[ibr2_sys_params[i+1]] = create_parameter_input(col2, ibr2_sys_params[i+1], '_IBR2')
    # Line Parameters
    with line_tab:
        st.header("Line Parameters")
        line_params = ['Rline1', 'Lline1', 'Rline2', 'Lline2']
        for i in range(0, len(line_params), 2):
            col1, col2 = st.columns(2)
            user_params[line_params[i]] = create_parameter_input(col1, line_params[i])
            if i + 1 < len(line_params):
                user_params[line_params[i+1]] = create_parameter_input(col2, line_params[i+1])
    # Load Parameters
    with load_tab:
        st.header("Load Parameters")
        load_params = ['Rload', 'Lload', 'Rx']
        for i in range(0, len(load_params), 2):
            col1, col2 = st.columns(2)
            user_params[load_params[i]] = create_parameter_input(col1, load_params[i])
            if i + 1 < len(load_params):
                user_params[load_params[i+1]] = create_parameter_input(col2, load_params[i+1])
    return user_params

def prepare_simulation_parameters(user_params):
    """Prepares the parameters in the format expected by the simulation function."""
    ibr1_params = {}
    ibr2_params = {}
    line1_params = {}
    line2_params = {}
    load_params = {}
    for key, value in user_params.items():
        if key.endswith('_IBR2'):
            ibr2_params[key.replace('_IBR2', '')] = value
        elif key.startswith('Rline1') or key.startswith('Lline1'):
            line1_params[key.replace('1', '')] = value
        elif key.startswith('Rline2') or key.startswith('Lline2'):
            line2_params[key.replace('2', '')] = value
        elif key in ['Rload', 'Lload', 'Rx']:
            load_params[key] = value
        else:
            ibr1_params[key] = value
    return {
        'parasIBR1': ibr1_params,
        'parasIBR2': ibr2_params,
        'parasLine1': line1_params,
        'parasLine2': line2_params,
        'parasLoad': load_params
    }

def run_simulation(user_params):
    """Runs the simulation with the given parameters."""
    sim_params = prepare_simulation_parameters(user_params)
    return case11main_droopPlant_vsmPlant.main_droopPlant_vsmPlant(sim_params)

def visualization(testResults):
    """Creates visualizations for the simulation results."""
    state_variables = [
        "thetaPlant(IBR1)", "epsilonPLLPlant(IBR1)", "wPlant(IBR1)", "epsilonP(IBR1)", "epsilonQ(IBR1)",
        "PoPlant(IBR1)", "QoPlant(IBR1)", "PsetDelay(IBR1)", "QsetDelay(IBR1)", "Po(IBR1)", "Qo(IBR1)",
        "phid(IBR1)", "phiq(IBR1)", "gammad(IBR1)", "gammaq(IBR1)", "iid(IBR1)", "iiq(IBR1)", "vcd(IBR1)", "vcq(IBR1)",
        "iod(IBR1)", "ioq(IBR1)",
        "thetaPlant(IBR2)", "epsilonPLLPlant(IBR2)", "wPlant(IBR2)", "epsilonP(IBR2)", "epsilonQ(IBR2)",
        "PoPlant(IBR2)", "QoPlant(IBR2)", "PsetDelay(IBR2)", "QsetDelay(IBR2)", "theta(IBR2)", "Tef(IBR2)", "Qof(IBR2)",
        "Vof(IBR2)", "winv(IBR2)", "psif(IBR2)", "iid(IBR2)", "iiq(IBR2)", "vcd(IBR2)", "vcq(IBR2)", "iod(IBR2)", "ioq(IBR2)",
        'ilineD(Line1)', 'ilineQ(Line1)',
        'ilineD(Line2)', 'ilineQ(Line2)',
        'iloadD(Load)', 'iloadQ(Load)'
    ]
    mode_data_raw = testResults[1][4]
    modes = mode_data_raw[1:] if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode' else mode_data_raw
    mode_range = len(modes)
    selected_mode = st.sidebar.slider(
        "Select Mode",
        1, mode_range,
        st.session_state.selected_mode,
        key="mode_slider"
    )
    st.session_state.selected_mode = selected_mode
    mode_index = selected_mode - 1
    # Display eigenvalue
    eigenvalue = testResults[1][1][mode_index]
    st.sidebar.write(f"Eigenvalue: {eigenvalue.real:.3f} + {eigenvalue.imag:.3f}j")
    # Process participation factors
    mode_data = modes[mode_index]
    participation_factors = mode_data[5]
    valid_factors = [
        (entry[0], float(entry[2]), state_variables[entry[0]-1])
        for entry in participation_factors
        if isinstance(entry[0], (int, np.integer)) and 1 <= entry[0] <= len(state_variables)
    ]
    factor_magnitudes = [factor[1] for factor in valid_factors]
    dominant_state_names = [factor[2] for factor in valid_factors]
    # Create visualizations
    col1, col2 = st.columns([1, 1])

    # Pie chart
    with col1:
        st.subheader(f"Participation Factors for Mode {selected_mode}")
        pie_chart_fig = px.pie(
            names=dominant_state_names,
            values=factor_magnitudes,
            title=f"Participation Factor Distribution for Mode {selected_mode}",
            width=900, height=700
        )
        st.plotly_chart(pie_chart_fig, use_container_width=True)
    # Heatmap
    with col2:
        st.subheader("Participation Factors Heatmap")
        heatmap_data = {}

        for mode_idx in range(mode_range):
            for entry in modes[mode_idx][5]:
                if isinstance(entry[0], (int, np.integer)) and 1 <= entry[0] <= len(state_variables):
                    state_name = state_variables[entry[0]-1]
                    if state_name not in heatmap_data:
                        heatmap_data[state_name] = [0] * mode_range
                    heatmap_data[state_name][mode_idx] = float(entry[2])
        heatmap_array = np.array(list(heatmap_data.values()))
        heatmap_fig = px.imshow(
            heatmap_array,
            x=[f"Mode {i+1}" for i in range(mode_range)],
            y=list(heatmap_data.keys()),
            labels={"color": "Participation Factor"},
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