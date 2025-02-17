# Test confirmed

import streamlit as st
import importlib
import sys
import os  # Needed to check if images exist

# Set page layout (must be the first Streamlit command)
st.set_page_config(layout="wide")

# Define available visualization pages
PAGES = {
    "Main Page": None,
    "Droop Infinite": "vis_droop_infinite",
    "Droop Plant Infinite": "vis_droopPlant_infinite",
    "Droop Simplified Infinite": "vis_droopSimplified_infinite",
    "GFL Infinite": "vis_gfl_infinite",
    "GFL Plant Infinite": "vis_gflPlant_infinite",
    "VSM Infinite": "vis_vsm"
}

# ------------- 📌 Sidebar: Navigation (Dropdown) ------------- #
selected_page = st.sidebar.selectbox(
    "Select Analysis Type:",
    list(PAGES.keys()),
    key="nav_selection"
)

# ----------------- 🏠 Main Page Content ----------------- #
if selected_page == "Main Page":
    st.title("Power System Stability Analysis")
    st.write("""
    This tool allows users to analyze different power system cases. 
    Select a case from the **Navigation Panel** to view simulations.
    """)

    # Case explanations with images
    case_descriptions = {
        "Droop Infinite": "A droop-controlled inverter connected to an infinite bus.",
        "Droop Plant Infinite": "A plant-level droop controller interacting with an infinite bus.",
        "Droop Simplified Infinite": "A simplified droop control model.",
        "GFL Infinite": "A Grid-Following (GFL) inverter connected to an infinite bus.",
        "GFL Plant Infinite": "A GFL plant interacting with an infinite bus.",
        "VSM Infinite": "A Virtual Synchronous Machine (VSM) inverter connected to an infinite bus."
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

# ----------------- 📌 Load the Selected Page ----------------- #
else:
    module_name = PAGES[selected_page]

    if module_name:
        if module_name in sys.modules:
            module = sys.modules[module_name]
            importlib.reload(module)  # Reload to reflect any updates
        else:
            module = importlib.import_module(module_name)

        # Call the selected module's main() function, which internally handles parameter tuning
        module.main()
