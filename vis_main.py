import streamlit as st
import importlib
import os
import sys
from datetime import datetime

# Set page layout
st.set_page_config(layout="wide")

# Mapping of Case Title → Visualization Python Module Path
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

# Default state setup
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None

# -------------------- CASE VIEW MODE -------------------- #
if st.session_state.selected_case:
    case_title = st.session_state.selected_case
    module_path = CASES.get(case_title)

    st.sidebar.success(f"Viewing: {case_title}")

    if st.button("⬅️ Back to Main Page"):
        st.session_state.selected_case = None
        st.experimental_rerun()

    try:
        # Dynamically import the module
        if module_path in sys.modules:
            module = sys.modules[module_path]
            importlib.reload(module)
        else:
            module = importlib.import_module(module_path)

        with st.spinner(f"Loading {case_title}..."):
            st.toast(f"Showing {case_title}", icon="📊")
            module.main()
    except Exception as e:
        st.error(f"❌ Error loading `{module_path}`: {e}")

# -------------------- MAIN PAGE -------------------- #
else:
    st.title("⚡ Power System Stability Analysis")
    st.markdown("""
    Explore 17 dynamic simulation cases featuring inverter-based resources, grid-following/grid-forming controllers, and synchronous generators.
    """)

    st.header("🔍 Select a Simulation Case")
    cols = st.columns(3)

    for i, (case_title, _) in enumerate(CASES.items()):
        if cols[i % 3].button(case_title, key=f"casebtn_{i}"):
            with open("interaction_log.txt", "a") as log:
                log.write(f"{datetime.now().isoformat()} - Clicked: {case_title}\n")
            st.session_state.selected_case = case_title
            st.experimental_rerun()

    st.markdown("---")
    st.header("🗺️ System Configuration Diagrams")
    for case_title in CASES.keys():
        st.subheader(case_title)
        image_name = case_title.replace(" ", "_").lower()
        img_path = f"configurations/{image_name}.png"
        if os.path.exists(img_path):
            st.image(img_path, width=800)
        else:
            st.info("⚠️ No diagram available.")
