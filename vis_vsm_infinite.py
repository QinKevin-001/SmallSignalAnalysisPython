# Test confirmed

import streamlit as st
import numpy as np
import plotly.express as px
import main_vsm_infinite  # Import simulation script

# ----------------- 📌 Define Parameter Limits ----------------- #
variable_ranges = {
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
    "J": (1.0, 20.0),
    "K": (1.0, 100.0),
    "τf": (0.01, 0.1)
}

# Default values from `main_vsm_infinite.py`
default_values = {
    "Pset": 0.1, "Qset": 0.0,
    "ωset": 1.0, "Vset": 1.0,
    "mp": 0.05, "mq": 0.05,
    "Rt": 0.02, "Lt": 0.10,
    "Rd": 0.00, "Cf": 0.05,
    "Rc": 0.10, "Lc": 0.50,
    "J": 10.0, "K": 12.0,
    "τf": 0.01
}

# ----------------- 📌 Sidebar: Simulation Parameters ----------------- #
def get_user_inputs():
    """Creates user input controls inside the Simulation Parameters tab, ensuring unique widget keys."""

    # Ensure session state is initialized
    if "user_params" not in st.session_state:
        st.session_state["user_params"] = {key: default_values[key] for key in variable_ranges}

    user_params = {}

    # Create a Simulation Parameters Sidebar
    st.sidebar.header("Simulation Parameters")
    for var, (min_val, max_val) in variable_ranges.items():
        user_params[var] = st.sidebar.number_input(
            f"{var} ({min_val} to {max_val})",
            min_value=float(min_val),
            max_value=float(max_val),
            value=float(st.session_state["user_params"].get(var, default_values[var])),
            step=round((float(max_val) - float(min_val)) / 100, 3),
            key=f"param_{var}"  # Unique key for each parameter
        )

    st.session_state["user_params"] = user_params
    return user_params


# ----------------- 📌 Sidebar: Mode Selection ----------------- #
def get_mode_selection(mode_range):
    """Creates a mode selection dropdown inside the sidebar."""
    st.sidebar.header("Mode Selection")
    selected_mode = st.sidebar.slider("Select a Mode", 1, mode_range, 1, key="mode_slider")
    return selected_mode - 1  # Convert to zero-based index


# ----------------- 📌 Simulation Execution ----------------- #
def run_simulation(user_params):
    """Runs the simulation using the selected parameters."""
    return main_vsm_infinite.main_vsm_infinite(user_params)


# ----------------- 📌 Visualization ----------------- #
def visualization(testResults):
    """Generates plots and displays test results based on simulation output."""
    state_variables = [
        "Theta0", "Tef0", "Qof0", "Vof0", "winv0", "Psif0", "Iid0", "Iiq0",
        "Vcd0", "Vcq0", "Iod0", "Ioq0"
    ]

    st.subheader("🔹 Simulation Test Results")

    # ✅ Display Parameters
    with st.expander("📌 Simulation Parameters", expanded=False):
        st.json(testResults[1][0])  # Dictionary of parameters

    # ✅ Display Eigenvalue Analysis
    with st.expander("🔹 Eigenvalue Analysis", expanded=True):
        st.write(f"**Eigenvalues:** {testResults[1][1]}")
        st.write(f"**Max Real Value:** {testResults[1][2]}")
        st.write(f"**Min Damping Ratio:** {testResults[1][3]}")
        st.write(f"**Power Flow Exit Flag:** {testResults[1][5]}")

    # ✅ Display Modal Analysis (NEW)
    with st.expander("📊 Modal Analysis", expanded=True):
        modal_analysis_data = testResults[1][4]  # Extract modal analysis results

        if isinstance(modal_analysis_data, list):
            st.write("### Mode Details:")
            for i, mode in enumerate(modal_analysis_data[1:]):  # Skip the header row
                mode_num = i + 1
                st.write(f"#### Mode {mode_num}:")
                st.write(f"  - **Eigenvalue:** {mode[1]}")
                st.write(f"  - **Damping Ratio:** {mode[3]}")
                st.write(f"  - **Frequency:** {mode[2]}")
                st.write(f"  - **Participation Factors:** {mode[5] if len(mode) > 5 else 'N/A'}")
        else:
            st.error("Modal Analysis data is unavailable or improperly formatted.")

    # ✅ Extract Mode Data for Visualization
    mode_data_raw = testResults[1][4]
    modes = mode_data_raw[1:] if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode' else mode_data_raw
    mode_range = len(modes)

    # Get mode selection from sidebar
    mode_index = get_mode_selection(mode_range)

    try:
        eigenvalue_real = float(np.real(testResults[1][1][mode_index]))
        eigenvalue_imag = float(np.imag(testResults[1][1][mode_index]))
    except IndexError:
        st.error("Eigenvalue data is unavailable.")
        return

    participation_factors = modes[mode_index][5] if len(modes[mode_index]) > 5 else []
    valid_factors = [(entry[0], float(entry[2])) for entry in participation_factors if isinstance(entry[0], int)]

    factor_magnitudes = [entry[1] for entry in valid_factors]
    dominant_state_names = [state_variables[entry[0] - 1] for entry in valid_factors]

    # ✅ Visualization
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(f"Participation Factor Distribution for Mode {mode_index + 1}")
        if factor_magnitudes:
            pie_chart_fig = px.pie(
                names=dominant_state_names,
                values=factor_magnitudes,
                width=1000,
                height=800
            )
            st.plotly_chart(pie_chart_fig, use_container_width=True)

    with col2:
        st.subheader("Heatmap of Participation Factors for All Modes")
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


# ----------------- 📌 Run Simulation & Visualization ----------------- #
def run_simulation_and_visualization():
    """Runs the simulation and visualization process, ensuring parameters are not duplicated."""
    user_params = get_user_inputs()  # Get user parameters
    testResults = run_simulation(user_params)  # Run simulation
    visualization(testResults)  # Show visualization


# ----------------- 📌 Main Page Layout ----------------- #
def main():
    st.title("VSM Infinite System Analysis")
    run_simulation_and_visualization()


if __name__ == "__main__":
    main()
