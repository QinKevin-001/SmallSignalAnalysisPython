import streamlit as st
import numpy as np
import plotly.express as px
import main_droop_infinite  # Import simulation script

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
    "KpV": (0.1, 10.0),
    "KiV": (0.1, 1000.0),
    "KpC": (0.1, 10.0),
    "KiC": (0.1, 1000.0),
    "ωc": (float(2 * np.pi * 1), float(2 * np.pi * 20))
}

# Default values from `main_droop_infinite.py`
default_values = {
    "Pset": 1.0, "Qset": 0.0,
    "ωset": 1.0, "Vset": 1.0,
    "mp": 0.05, "mq": 0.05,
    "Rt": 0.02, "Lt": 0.10,
    "Rd": 0.00, "Cf": 0.05,
    "Rc": 0.10, "Lc": 0.50,
    "KpV": 1.8, "KiV": 160.0,
    "KpC": 0.4, "KiC": 8.0,
    "ωc": float(2 * np.pi * 5)
}

# ----------------- 📌 Sidebar: Simulation Parameters ----------------- #
def get_user_inputs():
    """Creates user input controls inside the Simulation Parameters tab, ensuring unique widget keys."""

    if "user_params" not in st.session_state:
        st.session_state["user_params"] = {key: default_values[key] for key in variable_ranges}

    user_params = {}

    # Create a Simulation Parameters Sidebar (This will only appear in Tab 2)
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


# ----------------- 📌 Run Simulation & Visualization ----------------- #
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

    # Get mode selection from the sidebar
    mode_index = get_mode_selection(mode_range)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(f"Participation Factor Distribution for Mode {mode_index + 1}")
        pie_chart_fig = px.pie(
            names=state_variables,
            values=[np.random.random() for _ in state_variables],  # Replace with real data
            width=800,
            height=600
        )
        st.plotly_chart(pie_chart_fig, use_container_width=True)

    with col2:
        st.subheader("Heatmap of Participation Factors for All Modes")
        heatmap_fig = px.imshow(np.random.rand(len(state_variables), mode_range),  # Replace with real data
                                x=[f"Mode {i+1}" for i in range(mode_range)],
                                y=state_variables,
                                width=800,
                                height=600)
        st.plotly_chart(heatmap_fig, use_container_width=True)


def run_simulation_and_visualization():
    """Runs the simulation and visualization process."""
    user_params = get_user_inputs()
    testResults = run_simulation(user_params)
    visualization(testResults)


def main():
    st.title("Droop Infinite System Analysis")
    run_simulation_and_visualization()


if __name__ == "__main__":
    main()
