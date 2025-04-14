import streamlit as st
import importlib
import sys
import os
from datetime import datetime

st.set_page_config(layout="wide")

# Mapping: Case title -> module path
PAGES = {
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

# First-time setup
if "page_to_load" not in st.session_state:
    st.session_state.page_to_load = "Main Page"

# If flag set, rerun after setting state to simulate "instant redirect"
if "trigger_rerun" in st.session_state:
    del st.session_state["trigger_rerun"]
    st.experimental_rerun()

# ------------------------- CASE PAGE -------------------------
if st.session_state.page_to_load != "Main Page":
    selected_page = st.session_state.page_to_load
    st.sidebar.success(f"Viewing: {selected_page}")

    module_name = PAGES.get(selected_page)
    if module_name:
        try:
            if module_name in sys.modules:
                module = sys.modules[module_name]
                importlib.reload(module)
            else:
                module = importlib.import_module(module_name)

            with st.spinner(f"Loading {selected_page}..."):
                st.toast(f"Now viewing: {selected_page}", icon="📊")
                module.main()
        except Exception as e:
            st.error(f"❌ Failed to load `{module_name}`.\n\n{e}")
    else:
        st.error("❌ Invalid case selected.")

    if st.button("⬅️ Back to Main Page"):
        st.session_state.page_to_load = "Main Page"
        st.session_state.trigger_rerun = True

# ------------------------- MAIN PAGE -------------------------
else:
    st.title("⚡ Power System Stability Analysis")
    st.markdown("""
    Explore simulation cases involving inverter-based resources (IBRs), grid-following/grid-forming controls, and synchronous generators.
    """)

    st.header("🔍 Explore Simulation Cases")
    cols = st.columns(3)
    for i, (case_title, _) in enumerate(PAGES.items()):
        if cols[i % 3].button(case_title, key=f"btn_{i}"):
            # Log
            with open("interaction_log.txt", "a") as log:
                log.write(f"{datetime.now().isoformat()} - Clicked: {case_title}\n")

            # Set target page and rerun
            st.session_state.page_to_load = case_title
            st.session_state.trigger_rerun = True

    st.markdown("---")
    st.header("🗺️ System Configuration Diagrams")
    for case_title in PAGES:
        st.subheader(case_title)
        img_path = f"configurations/{case_title.replace(' ', '_').lower()}.png"
        if os.path.exists(img_path):
            st.image(img_path, width=800)
        else:
            st.info("⚠️ No diagram found for this case.")
