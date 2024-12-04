import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# Function to parse and display data based on testResults
def heatmap(testResults):
    # Extract the parameters and modes from testResults
    parameter_list = [str(row[0]) for row in testResults[1:]]
    mode_range = len(testResults[1][4])  # Number of modes available in the results

    # Sidebar for parameter selection
    selected_parameter = st.sidebar.selectbox("Select a Parameter", parameter_list)
    parameter_index = parameter_list.index(selected_parameter)  # Get index of selected parameter

    # Sidebar for mode selection
    selected_mode = st.sidebar.slider("Select a Mode", 1, mode_range, 1)
    mode_index = selected_mode - 1  # Mode index for accessing data

    # Extracting values for the selected parameter and mode
    parameter_data = testResults[parameter_index + 1]
    mode_data = parameter_data[4][mode_index]  # Extract mode-specific data

    # Eigenvalues
    eigenvalue_real = np.real(parameter_data[1][mode_index])
    eigenvalue_imag = np.imag(parameter_data[1][mode_index])

    # Participation Factors
    participation_factors = mode_data[5]
    state_locations = [entry[0] for entry in participation_factors]
    factor_magnitudes = [entry[2] for entry in participation_factors]

    # Display Eigenvalue Information
    st.header(f"Parameter: {selected_parameter} | Mode {selected_mode}")
    st.subheader("Eigenvalue Information")
    st.write(f"**Real Part:** {eigenvalue_real}")
    st.write(f"**Imaginary Part:** {eigenvalue_imag}")
    st.write(f"**Frequency (Hz):** {np.abs(eigenvalue_imag / (2 * np.pi))}")
    st.write(f"**Damping Ratio:** {mode_data[4]}")

    # Create DataFrame for Participation Factors
    participation_df = pd.DataFrame({
        "State Location": state_locations,
        "Participation Factor Magnitude": factor_magnitudes
    })

    # Plot Heatmap
    st.subheader("Participation Factor Heatmap")
    heatmap_fig = px.imshow(
        np.array([factor_magnitudes]),
        x=[f"State {loc}" for loc in state_locations],
        y=[f"Mode {selected_mode}"],
        labels={"color": "Participation Factor"},
        color_continuous_scale="Blues",
        title=f"Participation Factors for Mode {selected_mode}"
    )
    st.plotly_chart(heatmap_fig)

    # Plot Participation Factor Bar Chart
    st.subheader("Participation Factors Bar Chart")
    bar_chart_fig = px.bar(
        participation_df,
        x="State Location",
        y="Participation Factor Magnitude",
        title=f"Participation Factors for Mode {selected_mode}",
        color="Participation Factor Magnitude",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(bar_chart_fig)
