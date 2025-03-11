import streamlit as st
import numpy as np
import plotly.express as px
from Main import case08main_droop_droop

# Set page layout if desired (uncomment to use wide layout)
# st.set_page_config(layout="wide")

# Variable ranges for Droop-Droop System
variable_ranges = {
    # IBR1 parameters
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
    # IBR2 parameters
    "Pset_IBR2": (0.0, 1.0),
    "Qset_IBR2": (-1.0, 1.0),
    "ωset_IBR2": (1.0, 1.0),
    "Vset_IBR2": (0.9, 1.1),
    "mp_IBR2": (0.01, 1.00),
    "mq_IBR2": (0.01, 1.00),
    "Rt_IBR2": (0.01, 1.0),
    "Lt_IBR2": (0.01, 1.0),
    "Rd_IBR2": (0.0, 100.0),
    "Cf_IBR2": (0.01, 0.20),
    "Rc_IBR2": (0.01, 1.0),
    "Lc_IBR2": (0.01, 1.0),
    "KpV_IBR2": (0.1, 10.0),
    "KiV_IBR2": (0.1, 1000.0),
    "KpC_IBR2": (0.1, 10.0),
    "KiC_IBR2": (0.1, 1000.0),
    "ωc_IBR2": (float(2 * np.pi * 1), float(2 * np.pi * 20)),
    # Load parameters
    "Rload": (0.5, 10.0),
    "Lload": (0.1, 10.0),
    "Rx": (100.0, 1000.0)
}

# Default values based on provided parameters
wbase = 2 * np.pi * 60
default_values = {
    # IBR1 parameters
    "Pset": 0.1,
    "Qset": 0.0,
    "ωset": 1.0,
    "Vset": 1.0,
    "mp": 0.05,
    "mq": 0.05,
    "Rt": 0.02,
    "Lt": 0.10,
    "Rd": 0.00,
    "Cf": 0.05,
    "Rc": 0.10,
    "Lc": 0.50,
    "KpV": 4.0,
    "KiV": 15.0,
    "KpC": 0.4,
    "KiC": 8.0,
    "ωc": 2 * np.pi * 5,
    # IBR2 parameters
    "Pset_IBR2": 0.1,
    "Qset_IBR2": 0.0,
    "ωset_IBR2": 1.0,
    "Vset_IBR2": 1.0,
    "mp_IBR2": 0.05,
    "mq_IBR2": 0.05,
    "Rt_IBR2": 0.02,
    "Lt_IBR2": 0.10,
    "Rd_IBR2": 0.00,
    "Cf_IBR2": 0.05,
    "Rc_IBR2": 0.10,
    "Lc_IBR2": 0.50,
    "KpV_IBR2": 4.0,
    "KiV_IBR2": 15.0,
    "KpC_IBR2": 0.4,
    "KiC_IBR2": 8.0,
    "ωc_IBR2": 2 * np.pi * 5,
    # Load parameters
    "Rload": 0.9,
    "Lload": 0.4358,
    "Rx": 100
}


def get_user_inputs():
    """Creates user input controls for parameter tuning via the sidebar."""
    st.sidebar.header("Simulation Parameters")

    # Create tabs for different parameter groups
    ibr1_tab, ibr2_tab, load_tab = st.sidebar.tabs(["IBR1 Parameters", "IBR2 Parameters", "Load Parameters"])

    user_params = {}

    # IBR1 Parameters
    with ibr1_tab:
        st.header("IBR1 Parameters")
        ibr1_params = [param for param in variable_ranges.keys() if
                       not param.endswith('_IBR2') and param not in ['Rload', 'Lload', 'Rx']]
        for var in ibr1_params:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            # Convert all numeric values to float
            min_val = float(min_val)
            max_val = float(max_val)
            default = float(default)
            step = float((max_val - min_val) / 100.0)  # Adjusted step size for better control

            user_params[var] = st.number_input(
                f"{var} ({min_val:.3f} to {max_val:.3f})",
                min_value=min_val,
                max_value=max_val,
                value=default,
                step=step,
                format="%.3f",  # Format to 3 decimal places
                key=f"ibr1_{var}"
            )

    # IBR2 Parameters
    with ibr2_tab:
        st.header("IBR2 Parameters")
        ibr2_params = [param for param in variable_ranges.keys() if param.endswith('_IBR2')]
        for var in ibr2_params:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            # Convert all numeric values to float
            min_val = float(min_val)
            max_val = float(max_val)
            default = float(default)
            step = float((max_val - min_val) / 100.0)  # Adjusted step size for better control

            user_params[var] = st.number_input(
                f"{var.replace('_IBR2', '')} ({min_val:.3f} to {max_val:.3f})",
                min_value=min_val,
                max_value=max_val,
                value=default,
                step=step,
                format="%.3f",  # Format to 3 decimal places
                key=f"ibr2_{var}"
            )

    # Load Parameters
    with load_tab:
        st.header("Load Parameters")
        load_params = ['Rload', 'Lload', 'Rx']
        for var in load_params:
            min_val, max_val = variable_ranges[var]
            default = default_values.get(var, (min_val + max_val) / 2.0)
            # Convert all numeric values to float
            min_val = float(min_val)
            max_val = float(max_val)
            default = float(default)
            step = float((max_val - min_val) / 100.0)  # Adjusted step size for better control

            user_params[var] = st.number_input(
                f"{var} ({min_val:.3f} to {max_val:.3f})",
                min_value=min_val,
                max_value=max_val,
                value=default,
                step=step,
                format="%.3f",  # Format to 3 decimal places
                key=f"load_{var}"
            )

    return user_params

