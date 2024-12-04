import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Function to parse and display data based on testResults
def heatmap(testResults):
    # Provided state variable mapping
    state_variables = [
        "Theta0", "Po0", "Qo0", "Phid0", "Phiq0", "Gammad0", "Gammaq0",
        "Iid0", "Iiq0", "Vcd0", "Vcq0", "Iod0", "Ioq0"
    ]

    # Extract the parameters and modes from testResults
    parameter_list = [str(row[0]) for row in testResults[1:]]
    mode_range = len(testResults[1][4])   # Number of modes available in the results

    # Sidebar for parameter and mode selection
    selected_parameter = st.sidebar.selectbox("Select a Parameter", parameter_list)
    parameter_index = parameter_list.index(selected_parameter)  # Get index of selected parameter
    selected_mode = st.sidebar.slider("Select a Mode", 1, mode_range, 1)
    mode_index = selected_mode -1 # Adjust for zero-based indexing

    # Extracting data for the selected parameter and mode
    parameter_data = testResults[parameter_index + 1]
    try:
        mode_data = parameter_data[4][mode_index]  # Extract mode-specific data
    except IndexError:
        st.error(f"Mode data is unavailable for the selected parameter or mode.")
        return

    # Eigenvalues
    try:
        eigenvalue_real = np.real(parameter_data[1][mode_index])
        eigenvalue_imag = np.imag(parameter_data[1][mode_index])
    except IndexError:
        st.error("Eigenvalue data is unavailable or malformed for the selected parameter or mode.")
        return

    # Participation Factors
    try:
        participation_factors = mode_data[5] if len(mode_data) > 5 else []
        if not participation_factors:
            raise ValueError("Participation factors missing or malformed.")
    except (IndexError, ValueError, TypeError):
        st.error(f"Participation factors are malformed for Parameter: {selected_parameter}, Mode: {selected_mode}")
        st.write("Mode Data:", mode_data)
        return

    try:
        # Filter participation factors to skip headers or malformed entries
        valid_factors = [
            entry for entry in participation_factors
            if isinstance(entry[0], (int, np.integer)) and 1 <= entry[0] <= len(state_variables)
        ]
        state_locations = [entry[0] for entry in valid_factors]
        factor_magnitudes = [entry[2] for entry in valid_factors]
        dominant_state_names = [state_variables[loc - 1] for loc in state_locations]
    except (IndexError, ValueError, TypeError) as e:
        st.error("Error mapping state locations to dominant state names.")
        st.write("State Locations:", state_locations)
        st.write("Participation Factors:", participation_factors)
        return

    # Display Eigenvalue Information
    st.header(f"Parameter: {selected_parameter} | Mode {selected_mode}")
    st.subheader("Eigenvalue Information")
    st.write(f"**Real Part:** {eigenvalue_real}")
    st.write(f"**Imaginary Part:** {eigenvalue_imag}")
    st.write(f"**Frequency (Hz):** {np.abs(eigenvalue_imag / (2 * np.pi))}")
    st.write(f"**Damping Ratio:** {mode_data[4]}")

    # Pie Chart for Selected Parameter and Mode
    st.subheader(f"Participation Factor Distribution for Mode {selected_mode}")
    pie_chart_fig = px.pie(
        names=dominant_state_names,
        values=factor_magnitudes,
        title=f"Participation Factor Distribution for Parameter {selected_parameter}, Mode {selected_mode}"
    )
    st.plotly_chart(pie_chart_fig)

    # Heatmap for Each Parameter
    st.subheader("Heatmap of Participation Factors for All Modes (Per Parameter)")
    heatmap_data = []
    max_state_count = len(state_variables)  # Always map to predefined states

    # Prepare heatmap data for all modes
    for mode_idx in range(mode_range):
        try:
            mode_participation = parameter_data[4][mode_idx][5]  # Access participation factors for each mode
            mode_values = np.zeros(max_state_count)  # Initialize array for all states
            for entry in mode_participation:
                try:
                    # Ensure entry[0] is a valid integer and within range
                    if isinstance(entry[0], (int, np.integer)) and 1 <= entry[0] <= max_state_count:
                        state_idx = entry[0] - 1  # Map state location to 0-based index
                        mode_values[state_idx] = entry[2]  # Assign participation factor magnitude
                except (TypeError, ValueError) as e:
                    st.warning(f"Skipping invalid participation factor entry: {entry}")
            heatmap_data.append(mode_values)
        except (IndexError, ValueError):
            st.warning(f"Mode {mode_idx + 1} data is missing or malformed.")
            heatmap_data.append(np.zeros(max_state_count))  # Handle missing modes gracefully

    # X-axis: Modes, Y-axis: State Variables
    mode_labels = [f"Mode {i + 1}" for i in range(mode_range)]
    heatmap_fig = px.imshow(
        np.array(heatmap_data).T,  # Transpose to align modes (columns) and states (rows)
        x=mode_labels,
        y=state_variables,
        labels={"color": "Participation Factor"},
        color_continuous_scale="Blues",
        title=f"Participation Factors Heatmap for Parameter {selected_parameter}"
    )
    st.plotly_chart(heatmap_fig)

