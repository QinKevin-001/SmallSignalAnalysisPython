import streamlit as st
import importlib
import sys

# Set page layout (must be the first Streamlit command)
st.set_page_config(layout="wide")

# Define available visualization pages
PAGES = {
    "Droop Infinite": "vis_droop_infinite",
    "Droop Plant Infinite": "vis_droopPlant_infinite",
    "Droop Simplified Infinite": "vis_droopSimplified_infinite",
    "GFL Infinite": "vis_gfl_infinite",
    "GFL Plant Infinite": "vis_gflPlant_infinite"
}

# Create sidebar tabs
tabs = st.sidebar.tabs(["Navigation", "Simulation Parameters"])

# Navigation Tab
with tabs[0]:
    st.title("Navigation")
    selected_page = st.radio("Go to:", list(PAGES.keys()))

# Dynamically import and run the selected page module
module_name = PAGES[selected_page]

if module_name in sys.modules:
    module = sys.modules[module_name]  # Assign the existing module
    importlib.reload(module)  # Reload to ensure latest updates
else:
    module = importlib.import_module(module_name)  # Import dynamically

# Run the selected page's `main()` function
module.main()
