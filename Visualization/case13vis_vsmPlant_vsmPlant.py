import streamlit as st
import numpy as np
import plotly.express as px
from Main import case13main_vsmPlant_vsmPlant

# Variable ranges for VSM Plant + VSM Plant System
variable_ranges = {
    # IBR1 Plant-level parameters
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
    # IBR1 System parameters
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
    # IBR1 VSM Parameters
    "J1": (1, 20),
    "K1": (1, 100),
    "τf1": (0.01, 0.1),
    # IBR2 Plant-level parameters (using _IBR2 suffix)
    "PsetPlant_IBR2": (0.0, 1.0),
    "QsetPlant_IBR2": (-1.0, 1.0),
    "ωsetPlant_IBR2": (1.0, 1.0),
    "VsetPlant_IBR2": (0.9, 1.1),
    "KpPLLPlant_IBR2": (0.1, 10.0),
    "KiPLLPlant_IBR2": (0.1, 1000.0),
    "KpPlantP_IBR2": (0.1, 10.0),
    "KiPlantP_IBR2": (0.1, 100.0),
    "KpPlantQ_IBR2": (0.1, 10.0),
    "KiPlantQ_IBR2": (0.1, 100.0),
    "ωcPLLPlant_IBR2": (float(2 * np.pi * 50), float(2 * np.pi * 1000)),
    "ωcPlant_IBR2": (float(2 * np.pi * 0.1), float(2 * np.pi * 5)),
    "tDelay_IBR2": (0.1, 1.0),
    # IBR2 System parameters
    "ωset_IBR2": (1.0, 1.0),
    "Vset_IBR2": (0.9, 1.1),
    "mp_IBR2": (0.01, 1.0),
    "mq_IBR2": (0.01, 1.0),
    "Rt_IBR2": (0.01, 1.0),
    "Lt_IBR2": (0.01, 1.0),
    "Rd_IBR2": (0.0, 100.0),
    "Cf_IBR2": (0.01, 0.20),
    "Rc_IBR2": (0.01, 1.0),
    "Lc_IBR2": (0.01, 1.0),
    # IBR2 VSM Parameters (renamed from J2, K2, τf2)
    "J_IBR2": (1, 20),
    "K_IBR2": (1, 100),
    "τf_IBR2": (0.01, 0.1),
    # Line parameters (for Line1 and Line2)
    "Rline1": (0.01, 1.0),
    "Lline1": (0.01, 1.0),
    "Rline2": (0.01, 1.0),
    "Lline2": (0.01, 1.0),
    # Load parameters
    "Rload": (0.5, 10.0),
    "Lload": (0.1, 10.0),
    "Rx": (100.0, 1000.0)
}

# Default values
default_values = {
    # IBR1 Plant-level defaults
    "PsetPlant": 0.1,
    "QsetPlant": 0.1,
    "ωsetPlant": 1.0,
    "VsetPlant": 1.0,
    "KpPLLPlant": 1.0,
    "KiPLLPlant": 50.0,
    "KpPlantP": 1.0,
    "KiPlantP": 10.0,
    "KpPlantQ": 1.0,
    "KiPlantQ": 10.0,
    "ωcPLLPlant": 2 * np.pi * 100,
    "ωcPlant": 2 * np.pi * 1,
    "tDelay": 0.5,
    # IBR1 System defaults
    "ωset": 1.0,
    "Vset": 1.0,
    "mp": 0.05,
    "mq": 0.05,
    "Rt": 0.02,
    "Lt": 0.10,
    "Rd": 10.00,
    "Cf": 0.05,
    "Rc": 0.01,
    "Lc": 0.05,
    # IBR1 VSM defaults
    "J1": 10,
    "K1": 50,
    "τf1": 0.05,
    # IBR2 Plant-level defaults
    "PsetPlant_IBR2": 0.1,
    "QsetPlant_IBR2": 0.1,
    "ωsetPlant_IBR2": 1.0,
    "VsetPlant_IBR2": 1.0,
    "KpPLLPlant_IBR2": 1.0,
    "KiPLLPlant_IBR2": 50.0,
    "KpPlantP_IBR2": 1.0,
    "KiPlantP_IBR2": 10.0,
    "KpPlantQ_IBR2": 1.0,
    "KiPlantQ_IBR2": 10.0,
    "ωcPLLPlant_IBR2": 2 * np.pi * 100,
    "ωcPlant_IBR2": 2 * np.pi * 1,
    "tDelay_IBR2": 0.5,
    # IBR2 System defaults
    "ωset_IBR2": 1.0,
    "Vset_IBR2": 1.0,
    "mp_IBR2": 0.05,
    "mq_IBR2": 0.05,
    "Rt_IBR2": 0.02,
    "Lt_IBR2": 0.10,
    "Rd_IBR2": 10.00,
    "Cf_IBR2": 0.05,
    "Rc_IBR2": 0.01,
    "Lc_IBR2": 0.05,
    # IBR2 VSM defaults
    "J_IBR2": 10,
    "K_IBR2": 12,
    "τf_IBR2": 0.01,
    # Line defaults
    "Rline1": 0.02,
    "Lline1": 0.10,
    "Rline2": 0.02,
    "Lline2": 0.10,
    # Load defaults
    "Rload": 0.90,
    "Lload": 0.4358,
    "Rx": 100
}