def prepare_simulation_parameters(user_params):
    """Prepares the parameters in the format expected by the simulation function."""
    # Separate parameters for IBR1, IBR2, and Load
    ibr1_params = {}
    ibr2_params = {}
    load_params = {}

    for key, value in user_params.items():
        if key.endswith('_IBR2'):
            # Remove the '_IBR2' suffix and add to IBR2 parameters
            ibr2_params[key.replace('_IBR2', '')] = value
        elif key in ['Rload', 'Lload', 'Rx']:
            load_params[key] = value
        else:
            ibr1_params[key] = value

    return {
        'parasIBR1': ibr1_params,
        'parasIBR2': ibr2_params,
        'parasLoad': load_params
    }

def run_simulation(user_params):
    """Runs the Droop-Droop simulation with the current parameters."""
    sim_params = prepare_simulation_parameters(user_params)
    return case08main_droop_droop.main_droop_droop(sim_params)

def visualization(testResults):
    """Generates the eigenvalue and participation factor plots based on simulation output."""
    state_variables = [
        'Po(IBR1)', 'Qo(IBR1)', 'phid(IBR1)', 'phiq(IBR1)', 'gammad(IBR1)', 'gammaq(IBR1)', 'iid(IBR1)',
        'iiq(IBR1)', 'vcd(IBR1)', 'vcq(IBR1)', 'iod(IBR1)', 'ioq(IBR1)',
        'theta(IBR2)', 'Po(IBR2)', 'Qo(IBR2)', 'phid(IBR2)', 'phiq(IBR2)', 'gammad(IBR2)', 'gammaq(IBR2)', 'iid(IBR2)',
        'iiq(IBR2)', 'vcd(IBR2)', 'vcq(IBR2)', 'iod(IBR2)', 'ioq(IBR2)',
        'iloadD(Load)', 'iloadQ(Load)'
    ]

    # The modal analysis data is expected to be stored at index 4 of the second element
    mode_data_raw = testResults[1][4]

    # If the first entry is a header, skip it
    if isinstance(mode_data_raw[0], list) and mode_data_raw[0][0] == 'Mode':
        modes = mode_data_raw[1:]
    else:
        modes = mode_data_raw

    mode_range = len(modes)

    # Allow user to select a mode for closer inspection
    selected_mode = st.sidebar.slider(
        "Select a Mode",
        1,
        mode_range,
        1,
        key="mode_selector"  # Add unique key for mode selector
    )
    mode_index = selected_mode - 1

    parameter_data = testResults[1]
    try:
        eigenvalue_real = np.real(parameter_data[1][mode_index])
        eigenvalue_imag = np.imag(parameter_data[1][mode_index])
    except IndexError:
        st.error("Eigenvalue data is unavailable.")
        return

    try:
        participation_factors = modes[mode_index][5] if len(modes[mode_index]) > 5 else []
        if participation_factors:
            valid_factors = [
                entry for entry in participation_factors
                if isinstance(entry[0], (int, np.integer)) and 1 <= entry[0] <= len(state_variables)
            ]
            state_locations = [entry[0] for entry in valid_factors]
            factor_magnitudes = [entry[2] for entry in valid_factors]
            dominant_state_names = [state_variables[loc - 1] for loc in state_locations]
        else:
            factor_magnitudes = []
            dominant_state_names = []
    except (IndexError, ValueError, TypeError):
        st.error("Error parsing participation factors.")
        return

    # Layout the plots in two equal columns
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
        heatmap_data = []
        for mode_idx in range(mode_range):
            mode_values = np.zeros(len(state_variables))
            try:
                mode_participation = modes[mode_idx][5]
                for entry in mode_participation:
                    if isinstance(entry[0], (int, np.integer)) and 1 <= entry[0] <= len(state_variables):
                        mode_values[entry[0] - 1] = entry[2]
            except (IndexError, ValueError):
                pass
            heatmap_data.append(mode_values)

        mode_labels = [f"Mode {i + 1}" for i in range(mode_range)]
        heatmap_fig = px.imshow(
            np.array(heatmap_data).T,
            x=mode_labels,
            y=state_variables,
            labels={"color": "Participation Factor"},
            color_continuous_scale="Blues",
            title="Participation Factors Heatmap",
            width=900, height=700
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)

def main():
    """Main function to handle user inputs, simulation, and visualization."""
    st.title("Droop-Droop System Analysis")
    user_params = get_user_inputs()
    testResults = run_simulation(user_params)  # Run simulation with current parameters
    visualization(testResults)                # Generate updated plots

# Expose the main function for multipage navigation
if __name__ == "__main__":
    main()