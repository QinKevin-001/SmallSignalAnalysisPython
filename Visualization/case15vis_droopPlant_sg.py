import streamlit as st
import numpy as np
import plotly.express as px
from Main import case15main_droopPlant_sg

# Variable ranges for Droop Plant + SG System
variable_ranges = {
    # Droop Plant parameters (Case 9)
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
    # Droop controller parameters (Case 9)
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
    "KpV": (0.1, 10.0),
    "KiV": (0.1, 1000.0),
    "KpC": (0.1, 10.0),
    "KiC": (0.1, 1000.0),
    "ωc": (float(2 * np.pi * 1), float(2 * np.pi * 20)),
    # SG parameters (Case 14)
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
    # Load parameters (common)
    "Rload": (0.5, 10.0),
    "Lload": (0.1, 10.0),
    "Rx": (100.0, 1000.0),
    # Line parameters split into Line1 and Line2
    "Rline1": (0.01, 1.0),
    "Lline1": (0.01, 1.0),
    "Rline2": (0.01, 1.0),
    "Lline2": (0.01, 1.0)
}

# Default values for Droop Plant + SG System
default_values = {
    # Droop Plant defaults (Case 9)
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
    # Droop controller defaults (Case 9)
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
    "KpV": 4.0,
    "KiV": 15.0,
    "KpC": 0.4,
    "KiC": 8.0,
    "ωc": float(2 * np.pi * 5),
    # SG defaults (Case 14)
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
    # Load defaults
    "Rload": 0.9,
    "Lload": 0.4358,
    "Rx": 100,
    # Line defaults for Line1 and Line2
    "Rline1": 0.1,
    "Lline1": 0.1,
    "Rline2": 0.1,
    "Lline2": 0.1
}


def get_mode_selection(mode_range):
    st.sidebar.header("Mode Selection")
    selected_mode = st.sidebar.slider("Select Mode", 1, mode_range, 1, key="mode_slider")
    return selected_mode - 1


def get_user_inputs():
    if "user_params" not in st.session_state:
        st.session_state["user_params"] = default_values.copy()
    # Create tabs for different parameter groups
    ibr_tab, sg_tab, line1_tab, line2_tab, load_tab = st.sidebar.tabs([
        "IBR (Droop Plant+Controller)", "SG", "Line1", "Line2", "Load"
    ])
    user_params = {}

    # IBR Parameters: split into Plant-level and Controller parameters
    with ibr_tab:
        st.header("Droop Plant Parameters")
        plant_params = [var for var in variable_ranges.keys()
                        if "Plant" in var and "_SG" not in var]
        for var in plant_params:
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
                key=f"ibr_plant_{var}"
            )
        st.header("Droop Controller Parameters")
        ctrl_params = [var for var in variable_ranges.keys()
                       if ("Plant" not in var) and ("_SG" not in var)
                       and var not in ["Rline1", "Lline1", "Rline2", "Lline2", "Rload", "Lload", "Rx"]]
        for var in ctrl_params:
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
                key=f"ibr_ctrl_{var}"
            )

    # SG Parameters
    with sg_tab:
        st.header("SG Parameters")
        sg_params = [var for var in variable_ranges.keys() if var.endswith("_SG")]
        for var in sg_params:
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
                key=f"sg_{var}"
            )

    # Line1 Parameters
    with line1_tab:
        st.header("Line1 Parameters")
        line1_params = ["Rline1", "Lline1"]
        for var in line1_params:
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

    # Line2 Parameters
    with line2_tab:
        st.header("Line2 Parameters")
        line2_params = ["Rline2", "Lline2"]
        for var in line2_params:
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
        load_params = ["Rload", "Lload", "Rx"]
        for var in load_params:
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

    st.session_state["user_params"] = user_params
    return user_params


