import streamlit as st
import importlib
import sys
import os
from datetime import datetime

st.set_page_config(layout="wide")

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

if "selected_case" not in st.session_state:
    st.session_state.selected_case = None

# ---------- CASE PAGE ----------
if st.session_state.selected_case:
    case_title = st.session_state.selected_case
    module_path = CASES[case_title]

    st.sidebar.success(f"Viewing: {case_title}")

    # Back button: triggers a session change that will cause a re-render next time
    if st.button("⬅️ Back to Main Page"):
        st.session_state.selected_case = None

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
        st.error(f"❌ Could not load {module_path}: {e}")

# ---------- HOME PAGE ----------
else:
    st.title("⚡ Power System Stability Analysis")
    st.markdown("""
    Explore simulation cases involving inverter-based resources (IBRs), grid-forming/following controllers, and synchronous generators.
    """)

    st.header("🔍 Select a Simulation Case")
    cols = st.columns(3)

    # Force a visual refresh with a hidden key
    clicked_case = st.session_state.get("clicked_case", None)

    for i, case_title in enumerate(CASES.keys()):
        if cols[i % 3].button(case_title, key=f"btn_{i}"):
            # Log interaction
            with open("interaction_log.txt", "a") as log:
                log.write(f"{datetime.now().isoformat()} - Clicked: {case_title}\n")

            # Set a temp value
            st.session_state.clicked_case = case_title

    # Set actual state and trigger navigation
    if "clicked_case" in st.session_state and st.session_state.clicked_case:
        st.session_state.selected_case = st.session_state.clicked_case
        st.session_state.clicked_case = None
        st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🗺️ System Configuration Diagrams")
    for case_title in CASES.keys():
        st.subheader(case_title)
        image_path = f"configurations/{case_title.replace(' ', '_').lower()}.png"
        if os.path.exists(image_path):
            st.image(image_path, width=800)
        else:
            st.info("⚠️ No diagram found.")
