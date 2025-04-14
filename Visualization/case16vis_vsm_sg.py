import streamlit as st
import numpy as np
import plotly.express as px
from Main import case16main_vsm_sg

# Variable ranges for VSM + SG System
variable_ranges = {
    # VSM IBR parameters
    "Pset": (0.0, 1.0),
    "Qset": (-1.0, 1.0),
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

    # SG side line parameters
    "Rline_SG": (0.01, 1.0),
    "Lline_SG": (0.01, 1.0)
}

# Default values for VSM + SG System
default_values = {
    # VSM IBR defaults
    "Pset": 0.1,
    "Qset": 0.0,
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

    # SG side line defaults
    "Rline_SG": 0.1,
    "Lline_SG": 0.1
}


def get_user_inputs():
    """Creates user input controls for parameter tuning via the sidebar."""
    if "user_params" not in st.session_state:
        st.session_state["user_params"] = default_values.copy()

    # Create tabs for different parameter groups
    ibr_tab, sg_tab, line_tab, load_tab = st.sidebar.tabs([
        "IBR (VSM)", "SG", "Line (SG)", "Load"
    ])
    user_params = {}

    # VSM IBR Parameters
    with ibr_tab:
        st.header("VSM IBR Parameters")
        ibr_params = ["Pset", "Qset", "ωset", "Vset", "mp", "mq", "Rt", "Lt", "Rd",
                     "Cf", "Rc", "Lc", "J", "K", "τf"]
        for var in ibr_params:
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
                key=f"ibr_{var}"
            )

    # SG Parameters
    with sg_tab:
        st.header("SG Parameters")
        sg_params = [var for var in variable_ranges.keys()
                     if var.endswith("_SG") and var not in ["Rline_SG", "Lline_SG"]]
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

    # SG Side Line Parameters
    with line_tab:
        st.header("SG Side Line Parameters")
        line_params = ["Rline_SG", "Lline_SG"]
        for var in line_params:
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
                key=f"lineSG_{var}"
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

    return user_params


def visualization(testResults):
    """Generates the eigenvalue and participation factor plots based on simulation output."""
    state_variables = [
        "Tef(IBR1)", "Qof(IBR1)", "Vof(IBR1)", "winv(IBR1)", "psif(IBR1)", "iid(IBR1)", "iiq(IBR1)",
        "vcd(IBR1)", "vcq(IBR1)", "iod(IBR1)", "ioq(IBR1)",
        "theta(SG1)", "wr(SG1)", "psid(SG1)", "psiq(SG1)", "Eq1(SG1)", "Ed1(SG1)", "psi1d(SG1)",
        "psi2q(SG1)", "P1(SG1)", "Pg(SG1)", "Pf(SG1)", "P2(SG1)", "vx(SG1)", "Efd(SG1)",
        "ilineD(LineSG)", "ilineQ(LineSG)",
        "IloadD(Load)", "IloadQ(Load)"
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
        heatmap_data = np.zeros((len(state_variables), mode_range))
        for mode_idx in range(mode_range):
            if len(modes[mode_idx]) > 5:
                for entry in modes[mode_idx][5]:
                    if isinstance(entry[0], int) and 1 <= entry[0] <= len(state_variables):
                        heatmap_data[entry[0] - 1, mode_idx] = float(entry[2])

        heatmap_fig = px.imshow(
            heatmap_data,
            x=[f"Mode {i + 1}" for i in range(mode_range)],
            y=state_variables,
            width=1000,
            height=800,
            aspect='auto'
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)


def prepare_simulation_parameters(user_params):
    """Prepares the parameters in the format expected by the simulation function."""
    parasVSM = {}
    parasSG = {}
    parasLineSG = {}
    parasLoad = {}

    for key, value in user_params.items():
        if key in ["J", "K", "τf"] or (not key.endswith("_SG") and key not in ["Rload", "Lload", "Rx"]):
            parasVSM[key] = value
        elif key.endswith("_SG") and not key.startswith("Rline") and not key.startswith("Lline"):
            new_key = key.replace("_SG", "")
            parasSG[new_key] = value
        elif key.startswith("Rline_SG") or key.startswith("Lline_SG"):
            new_key = key.replace("_SG", "")
            parasLineSG[new_key] = value
        else:
            parasLoad[key] = value

    return {
        'parasVSM': parasVSM,
        'parasSG': parasSG,
        'parasLineSG': parasLineSG,
        'parasLoad': parasLoad
    }


def run_simulation(user_params):
    """Runs the VSM + SG simulation with the current parameters."""
    sim_params = prepare_simulation_parameters(user_params)
    return case16main_vsm_sg.main_vsm_sg(sim_params)


def run_simulation_and_visualization():
    user_params = get_user_inputs()
    testResults = run_simulation(user_params)
    visualization(testResults)


def main():
    st.title("VSM + SG System Analysis")
    run_simulation_and_visualization()


if __name__ == "__main__":
    main()