import streamlit as st
import importlib

# Set page layout **before any other Streamlit command**
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
    module = importlib.import_module(PAGES[selected_page])  # Import the correct script dynamically
    module.main()  # Call its main() function
