import streamlit as st
import numpy as np
import plotly.express as px
import main_droop_infinite  # Import simulation script

# Updated Variable Limits
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
    "KpV": (0.1, 10.0),
    "KiV": (0.1, 1000.0),
    "KpC": (0.1, 10.0),
    "KiC": (0.1, 1000.0),
    "ωc": (float(2 * np.pi * 1), float(2 * np.pi * 20))
}

# Default values
default_values = {
    "Pset": float(1.0), "Qset": float(0.0),
    "ωset": float(1.0), "Vset": float(1.0),
    "mp": float(0.05), "mq": float(0.05),
    "Rt": float(0.02), "Lt": float(0.10),
    "Rd": float(0.00), "Cf": float(0.05),
    "Rc": float(0.10), "Lc": float(0.50),
    "KpV": float(1.8), "KiV": float(160.0),
    "KpC": float(0.4), "KiC": float(8.0),
    "ωc": float(2 * np.pi * 5)
}


def get_user_inputs():
    """Creates user input controls for variable tuning inside a separate tab."""
    sim_param_tab = st.sidebar.tabs(["Simulation Parameters"])[0]
    with sim_param_tab:
        st.header("Simulation Parameters")
        user_params = {}

        for var, (min_val, max_val) in variable_ranges.items():
            user_params[var] = st.number_input(
                f"{var} ({min_val} to {max_val})",
                min_value=float(min_val),
                max_value=float(max_val),
                value=float(default_values[var]),
                step=round((float(max_val) - float(min_val)) / 100, 3)
            )

        st.session_state["user_params"] = user_params
        return user_params


def run_simulation(user_params):
    """Runs the simulation using the selected parameters."""
    return main_droop_infinite.main_droop_infinite(user_params)


def visualization(testResults):
    """Generates plots based on testResults."""
    state_variables = [
        "Theta0", "Po0", "Qo0", "Phid0", "Phiq0", "Gammad0", "Gammaq0",
        "Iid0", "Iiq0", "Vcd0", "Vcq0", "Iod0", "Ioq0"
    ]

    mode_data_raw = testResults[1][4]
    modes = mode_data_raw[1:] if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode' else mode_data_raw
    mode_range = len(modes)

    # Move mode selection inside the Simulation Parameters Tab
    sim_param_tab = st.sidebar.tabs(["Simulation Parameters"])[0]
    with sim_param_tab:
        selected_mode = st.slider("Select a Mode", 1, mode_range, 1)
        mode_index = selected_mode - 1

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

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(f"Participation Factor Distribution for Mode {selected_mode}")
        if factor_magnitudes:
            pie_chart_fig = px.pie(names=dominant_state_names, values=factor_magnitudes, width=1000, height=800)
            st.plotly_chart(pie_chart_fig, use_container_width=True)

    with col2:
        st.subheader("Heatmap of Participation Factors for All Modes")
        heatmap_data = [np.zeros(len(state_variables)) for _ in range(mode_range)]

        for mode_idx in range(mode_range):
            for entry in modes[mode_idx][5]:
                if isinstance(entry[0], int) and 1 <= entry[0] <= len(state_variables):
                    heatmap_data[mode_idx][entry[0] - 1] = float(entry[2])

        heatmap_fig = px.imshow(np.array(heatmap_data).T, x=[f"Mode {i + 1}" for i in range(mode_range)],
                                y=state_variables, width=1000, height=800)
        st.plotly_chart(heatmap_fig, use_container_width=True)


def main():
    st.title("Droop Infinite System Analysis")
    run_simulation_and_visualization()


if __name__ == "__main__":
    main()
