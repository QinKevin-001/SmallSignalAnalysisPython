import streamlit as st
import importlib
import sys
import os
from datetime import datetime

st.set_page_config(layout="wide")

# Enhanced CSS for consistent grid spacing
st.markdown("""
<style>
    /* Grid container for buttons */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* 3 buttons per row */
        gap: 1rem; /* Equal gap between buttons (both vertically and horizontally) */
        justify-items: center; /* Center buttons horizontally */
        align-items: center; /* Center buttons vertically */
    }

    /* Button styling */
    .stButton button {
        border: 4px solid rgba(49, 51, 63, 0.2) !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
    }

    /* Mobile-specific styling (phones) */
    @media (max-width: 480px) {
        .grid-container {
            grid-template-columns: 1fr; /* 1 button per row on mobile */
            gap: 0.5rem; /* Smaller gap on mobile */
        }

        .stButton button {
            width: 100%; /* Full width buttons on mobile */
        }
    }

    /* Tablet-specific styling */
    @media (min-width: 481px) and (max-width: 768px) {
        .grid-container {
            grid-template-columns: repeat(2, 1fr); /* 2 buttons per row on tablets */
            gap: 0.75rem; /* Medium gap on tablets */
        }
    }
</style>
""", unsafe_allow_html=True)

# Your existing CASES dictionary
CASES = {
    "Case 01: Droop Simplified Infinite": "Visualization.case01vis_droopSimplified_infinite",
    "Case 02: Droop Infinite": "Visualization.case02vis_droop_infinite",
    "Case 03: Droop Plant Infinite": "Visualization.case03vis_droopPlant_infinite",
    "Case 04: GFL Infinite": "Visualization.case04vis_gfl_infinite",
    "Case 05: GFL Plant Infinite": "Visualization.case05vis_gflPlant_infinite",
    "Case 06: VSM Infinite": "Visualization.case06vis_vsm_infinite",
    "Case 07: VSM Plant Infinite": "Visualization.case07vis_vsmPlant_infinite",
    "Case 08: Droop Droop": "Visualization.case08vis_droop_droop",
    "Case 09: Droop Plant Droop Plant": "Visualization.case09vis_droopPlant_droopPlant",
    "Case 10: Droop VSM": "Visualization.case10vis_droop_vsm",
    "Case 11: Droop Plant VSM Plant": "Visualization.case11vis_droopPlant_vsmPlant",
    "Case 12: VSM VSM": "Visualization.case12vis_vsm_vsm",
    "Case 13: VSM Plant VSM Plant": "Visualization.case13vis_vsmPlant_vsmPlant",
    "Case 14: Droop SG": "Visualization.case14vis_droop_sg",
    "Case 15: Droop Plant SG": "Visualization.case15vis_droopPlant_sg",
    "Case 16: VSM SG": "Visualization.case16vis_vsm_sg",
    "Case 17: VSM Plant SG": "Visualization.case17vis_vsmPlant_sg"
}

# Initialize session
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None

# ---------------- CASE VIEW ----------------
if st.session_state.selected_case:
    case_title = st.session_state.selected_case
    module_path = CASES.get(case_title)

    st.sidebar.success(f"Viewing: {case_title}")
    if st.button("⬅️ Home"):
        st.session_state.selected_case = None
        st.rerun()

    try:
        if module_path in sys.modules:
            module = sys.modules[module_path]
            importlib.reload(module)
        else:
            module = importlib.import_module(module_path)

        with st.spinner(f"Loading {case_title}..."):
            st.toast(f"Now viewing: {case_title}", icon="📊")
            module.main()
    except Exception as e:
        st.error(f"❌ Error loading `{module_path}`: {e}")

# ---------------- HOME PAGE ----------------
else:
    st.title("⚡ Power System Stability Analysis")
    st.markdown("""
    Explore simulation cases involving inverter-based resources (IBRs), grid-following/grid-forming controllers, and synchronous generators.
    """)

    st.header("🔍 Select a Simulation Case")

    # Create a grid container for buttons
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)

    # Add buttons to the grid
    for i, case_title in enumerate(CASES.keys()):
        if st.button(case_title, key=f"btn_{i}"):
            with open("interaction_log.txt", "a") as log:
                log.write(f"{datetime.now().isoformat()} - Clicked: {case_title}\n")
            st.session_state.selected_case = case_title
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # Close the grid container

    st.markdown("---")
    st.header("🗺️ System Configuration Diagrams")
    for case_title in CASES:
        st.subheader(case_title)
        image_path = f"configurations/{case_title.replace(' ', '_').lower()}.png"
        if os.path.exists(image_path):
            st.image(image_path, width=800)
        else:
            st.info("⚠️ No diagram found.")