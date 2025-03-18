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

def get_user_inputs():
    """Creates user input controls for parameter tuning via the sidebar."""
    st.sidebar.header("Simulation Parameters")

    # Create tabs for different parameter groups
    ibr1_tab, ibr2_tab, line_tab, load_tab = st.sidebar.tabs(["IBR1 (VSM Plant)", "IBR2 (VSM Plant)", "Line Parameters", "Load Parameters"])

    user_params = {}

    # IBR1 Parameters
    with ibr1_tab:
        st.header("IBR1 Plant-Level Parameters")
        ibr1_plant_params = [
            "PsetPlant", "QsetPlant", "ωsetPlant", "VsetPlant",
            "KpPLLPlant", "KiPLLPlant", "KpPlantP", "KiPlantP",
            "KpPlantQ", "KiPlantQ", "ωcPLLPlant", "ωcPlant", "tDelay"
        ]

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
        ibr1_sys_params = [
            "ωset", "Vset", "mp", "mq", "Rt", "Lt", "Rd",
            "Cf", "Rc", "Lc", "J1", "K1", "τf1"
        ]

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

    # IBR2 Parameters
    with ibr2_tab:
        st.header("IBR2 Plant-Level Parameters")
        # Same parameters as IBR1 but will be handled differently in the simulation
        ibr2_plant_params = [
            "PsetPlant", "QsetPlant", "ωsetPlant", "VsetPlant",
            "KpPLLPlant", "KiPLLPlant", "KpPlantP", "KiPlantP",
            "KpPlantQ", "KiPlantQ", "ωcPLLPlant", "ωcPlant", "tDelay"
        ]

        for var in ibr2_plant_params:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            min_val, max_val, default = float(min_val), float(max_val), float(default)
            step = float((max_val - min_val) / 100.0)

            # Store with _IBR2 suffix to differentiate
            user_params[f"{var}_IBR2"] = st.number_input(
                f"{var} ({min_val:.3f} to {max_val:.3f})",
                min_value=min_val,
                max_value=max_val,
                value=default,
                step=step,
                format="%.3f",
                key=f"ibr2_plant_{var}"
            )

        st.header("IBR2 System Parameters")
        ibr2_sys_params = [
            "ωset", "Vset", "mp", "mq", "Rt", "Lt", "Rd",
            "Cf", "Rc", "Lc", "J2", "K2", "τf2"
        ]

        for var in ibr2_sys_params:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            min_val, max_val, default = float(min_val), float(max_val), float(default)
            step = float((max_val - min_val) / 100.0)

            # Store with _IBR2 suffix to differentiate (except for J2, K2, τf2 which are already specific to IBR2)
            if var in ["J2", "K2", "τf2"]:
                user_params[var] = st.number_input(
                    f"{var} ({min_val:.3f} to {max_val:.3f})",
                    min_value=min_val,
                    max_value=max_val,
                    value=default,
                    step=step,
                    format="%.3f",
                    key=f"ibr2_sys_{var}"
                )
            else:
                user_params[f"{var}_IBR2"] = st.number_input(
                    f"{var} ({min_val:.3f} to {max_val:.3f})",
                    min_value=min_val,
                    max_value=max_val,
                    value=default,
                    step=step,
                    format="%.3f",
                    key=f"ibr2_sys_{var}"
                )

    # Line Parameters
    with line_tab:
        st.header("Line Parameters")
        line_params = ["Rline", "Lline"]
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
                key=f"line_{var}"
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

def run_simulation(user_params):
    """Runs the simulation with the current parameters."""
    # For this specific simulation, we don't need to transform the parameters
    return case13main_vsmPlant_vsmPlant.main_vsmPlant_vsmPlant(user_params)

