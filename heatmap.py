import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Function to parse and display data based on testResults
def heatmap(testResults):
    # Extract the parameters and modes from testResults
    parameter_list = [str(row[0]) for row in testResults[1:]]
    mode_range = len(testResults[1][4]) - 1  # Number of modes available in the results

    # Sidebar for parameter and mode selection
    selected_parameter = st.sidebar.selectbox("Select a Parameter", parameter_list)
    parameter_index = parameter_list.index(selected_parameter)  # Get index of selected parameter
    selected_mode = st.sidebar.slider("Select a Mode", 1, mode_range, 1)
    mode_index = selected_mode  # Adjust for zero-based indexing

    # Extracting data for the selected parameter and mode
    parameter_data = testResults[parameter_index + 1]
    mode_data = parameter_data[4][mode_index]  # Extract mode-specific data

    # Eigenvalues
    try:
        eigenvalue_real = np.real(parameter_data[1][mode_index])
        eigenvalue_imag = np.imag(parameter_data[1][mode_index])
    except IndexError:
        st.error("Eigenvalue data is unavailable or malformed for the selected parameter or mode.")
        return

    # Participation Factors
    participation_factors = mode_data[5] if len(mode_data) > 5 else []
    if not participation_factors:
        st.error(f"No participation factors found for Parameter: {selected_parameter}, Mode: {selected_mode}")
        return

    try:
        state_locations = [entry[0] for entry in participation_factors]
        factor_magnitudes = [entry[2] for entry in participation_factors]
    except (IndexError, TypeError):
        st.error(f"Participation factors are malformed for Parameter: {selected_parameter}, Mode: {selected_mode}")
        st.write("Participation Factors Raw Data:", participation_factors)
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
        names=[f"State {loc}" for loc in state_locations],
        values=factor_magnitudes,
        title=f"Participation Factor Distribution for Parameter {selected_parameter}, Mode {selected_mode}"
    )
    st.plotly_chart(pie_chart_fig)

    # Heatmap for Each Parameter
    st.subheader("Heatmap of Participation Factors for All Modes (Per Parameter)")
    heatmap_data = []
    max_state_count = 0  # Track maximum states across modes

    # Prepare heatmap data and handle cases with varying state locations
    for mode_idx in range(mode_range):
        try:
            mode_participation = parameter_data[4][mode_idx][5]  # Access participation factors for each mode
            magnitudes = [entry[2] for entry in mode_participation]
            heatmap_data.append(magnitudes)
            max_state_count = max(max_state_count, len(magnitudes))  # Track max number of states
        except IndexError:
            heatmap_data.append([])  # Handle missing modes gracefully

    # Pad rows with zeros to ensure uniform length
    heatmap_data_padded = [
        row + [0] * (max_state_count - len(row)) for row in heatmap_data
    ]

    # Generate heatmap labels dynamically
    state_labels = [f"State {i}" for i in range(max_state_count)]
    mode_labels = [f"Mode {i + 1}" for i in range(mode_range)]

    # Plot the heatmap
    heatmap_fig = px.imshow(
        np.array(heatmap_data_padded),
        x=state_labels,
        y=mode_labels,
        labels={"color": "Participation Factor"},
        color_continuous_scale="Blues",
        title=f"Participation Factors Heatmap for Parameter {selected_parameter}"
    )
    st.plotly_chart(heatmap_fig)
