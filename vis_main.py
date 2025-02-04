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

# Sidebar navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to:", list(PAGES.keys()))

# Dynamically import and run the selected page module
if selected_page in PAGES:
    module_name = PAGES[selected_page]

    # Check if module is already loaded to prevent reloading conflicts
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])  # Reload the module if it has been previously loaded
    else:
        module = importlib.import_module(module_name)  # Import the correct script dynamically

    # Run the selected page's `main()` function
    module.main()
