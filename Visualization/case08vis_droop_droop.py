import streamlit as st
import numpy as np
import plotly.express as px
from Main import case08main_droop_droop

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
    "ωc": (float(2 * np.pi * 1), float(2 * np.pi * 20)),
    "Rload": (0.5, 10.0),
    "Lload": (0.1, 10.0),
    "Rx": (100.0, 1000.0)
}

# Default values from `case08main_droop_droop.py`
default_values = {
    "Pset": 0.1, "Qset": 0.0,
    "ωset": 1.0, "Vset": 1.0,
    "mp": 0.05, "mq": 0.05,
    "Rt": 0.02, "Lt": 0.10,
    "Rd": 0.00, "Cf": 0.05,
    "Rc": 0.10, "Lc": 0.50,
    "KpV": 4.0, "KiV": 15.0,
    "KpC": 0.4, "KiC": 8.0,
    "ωc": float(2 * np.pi * 5),
    "Rload": 0.9, "Lload": 0.4358, "Rx": 100
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
    """Creates a mode selection slider inside the sidebar."""
    st.sidebar.header("Mode Selection")
    selected_mode = st.sidebar.slider("Select a Mode", 1, mode_range, 1, key="mode_slider")
    return selected_mode - 1  # Convert to zero-based index


# ----------------- 📌 Simulation Execution ----------------- #
def run_simulation(user_params):
    """Runs the simulation using the selected parameters."""
    return case08main_droop_droop.main_droop_droop(user_params)


# ----------------- 📌 Visualization ----------------- #
def visualization(testResults):
    """Generates plots based on testResults."""
    # Extract mode data. If a header row is present, skip it.
    mode_data_raw = testResults[1][4]
    modes = mode_data_raw[1:] if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode' else mode_data_raw
    mode_range = len(modes)

    mode_index = get_mode_selection(mode_range)

    try:
        eigenvalue_real = float(np.real(testResults[1][1][mode_index]))
        eigenvalue_imag = float(np.imag(testResults[1][1][mode_index]))
    except IndexError:
        st.error("Eigenvalue data is unavailable.")
        return

    # 🔹 Extract participation factors for the selected mode.
    # Skip the header row if it exists (e.g., if the first element is a string or contains "State Location")
    part_factors = modes[mode_index][5]
    if isinstance(part_factors[0], str) or (isinstance(part_factors[0], list) and "State Location" in part_factors[0]):
        part_factors = part_factors[1:]

    st.write("DEBUG: Participation Factors (Mode {}):".format(mode_index + 1), part_factors)

    # Extract valid factors with fallback for missing dominant state names.
    valid_factors = []
    for entry in part_factors:
        if isinstance(entry[0], int):
            state_name = entry[3] if entry[3] else f"UnnamedState{entry[0]}"
            unique_label = f"PF {entry[0]}: {state_name} ({entry[4]})"
            valid_factors.append((entry[0], float(entry[2]), unique_label))

    if not valid_factors:
        st.error("No valid participation factors found. Check if participation factor indices are correct.")
        return

    factor_magnitudes = [pf[1] for pf in valid_factors]
    dominant_state_names = [pf[2] for pf in valid_factors]

    col1, col2 = st.columns([1, 1])

    # Pie Chart for Selected Mode
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

    # Heatmap across all modes
    with col2:
        st.subheader("Heatmap of Participation Factors for All Modes")
        heatmap_data = {}

        # Process all modes
        for mode_idx in range(mode_range):
            part_data = modes[mode_idx][5]
            # Skip header row if present
            if isinstance(part_data[0], str) or (isinstance(part_data[0], list) and "State Location" in part_data[0]):
                part_data = part_data[1:]
            # Optional: sort by state location (the first column)
            part_data_sorted = sorted(part_data, key=lambda row: row[0])
            for entry in part_data_sorted:
                if isinstance(entry[0], int):
                    state_name = entry[3] if entry[3] else f"UnnamedState{entry[0]}"
                    unique_key = f"PF {entry[0]}: {state_name} ({entry[4]})"
                    if unique_key not in heatmap_data:
                        heatmap_data[unique_key] = [0] * mode_range
                    heatmap_data[unique_key][mode_idx] = float(entry[2])

        # Sort the heatmap rows based on the PF index extracted from the key
        def pf_sort_key(key):
            try:
                # key format: "PF {index}: ..."
                pf_index_str = key.split(":")[0].split()[1]
                return int(pf_index_str)
            except Exception:
                return 9999

        sorted_items = sorted(heatmap_data.items(), key=lambda x: pf_sort_key(x[0]))
        sorted_keys = [item[0] for item in sorted_items]
        sorted_values = [item[1] for item in sorted_items]
        heatmap_array = np.array(sorted_values)

        heatmap_fig = px.imshow(
            heatmap_array,
            x=[f"Mode {i + 1}" for i in range(mode_range)],
            y=sorted_keys,
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
    st.title("Droop + Droop System Analysis")
    run_simulation_and_visualization()


if __name__ == "__main__":
    main()
