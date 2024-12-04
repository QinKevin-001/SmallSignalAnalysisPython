import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import math

def heatmap():
    # Example Data
    # Replace with your actual state variables, eigenvalues, and participation matrix
    stateVariableNames = ['P01', 'Qo1', 'phid1', 'phiq1', 'gammad1', 'gammaq1', 'iid1', 'iiq1', 'vcd1', 'vcq1', 'iod1', 'ioq1']
    numeigs = 10
    modeNames = [f"Mode {i}" for i in range(1, numeigs + 1)]
    pmatrixabs = np.random.rand(len(stateVariableNames), numeigs)  # Random data for example

    # Create Heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pmatrixabs, annot=False, cmap="Blues", cbar=True, xticklabels=modeNames, yticklabels=stateVariableNames)
    plt.xlabel("Modes")
    plt.ylabel("State Variables")
    plt.title("Participation Factor Heatmap")
    st.pyplot(fig)

    # Create Dropdown for Mode Selection
    mode_index = st.sidebar.selectbox(
        "Select a Mode for Participation Factor Analysis",
        list(range(1, numeigs + 1))
    )

    # Generate Pie Chart for Selected Mode
    selected_mode_column = pmatrixabs[:, mode_index - 1]
    df = pd.DataFrame({
        "State Variables": stateVariableNames,
        "Participation Factor": selected_mode_column
    })
    df["State Variables"] = np.where(df["Participation Factor"] < 0.02, "Other States", df["State Variables"])

    fig_pie = px.pie(
        df,
        names="State Variables",
        values="Participation Factor",
        title=f"Participation Factor Analysis for Mode {mode_index}"
    )

    # Display Pie Chart
    st.plotly_chart(fig_pie)

    # Generate Eigenvalue Analysis Data
    eigvals = np.random.randn(numeigs) + 1j * np.random.randn(numeigs)  # Random complex eigenvalues for example
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

    st.write("Eigenvalue Analysis:")
    st.dataframe(df_eigen)
