import streamlit as st

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

# Dynamically load the selected page
st.sidebar.write(f"**Current Selection:** {selected_page}")

# Run the selected visualization script
if selected_page in PAGES:
    script = PAGES[selected_page]
    st.experimental_rerun()  # Ensures page updates dynamically
    exec(open(f"{script}.py").read())  # Dynamically run the selected file
