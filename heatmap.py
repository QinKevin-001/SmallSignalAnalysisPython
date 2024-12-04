import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import math

# Example Data (Replace with your actual data)
stateVariableNames = ['P01', 'Qo1', 'phid1', 'phiq1', 'gammad1', 'gammaq1', 'iid1', 'iiq1', 'vcd1', 'vcq1', 'iod1', 'ioq1']
numeigs = 10
modeNames = [f"Mode {i}" for i in range(1, numeigs + 1)]
pmatrixabs = np.random.rand(len(stateVariableNames), numeigs)  # Random participation factor data for example

# Interactive Heatmap
st.subheader("Interactive Participation Factor Heatmap")
df_heatmap = pd.DataFrame(pmatrixabs, index=stateVariableNames, columns=modeNames)
fig_heatmap = px.imshow(
    df_heatmap,
    labels=dict(x="Modes", y="State Variables", color="Participation Factor"),
    x=modeNames,
    y=stateVariableNames,
    color_continuous_scale="Blues",
    title="Participation Factor Heatmap"
)
fig_heatmap.update_layout(
    height=600,  # Adjust height for better visibility
    xaxis_title="Modes",
    yaxis_title="State Variables",
    font=dict(size=14)
)
st.plotly_chart(fig_heatmap)  # Heatmap with hover functionality

# Sidebar for Mode Selection
mode_index = st.sidebar.selectbox(
    "Select a Mode for Participation Factor Analysis",
    list(range(1, numeigs + 1))  # Dropdown for mode numbers
)

# Dynamic Pie Chart
selected_mode_column = pmatrixabs[:, mode_index - 1]  # Get participation factors for the selected mode
df_pie = pd.DataFrame({
    "State Variables": stateVariableNames,
    "Participation Factor": selected_mode_column
})
df_pie["State Variables"] = np.where(df_pie["Participation Factor"] < 0.02, "Other States", df_pie["State Variables"])  # Group small factors

st.subheader(f"Participation Factor Analysis for Mode {mode_index}")
fig_pie = px.pie(
    df_pie,
    names="State Variables",
    values="Participation Factor",
    title=f"Participation Factor Analysis for Mode {mode_index}",
    color_discrete_sequence=px.colors.sequential.Blues
)
st.plotly_chart(fig_pie)  # Pie chart with hover functionality

# Eigenvalue Analysis
eigvals = np.random.randn(numeigs) + 1j * np.random.randn(numeigs)  # Random eigenvalues for example
realpart = eigvals.real
imagpart = eigvals.imag
frequency = imagpart / (2 * math.pi)
dampingratio = -realpart / np.sqrt(realpart**2 + imagpart**2)

# Create Eigenvalue Analysis Table
df_eigen = pd.DataFrame({
    "Mode": range(1, numeigs + 1),
    "Real Part": realpart,
    "Imaginary Part": imagpart,
    "Frequency (Hz)": np.abs(frequency),
    "Damping Ratio": dampingratio
})

st.subheader("Eigenvalue Analysis")
st.dataframe(df_eigen)