def get_user_inputs():
    """Creates user input controls for parameter tuning via the sidebar."""
    st.sidebar.header("Simulation Parameters")

    # Create tabs for different parameter groups
    ibr1_tab, ibr2_tab, line_tab, load_tab = st.sidebar.tabs([
        "IBR1 (VSM Plant)", "IBR2 (VSM Plant)", "Line Parameters", "Load Parameters"
    ])

    user_params = {}

    # IBR1 Parameters
    with ibr1_tab:
        st.header("IBR1 Plant-Level Parameters")
        ibr1_plant_params = [param for param in variable_ranges.keys()
                             if not param.endswith('_IBR2') and not param.startswith('Rline')
                             and not param.startswith('Lline') and param not in ['Rload', 'Lload', 'Rx']
                             and 'Plant' in param]
        for var in ibr1_plant_params:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            min_val, max_val, default = float(min_val), float(max_val), float(default)
            step = float((max_val - min_val) / 100.0)
            user_params[var] = st.number_input(
                f"{var} ({min_val:.3f} to {max_val:.3f})",
                min_value=min_val,
                max_value=max_val,
                value=default,
                step=step,
                format="%.3f",
                key=f"ibr1_plant_{var}"
            )

        st.header("IBR1 System Parameters")
        ibr1_sys_params = [param for param in variable_ranges.keys()
                           if not param.endswith('_IBR2') and not param.startswith('Rline')
                           and not param.startswith('Lline') and param not in ['Rload', 'Lload', 'Rx']
                           and 'Plant' not in param and param not in ["J1", "K1", "τf1"]]
        for var in ibr1_sys_params:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            min_val, max_val, default = float(min_val), float(max_val), float(default)
            step = float((max_val - min_val) / 100.0)
            user_params[var] = st.number_input(
                f"{var} ({min_val:.3f} to {max_val:.3f})",
                min_value=min_val,
                max_value=max_val,
                value=default,
                step=step,
                format="%.3f",
                key=f"ibr1_sys_{var}"
            )

        st.header("IBR1 VSM Parameters")
        for var in ["J1", "K1", "τf1"]:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            min_val, max_val, default = float(min_val), float(max_val), float(default)
            step = float((max_val - min_val) / 100.0)
            user_params[var] = st.number_input(
                f"{var} ({min_val:.3f} to {max_val:.3f})",
                min_value=min_val,
                max_value=max_val,
                value=default,
                step=step,
                format="%.3f",
                key=f"ibr1_vsm_{var}"
            )

    # IBR2 Parameters
    with ibr2_tab:
        st.header("IBR2 Plant-Level Parameters")
        ibr2_plant_params = [param for param in variable_ranges.keys()
                             if param.endswith('_IBR2') and 'Plant' in param]
        for var in ibr2_plant_params:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            min_val, max_val, default = float(min_val), float(max_val), float(default)
            step = float((max_val - min_val) / 100.0)
            user_params[var] = st.number_input(
                f"{var.replace('_IBR2', '')} ({min_val:.3f} to {max_val:.3f})",
                min_value=min_val,
                max_value=max_val,
                value=default,
                step=step,
                format="%.3f",
                key=f"ibr2_plant_{var}"
            )

        st.header("IBR2 System Parameters")
        ibr2_sys_params = [param for param in variable_ranges.keys()
                           if param.endswith('_IBR2') and 'Plant' not in param and param not in ["J_IBR2", "K_IBR2",
                                                                                                 "τf_IBR2"]]
        for var in ibr2_sys_params:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            min_val, max_val, default = float(min_val), float(max_val), float(default)
            step = float((max_val - min_val) / 100.0)
            user_params[var] = st.number_input(
                f"{var.replace('_IBR2', '')} ({min_val:.3f} to {max_val:.3f})",
                min_value=min_val,
                max_value=max_val,
                value=default,
                step=step,
                format="%.3f",
                key=f"ibr2_sys_{var}"
            )

        st.header("IBR2 VSM Parameters")
        for var in ["J_IBR2", "K_IBR2", "τf_IBR2"]:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            min_val, max_val, default = float(min_val), float(max_val), float(default)
            step = float((max_val - min_val) / 100.0)
            user_params[var] = st.number_input(
                f"{var.replace('_IBR2', '')} ({min_val:.3f} to {max_val:.3f})",
                min_value=min_val,
                max_value=max_val,
                value=default,
                step=step,
                format="%.3f",
                key=f"ibr2_vsm_{var}"
            )

    # Line Parameters
    with line_tab:
        st.header("Line1 Parameters")
        for var in ['Rline1', 'Lline1']:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            min_val, max_val, default = float(min_val), float(max_val), float(default)
            step = float((max_val - min_val) / 100.0)
            user_params[var] = st.number_input(
                f"{var} ({min_val:.3f} to {max_val:.3f})",
                min_value=min_val,
                max_value=max_val,
                value=default,
                step=step,
                format="%.3f",
                key=f"line1_{var}"
            )

        st.header("Line2 Parameters")
        for var in ['Rline2', 'Lline2']:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            min_val, max_val, default = float(min_val), float(max_val), float(default)
            step = float((max_val - min_val) / 100.0)
            user_params[var] = st.number_input(
                f"{var} ({min_val:.3f} to {max_val:.3f})",
                min_value=min_val,
                max_value=max_val,
                value=default,
                step=step,
                format="%.3f",
                key=f"line2_{var}"
            )

    # Load Parameters
    with load_tab:
        st.header("Load Parameters")
        for var in ['Rload', 'Lload', 'Rx']:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            min_val, max_val, default = float(min_val), float(max_val), float(default)
            step = float((max_val - min_val) / 100.0)
            user_params[var] = st.number_input(
                f"{var} ({min_val:.3f} to {max_val:.3f})",
                min_value=min_val,
                max_value=max_val,
                value=default,
                step=step,
                format="%.3f",
                key=f"load_{var}"
            )

    return user_params


