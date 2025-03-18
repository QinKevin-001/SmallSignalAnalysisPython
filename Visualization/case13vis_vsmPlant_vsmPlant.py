import streamlit as st
import numpy as np
import plotly.express as px
from Main import case13main_vsmPlant_vsmPlant

# Parameter ranges
variable_ranges = {
    # Plant parameters (for both VSM Plants)
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
    # System parameters
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
    # IBR #1 VSM Plant parameters
    "J1": (1, 20),
    "K1": (1, 100),
    "τf1": (0.01, 0.1),
    # IBR #2 VSM Plant parameters
    "J2": (1, 20),
    "K2": (1, 100),
    "τf2": (0.01, 0.1),
    # Load parameters
    "Rload": (0.5, 10.0),
    "Lload": (0.1, 10.0),
    "Rx": (100.0, 1000.0),
    # Line parameters (for both Line #1 and Line #2)
    "Rline": (0.01, 1.0),
    "Lline": (0.01, 1.0)
}

# Default values
default_values = {
    # Plant defaults
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
    # System defaults
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
    # IBR #1 VSM Plant defaults
    "J1": 10,
    "K1": 50,
    "τf1": 0.05,
    # IBR #2 VSM Plant defaults
    "J2": 10,
    "K2": 50,
    "τf2": 0.05,
    # Load defaults
    "Rload": 0.9,
    "Lload": 0.4358,
    "Rx": 100,
    # Line defaults
    "Rline": 0.1,
    "Lline": 0.1
}

# Sidebar: User input
def get_user_inputs():
    if "user_params" not in st.session_state:
        st.session_state["user_params"] = default_values.copy()
    user_params = {}
    st.sidebar.header("Parameters")
    for var, (min_val, max_val) in variable_ranges.items():
        user_params[var] = st.sidebar.number_input(
            f"{var} ({min_val} to {max_val})",
            min_value=float(min_val),
            max_value=float(max_val),
            value=float(st.session_state["user_params"].get(var, default_values[var])),
            step=round((max_val - min_val) / 100, 3),
            key=f"param_{var}"
        )
    st.session_state["user_params"] = user_params
    return user_params

# Sidebar: Mode selection
def get_mode_selection(mode_range):
    st.sidebar.header("Mode Selection")
    selected_mode = st.sidebar.slider("Select Mode", 1, mode_range, 1, key="mode_slider")
    return selected_mode - 1

# Run simulation
def run_simulation(user_params):
    return case13main_vsmPlant_vsmPlant.main_vsmPlant_vsmPlant(user_params)

# Visualization
def visualization(testResults):
    state_variables = [
        "epsilonPLLPlant(IBR1)", "wPlant(IBR1)", "epsilonP(IBR1)", "epsilonQ(IBR1)", "PoPlant(IBR1)", "QoPlant(IBR1)",
        "PsetDelay(IBR1)", "QsetDelay(IBR1)", "theta(IBR1)", "Tef(IBR1)" "Qof(IBR1)", "Vof(IBR1)", "winv(IBR1)",
        "psif(IBR1)", "iid(IBR1)", "iiq(IBR1)", "vcd(IBR1)", "vcq(IBR1)", "iod(IBR1)", "ioq(IBR1)",
        "thetaPlant(IBR2)", "epsilonPLLPlant(IBR2)", "wPlant(IBR2)", "epsilonP(IBR2)", "epsilonQ(IBR2)", "PoPlant(IBR2)",
        "QoPlant(IBR2)", "PsetDelay(IBR2)", "QsetDelay(IBR2)", "theta(IBR2)", "Tef(IBR2)" "Qof(IBR2)", "Vof(IBR2)",
        "winv(IBR2)", "psif(IBR2)", "iid(IBR2)", "iiq(IBR2)", "vcd(IBR2)", "vcq(IBR2)", "iod(IBR2)", "ioq(IBR2)",
        "ilineD(Line1)", "ilineQ(Line1)",
        "ilineD(Line2)", "ilineQ(Line2)",
        "IloadD(Load)", "IloadQ(Load)"
    ]
    mode_data_raw = testResults[1][4]
    modes = mode_data_raw[1:] if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode' else mode_data_raw
    mode_range = len(modes)
    mode_index = get_mode_selection(mode_range)
    try:
        eigenvalue_real = float(np.real(testResults[1][1][mode_index]))
        eigenvalue_imag = float(np.imag(testResults[1][1][mode_index]))
    except IndexError:
        st.error("Eigenvalue data unavailable.")
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
    st.title("VSM Plant + VSM Plant System Analysis")
    run_simulation_and_visualization()

if __name__ == "__main__":
    main()