def visualization(testResults):
    """Generates the eigenvalue and participation factor plots based on simulation output."""
    # Define state variables - corrected list with proper ordering
    state_variables = [
        "epsilonPLLPlant(IBR1)", "wPlant(IBR1)", "epsilonP(IBR1)", "epsilonQ(IBR1)", "PoPlant(IBR1)", "QoPlant(IBR1)",
        "PsetDelay(IBR1)", "QsetDelay(IBR1)", "theta(IBR1)", "Tef(IBR1)", "Qof(IBR1)", "Vof(IBR1)", "winv(IBR1)",
        "psif(IBR1)", "iid(IBR1)", "iiq(IBR1)", "vcd(IBR1)", "vcq(IBR1)", "iod(IBR1)", "ioq(IBR1)",
        "epsilonPLLPlant(IBR2)", "wPlant(IBR2)", "epsilonP(IBR2)", "epsilonQ(IBR2)", "PoPlant(IBR2)", "QoPlant(IBR2)",
        "PsetDelay(IBR2)", "QsetDelay(IBR2)", "theta(IBR2)", "Tef(IBR2)", "Qof(IBR2)", "Vof(IBR2)", "winv(IBR2)",
        "psif(IBR2)", "iid(IBR2)", "iiq(IBR2)", "vcd(IBR2)", "vcq(IBR2)", "iod(IBR2)", "ioq(IBR2)",
        "ilineD(Line1)", "ilineQ(Line1)", "ilineD(Line2)", "ilineQ(Line2)", "IloadD(Load)", "IloadQ(Load)"
    ]

    # Extract mode data with robust error handling
    try:
        # Debug information
        st.sidebar.write(f"Total results length: {len(testResults)}")
        st.sidebar.write(f"Eigenvalues length: {len(testResults[1][1])}")

        mode_data_raw = testResults[1][4]

        # Determine if the first element is a header row
        if isinstance(mode_data_raw[0], list) and len(mode_data_raw[0]) > 0 and mode_data_raw[0][0] == 'Mode':
            modes = mode_data_raw[1:]  # Skip header
        else:
            modes = mode_data_raw

        # Get the actual number of modes from eigenvalues
        eigenvalues = testResults[1][1]
        mode_range = len(eigenvalues)

        st.sidebar.write(f"Number of modes from eigenvalues: {mode_range}")
        st.sidebar.write(f"Number of modes from mode data: {len(modes)}")

        # If there's a mismatch, use the eigenvalues count
        if len(modes) < mode_range:
            st.warning(f"Mode data incomplete. Using eigenvalues count ({mode_range}) instead of mode data count ({len(modes)}).")
            # Pad the modes list if needed
            while len(modes) < mode_range:
                modes.append([len(modes)+1, eigenvalues[len(modes)], None, None, None, []])

    except (IndexError, TypeError) as e:
        st.error(f"Error extracting mode data: {e}")
        return

    # Mode selection
    st.sidebar.header("Mode Selection")
    selected_mode = st.sidebar.slider(
        "Select Mode",
        1,
        mode_range,
        1,
        key="mode_slider"
    )
    mode_index = selected_mode - 1

    # Extract eigenvalues with error handling
    try:
        eigenvalue_real = float(np.real(eigenvalues[mode_index]))
        eigenvalue_imag = float(np.imag(eigenvalues[mode_index]))
        st.sidebar.write(f"Eigenvalue: {eigenvalue_real:.3f} + {eigenvalue_imag:.3f}j")
    except (IndexError, TypeError, ValueError) as e:
        st.error(f"Error extracting eigenvalue data for mode {selected_mode}: {e}")
        return

    # Process participation factors with robust error handling
    try:
        # Check if we have participation factors for this mode
        if mode_index < len(modes) and len(modes[mode_index]) > 5 and modes[mode_index][5] is not None:
            participation_factors = modes[mode_index][5]

            # Filter valid factors and handle potential index errors
            valid_factors = []
            for entry in participation_factors:
                try:
                    if isinstance(entry[0], int) and 1 <= entry[0] <= len(state_variables):
                        state_idx = entry[0] - 1
                        factor_value = float(entry[2])
                        valid_factors.append((state_idx, factor_value, state_variables[state_idx]))
                except (IndexError, ValueError, TypeError):
                    continue

            # Extract data for visualization
            factor_magnitudes = [factor[1] for factor in valid_factors]
            dominant_state_names = [factor[2] for factor in valid_factors]

            if not valid_factors:
                st.warning("No valid participation factors found for this mode")
        else:
            st.warning(f"No participation factor data available for mode {selected_mode}")
            factor_magnitudes = []
            dominant_state_names = []
    except Exception as e:
        st.error(f"Error processing participation factors: {e}")
        factor_magnitudes = []
        dominant_state_names = []

    # Visualization
    col1, col2 = st.columns([1, 1])

    # Pie chart
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
            st.info("No participation factor data available for this mode.")

    # Heatmap
    with col2:
        st.subheader("Heatmap of Participation Factors for All Modes")
        try:
            # Create a dictionary to store participation factors
            heatmap_data = {}

            # Process all modes that have participation factors
            for mode_idx in range(min(len(modes), mode_range)):
                if len(modes[mode_idx]) > 5 and modes[mode_idx][5] is not None:
                    for entry in modes[mode_idx][5]:
                        try:
                            if isinstance(entry[0], int) and 1 <= entry[0] <= len(state_variables):
                                state_name = state_variables[entry[0]-1]
                                if state_name not in heatmap_data:
                                    heatmap_data[state_name] = [0] * mode_range
                                heatmap_data[state_name][mode_idx] = float(entry[2])
                        except (IndexError, ValueError, TypeError):
                            continue

            if heatmap_data:
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
            else:
                st.info("No participation factor data available for heatmap.")
        except Exception as e:
            st.error(f"Error creating heatmap: {e}")

def main():
    """Main function to handle user inputs, simulation, and visualization."""
    st.title("VSM Plant + VSM Plant System Analysis")
    user_params = get_user_inputs()
    testResults = run_simulation(user_params)
    visualization(testResults)

if __name__ == "__main__":
    main()