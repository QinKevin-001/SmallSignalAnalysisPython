import streamlit as st
import numpy as np
import plotly.express as px

def heatmap(testResults):
    # State variable mapping
    state_variables = [
        "Theta0", "Po0", "Qo0", "Phid0", "Phiq0", "Gammad0", "Gammaq0",
        "Iid0", "Iiq0", "Vcd0", "Vcq0", "Iod0", "Ioq0"
    ]

    # Extract parameters and modes
    parameter_list = [str(row[0]) for row in testResults[1:]]
    modes = testResults[1][4]  # Modes for the first parameter
    mode_range = len(modes)  # Correct total number of modes (should be 8)

    # Sidebar for user selection
    selected_parameter = st.sidebar.selectbox("Select a Parameter", parameter_list)
    parameter_index = parameter_list.index(selected_parameter)

    # Slider with exact mode range (1 to mode_range)
    selected_mode = st.sidebar.slider("Select a Mode", 1, mode_range, 1)
    mode_index = selected_mode - 1  # Convert to 0-based indexing for internal use

    # Extract data for the selected parameter and mode
    parameter_data = testResults[parameter_index + 1]
    try:
        mode_data = parameter_data[4][mode_index]  # Fetch mode-specific data
    except IndexError:
        st.error("Mode data is unavailable.")
        return

    # Eigenvalue information
    try:
        eigenvalue_real = np.real(parameter_data[1][mode_index])
        eigenvalue_imag = np.imag(parameter_data[1][mode_index])
    except IndexError:
        st.error("Eigenvalue data is unavailable.")
        return

    # Participation factors
    try:
        participation_factors = mode_data[5] if len(mode_data) > 5 else []
        if participation_factors:
            valid_factors = [
                entry for entry in participation_factors
                if isinstance(entry[0], (int, np.integer)) and 1 <= entry[0] <= len(state_variables)
            ]
            state_locations = [entry[0] for entry in valid_factors]
            factor_magnitudes = [entry[2] for entry in valid_factors]
            dominant_state_names = [state_variables[loc - 1] for loc in state_locations]
        else:
            valid_factors = []
            state_locations = []
            factor_magnitudes = []
            dominant_state_names = []
    except (IndexError, ValueError, TypeError):
        st.error("Error parsing participation factors.")
        return

    # Display eigenvalue information
    st.header(f"Parameter: {selected_parameter} | Mode {selected_mode}")
    st.subheader("Eigenvalue Information")
    st.write(f"**Real Part:** {eigenvalue_real}")
    st.write(f"**Imaginary Part:** {eigenvalue_imag}")
    st.write(f"**Frequency (Hz):** {np.abs(eigenvalue_imag / (2 * np.pi))}")
    st.write(f"**Damping Ratio:** {mode_data[4]}")

    # Pie Chart for participation factors
    st.subheader(f"Participation Factor Distribution for Mode {selected_mode}")
    if factor_magnitudes:
        pie_chart_fig = px.pie(
            names=dominant_state_names,
            values=factor_magnitudes,
            title=f"Participation Factor Distribution for Parameter {selected_parameter}, Mode {selected_mode}"
        )
        st.plotly_chart(pie_chart_fig)
    else:
        st.warning("No participation factor data available for this mode.")

    # Heatmap of participation factors
    st.subheader("Heatmap of Participation Factors for All Modes")
    heatmap_data = []
    for mode_idx in range(mode_range):
        mode_values = np.zeros(len(state_variables))  # Initialize all-zero participation values
        try:
            mode_participation = parameter_data[4][mode_idx][5]
            for entry in mode_participation:
                if isinstance(entry[0], (int, np.integer)) and 1 <= entry[0] <= len(state_variables):
                    mode_values[entry[0] - 1] = entry[2]  # Map to 0-based index
        except (IndexError, ValueError):
            pass
        heatmap_data.append(mode_values)

    # Correct heatmap data alignment
    mode_labels = [f"Mode {i + 1}" for i in range(mode_range)]  # Labels aligned to 1-based mode numbering
    heatmap_fig = px.imshow(
        np.array(heatmap_data).T,
        x=mode_labels,
        y=state_variables,
        labels={"color": "Participation Factor"},
        color_continuous_scale="Blues",
        title=f"Participation Factors Heatmap for Parameter {selected_parameter}"
    )
    st.plotly_chart(heatmap_fig)

# Example function call
# Replace `testResults` with your actual data
# heatmap(testResults)