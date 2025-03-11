import streamlit as st
import numpy as np
import plotly.express as px
from Main import case12main_vsm_vsm

# Parameter ranges
variable_ranges = {
    # System parameters
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
    # IBR #1 VSM parameters
    "J1": (1, 20),
    "K1": (1, 100),
    "τf1": (0.01, 0.1),
    # IBR #2 VSM parameters
    "J2": (1, 20),
    "K2": (1, 100),
    "τf2": (0.01, 0.1),
    # Load parameters
    "Rload": (0.5, 10.0),
    "Lload": (0.1, 10.0),
    "Rx": (100.0, 1000.0)
}

# Default values
default_values = {
    # System defaults
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
    # IBR #1 VSM defaults
    "J1": 10,
    "K1": 50,
    "τf1": 0.05,
    # IBR #2 VSM defaults
    "J2": 10,
    "K2": 50,
    "τf2": 0.05,
    # Load defaults
    "Rload": 0.9,
    "Lload": 0.4358,
    "Rx": 100
}

# User input sidebar
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

# Mode selection sidebar
def get_mode_selection(mode_range):
    st.sidebar.header("Mode Selection")
    selected_mode = st.sidebar.slider("Select Mode", 1, mode_range, 1, key="mode_slider")
    return selected_mode - 1

# Run simulation
def run_simulation(user_params):
    return case12main_vsm_vsm.main_vsm_vsm(user_params)

# Visualization
def visualization(testResults):
    state_variables = [
        "Theta1", "Po1", "Qo1", "Phid1", "Phiq1", "Gammad1", "Gammaq1",
        "Iid1", "Iiq1", "Vcd1", "Vcq1", "Iod1", "Ioq1", "IloadD1", "IloadQ1",
        "Theta2", "Po2", "Qo2", "Phid2", "Phiq2", "Gammad2", "Gammaq2",
        "Iid2", "Iiq2", "Vcd2", "Vcq2", "Iod2", "Ioq2", "IloadD2", "IloadQ2",
        "IloadD", "IloadQ"
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
    dominant_state_names = [state_variables[entry[0]-1] for entry in valid_factors]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Participation Factors for Mode {mode_index+1}")
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
                    heatmap_data[mode_idx][entry[0]-1] = float(entry[2])
        heatmap_fig = px.imshow(
            np.array(heatmap_data).T,
            x=[f"Mode {i+1}" for i in range(mode_range)],
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
    st.title("VSM + VSM System Analysis")
    run_simulation_and_visualization()

if __name__ == "__main__":
    main()
