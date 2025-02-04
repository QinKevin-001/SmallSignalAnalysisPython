import streamlit as st
import importlib
import sys
import os  # Needed to check if images exist

# Set page layout (must be the first Streamlit command)
st.set_page_config(layout="wide")

# Define available visualization pages
PAGES = {
    "Main Page": "vis_main",
    "Droop Infinite": "vis_droop_infinite",
    "Droop Plant Infinite": "vis_droopPlant_infinite",
    "Droop Simplified Infinite": "vis_droopSimplified_infinite",
    "GFL Infinite": "vis_gfl_infinite",
    "GFL Plant Infinite": "vis_gflPlant_infinite"
}

# Sidebar tabs
nav_tab, sim_param_tab = st.sidebar.tabs(["Navigation", "Simulation Parameters"])

# Navigation Tab
with nav_tab:
    st.header("Navigation")
    selected_page = st.radio("Select Analysis Type", list(PAGES.keys()))

# Main Page Content
if selected_page == "Main Page":
    st.title("Power System Stability Analysis")
    st.write("""
    This tool allows users to analyze different power system cases. 
    Select a case from the navigation tab to view simulations.
    """)

    # Case explanations with images
    case_descriptions = {
        "Droop Infinite": "A droop-controlled inverter connected to an infinite bus.",
        "Droop Plant Infinite": "A plant-level droop controller interacting with an infinite bus.",
        "Droop Simplified Infinite": "A simplified droop control model.",
        "GFL Infinite": "A Grid-Following (GFL) inverter connected to an infinite bus.",
        "GFL Plant Infinite": "A GFL plant interacting with an infinite bus."
    }

    for case, description in case_descriptions.items():
        st.subheader(case)
        st.write(description)

        # Construct the image path
        image_path = f"images/{case.replace(' ', '_').lower()}.png"

        # Check if the image exists before loading it
        if os.path.exists(image_path):
            st.image(image_path, width=600)
        else:
            st.warning(f"Image for '{case}' not found: {image_path}")

else:
    # Dynamically load the selected script
    module_name = PAGES[selected_page]

    if module_name in sys.modules:
        module = sys.modules[module_name]
        importlib.reload(module)
    else:
        module = importlib.import_module(module_name)

    # Simulation Parameters Tab
    with sim_param_tab:
        module.get_user_inputs()  # Load the parameter input UI

    # Run the selected visualization (excluding parameter input)
    module.run_simulation_and_visualization()