def prepare_simulation_parameters(user_params):
    """
    Prepares the parameters in the format expected by the simulation function.
    Splits the inputs into separate groups for Droop IBR, SG, Line1, Line2, and Load.
    """
    parasIBR = {}
    parasSG = {}
    parasLine1 = {}
    parasLine2 = {}
    parasLoad = {}

    for key, value in user_params.items():
        if key.startswith("ibr_plant_") or key.startswith("ibr_ctrl_"):
            new_key = key.split("_", 2)[-1]  # Remove the "ibr_plant_" or "ibr_ctrl_" prefix
            parasIBR[new_key] = value
        elif key.startswith("sg_"):
            new_key = key.replace("sg_", "")
            parasSG[new_key] = value
        elif key.startswith("line1_"):
            new_key = key.replace("line1_", "")
            parasLine1[new_key] = value
        elif key.startswith("line2_"):
            new_key = key.replace("line2_", "")
            parasLine2[new_key] = value
        elif key.startswith("load_"):
            new_key = key.replace("load_", "")
            parasLoad[new_key] = value
        else:
            parasIBR[key] = value  # fallback
    return {
        'parasIBR': parasIBR,
        'parasSG': parasSG,
        'parasLine1': parasLine1,
        'parasLine2': parasLine2,
        'parasLoad': parasLoad
    }


def run_simulation(user_params):
    """Runs the Droop Plant + SG simulation with the current parameters."""
    sim_params = prepare_simulation_parameters(user_params)
    return case15main_droopPlant_sg.main_droopPlant_sg(sim_params)


def visualization(testResults):
    """Generates the eigenvalue and participation factor plots based on simulation output."""
    state_variables = [
        "thetaPlant(IBR1)", "epsilonPLLPlant(IBR1)", "wPlant(IBR1)", "epsilonP(IBR1)", "epsilonQ(IBR1)",
        "PoPlant(IBR1)", "QoPlant(IBR1)", "PsetDelay(IBR1)", "QsetDelay(IBR1)", "Po(IBR1)", "Qo(IBR1)", "phid(IBR1)",
        "phiq(IBR1)", "gammad(IBR1)", "gammaq(IBR1)", "iid(IBR1)", "iiq(IBR1)", "vcd(IBR1)", "vcq(IBR1)", "iod(IBR1)",
        "ioq(IBR1)",
        "theta(SG1)", "wr(SG1)", "psid(SG1)", "psiq(SG1)", "Eq1(SG1)", "Ed1(SG1)", "psi1d(SG1)", "psi2q(SG1)",
        "P1(SG1)", "Pg(SG1)", "Pf(SG1)", "P2(SG1)", "vx(SG1)", "Efd(SG1)",
        "ilineD(Line1)", "ilineQ(Line1)",
        "ilineD(Line2)", "ilineQ(Line2)",
        "iloadD(Load)", "iloadQ(Load)"
    ]
    mode_data_raw = testResults[1][4]
    modes = mode_data_raw[1:] if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode' else mode_data_raw
    mode_range = len(modes)
    mode_index = get_mode_selection(mode_range)
    try:
        eigenvalue_real = float(np.real(testResults[1][1][mode_index]))
        eigenvalue_imag = float(np.imag(testResults[1][1][mode_index]))
        st.sidebar.write(f"Eigenvalue: {eigenvalue_real:.3f} + {eigenvalue_imag:.3f}j")
    except IndexError:
        st.error("Eigenvalue data is unavailable.")
        return

    participation_factors = modes[mode_index][5] if len(modes[mode_index]) > 5 else []
    valid_factors = [(entry[0], float(entry[2])) for entry in participation_factors
                     if isinstance(entry[0], int) and 1 <= entry[0] <= len(state_variables)]
    factor_magnitudes = [entry[1] for entry in valid_factors]
    dominant_state_names = [state_variables[entry[0] - 1] for entry in valid_factors]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Participation Factors for Mode {mode_index + 1}")
        if factor_magnitudes:
            pie_chart_fig = px.pie(
                names=dominant_state_names,
                values=factor_magnitudes,
                width=1000,
                height=800
            )
            st.plotly_chart(pie_chart_fig, use_container_width=True)
    with col2:
        st.subheader("Heatmap of Participation Factors")
        heatmap_data = [np.zeros(len(state_variables)) for _ in range(mode_range)]
        for mode_idx in range(mode_range):
            for entry in modes[mode_idx][5]:
                if isinstance(entry[0], int) and 1 <= entry[0] <= len(state_variables):
                    heatmap_data[mode_idx][entry[0] - 1] = float(entry[2])
        heatmap_fig = px.imshow(
            np.array(heatmap_data).T,
            x=[f"Mode {i + 1}" for i in range(mode_range)],
            y=state_variables,
            width=1000,
            height=800
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)


def run_simulation_and_visualization():
    user_params = get_user_inputs()
    testResults = run_simulation(user_params)
    visualization(testResults)


def main():
    st.title("Droop Plant + SG System Analysis")
    run_simulation_and_visualization()


if __name__ == "__main__":
    main()