def prepare_simulation_parameters(user_params):
    """Prepares the parameters in the format expected by the simulation function."""
    ibr1_params = {}
    ibr2_params = {}
    line1_params = {}
    line2_params = {}
    load_params = {}

    for key, value in user_params.items():
        if key.endswith('_IBR2') or '_ibr2_' in key:
            # Remove the '_IBR2' or 'ibr2_' substring for simulation input
            new_key = key.replace('_IBR2', '').replace('ibr2_', '')
            ibr2_params[new_key] = value
        elif key.startswith('line1_'):
            new_key = key.replace('line1_', '')
            line1_params[new_key] = value
        elif key.startswith('line2_'):
            new_key = key.replace('line2_', '')
            line2_params[new_key] = value
        elif key.startswith('load_'):
            new_key = key.replace('load_', '')
            load_params[new_key] = value
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
    """Runs the VSM Plant + VSM Plant simulation with the current parameters."""
    sim_params = prepare_simulation_parameters(user_params)
    return case13main_vsmPlant_vsmPlant.main_vsmPlant_vsmPlant(sim_params)


def visualization(testResults):
    """Generates the eigenvalue and participation factor plots based on simulation output."""
    state_variables = [
        "epsilonPLLPlant(IBR1)", "wPlant(IBR1)", "epsilonP(IBR1)", "epsilonQ(IBR1)", "PoPlant(IBR1)", "QoPlant(IBR1)",
        "PsetDelay(IBR1)", "QsetDelay(IBR1)", "theta(IBR1)", "Po(IBR1)", "Qo(IBR1)", "phid(IBR1)", "phiq(IBR1)",
        "gammad(IBR1)", "gammaq(IBR1)", "iid(IBR1)", "iiq(IBR1)", "vcd(IBR1)", "vcq(IBR1)", "iod(IBR1)", "ioq(IBR1)",
        "epsilonPLLPlant(IBR2)", "wPlant(IBR2)", "epsilonP(IBR2)", "epsilonQ(IBR2)", "PoPlant(IBR2)",
        "QoPlant(IBR2)", "PsetDelay(IBR2)", "QsetDelay(IBR2)", "theta(IBR2)", "Po(IBR2)", "Qo(IBR2)", "phid(IBR2)",
        "phiq(IBR2)", "gammad(IBR2)", "gammaq(IBR2)", "iid(IBR2)", "iiq(IBR2)", "vcd(IBR2)", "vcq(IBR2)", "iod(IBR2)",
        "ioq(IBR2)", "ilineD(Line1)", "ilineQ(Line1)", "ilineD(Line2)", "ilineQ(Line2)", "iloadD(Load)", "iloadQ(Load)"
    ]

    mode_data_raw = testResults[1][4]
    modes = mode_data_raw[1:] if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode' else mode_data_raw
    mode_range = len(modes)

    selected_mode = st.sidebar.slider("Select a Mode", 1, mode_range, 1, key="mode_selector")
    mode_index = selected_mode - 1

    try:
        eigenvalue_real = float(np.real(testResults[1][1][mode_index]))
        eigenvalue_imag = float(np.imag(testResults[1][1][mode_index]))
        st.sidebar.write(f"Eigenvalue: {eigenvalue_real:.3f} + {eigenvalue_imag:.3f}j")
    except IndexError:
        st.error("Eigenvalue data is unavailable.")
        return

    try:
        participation_factors = modes[mode_index][5] if len(modes[mode_index]) > 5 else []
        if participation_factors:
            valid_factors = [
                (entry[0], float(entry[2]), state_variables[entry[0] - 1])
                for entry in participation_factors
                if isinstance(entry[0], int) and 1 <= entry[0] <= len(state_variables)
            ]
            factor_magnitudes = [factor[1] for factor in valid_factors]
            dominant_state_names = [factor[2] for factor in valid_factors]
        else:
            factor_magnitudes = []
            dominant_state_names = []
    except (IndexError, ValueError, TypeError):
        st.error("Error parsing participation factors.")
        return

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
        heatmap_data = {}
        for mode_idx in range(mode_range):
            for entry in modes[mode_idx][5]:
                if isinstance(entry[0], int) and 1 <= entry[0] <= len(state_variables):
                    state_name = state_variables[entry[0] - 1]
                    if state_name not in heatmap_data:
                        heatmap_data[state_name] = [0] * mode_range
                    heatmap_data[state_name][mode_idx] = float(entry[2])
        heatmap_array = np.array(list(heatmap_data.values()))
        heatmap_fig = px.imshow(
            heatmap_array,
            x=[f"Mode {i + 1}" for i in range(mode_range)],
            y=list(heatmap_data.keys()),
            labels={"color": "Participation Factor"},
            color_continuous_scale="Blues",
            title="Participation Factors Heatmap",
            width=900, height=700
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)


def main():
    """Main function to handle user inputs, simulation, and visualization."""
    st.title("VSM Plant + VSM Plant System Analysis")
    user_params = get_user_inputs()
    testResults = run_simulation(user_params)
    visualization(testResults)


if __name__ == "__main__":
    main()
