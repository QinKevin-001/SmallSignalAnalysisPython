
import streamlit as st
import importlib
import sys
import os
from urllib.parse import unquote
from gsheet_logger import log_interaction
import socket
import time

# === CONFIG ===
CREDENTIALS_PATH = "one-hz-oscillation-logs-97d1c076d6ed.json"
POWERPLANT_IMAGE = "Images/powerplant.png"
IMAGE_PATH = "Images"

# Case mapping
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

# Set layout
st.set_page_config(layout="wide")

# Utility to get IP
def get_user_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Unknown"

# Load query param
query_params = st.query_params
case_param = query_params.get("case", "")
preselected_case = None
if case_param:
    case_param = unquote(case_param).zfill(2)
    for title in CASES:
        if f"case {case_param}" in title.lower():
            preselected_case = title
            break

if "selected_case" not in st.session_state:
    st.session_state.selected_case = preselected_case

# === CASE PAGE ===
if st.session_state.selected_case:
    case_title = st.session_state.selected_case
    module_path = CASES[case_title]

    st.sidebar.success(f"Viewing: {case_title}")
    if st.button("⬅️ Back to Home"):
        st.session_state.selected_case = None
        st.rerun()

    st.image(POWERPLANT_IMAGE, width=300, caption="Loading Simulation...")
    time.sleep(1)

    try:
        if module_path in sys.modules:
            module = sys.modules[module_path]
            importlib.reload(module)
        else:
            module = importlib.import_module(module_path)
        module.main()
    except Exception as e:
        st.error(f"❌ Failed to load {module_path}: {e}")

# === HOME PAGE ===
else:
    st.title("⚡ Power System Stability Analysis")
    st.markdown("Explore simulation cases involving inverter-based resources (IBRs), grid-forming/following controllers, and synchronous generators.")

    st.header("🔍 Select a Simulation Case")
    cols = st.columns(3)

    for i, case_title in enumerate(CASES):
        preview_img = os.path.join(IMAGE_PATH, case_title.replace(" ", "_").lower() + ".png")
        with cols[i % 3]:
            st.markdown(f'''
                <style>
                .preview-button {{
                    position: relative;
                }}
                .preview-button:hover .hover-img {{
                    display: block;
                }}
                .hover-img {{
                    display: none;
                    position: absolute;
                    top: 100%;
                    left: 0;
                    z-index: 100;
                    width: 300px;
                    border: 1px solid #ccc;
                    background: #fff;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                </style>
                <div class="preview-button">
                    <form action="?case={str(i+1).zfill(2)}" method="get">
                        <button type="submit">{case_title}</button>
                    </form>
                    <img class="hover-img" src="{preview_img}">
                </div>
            ''', unsafe_allow_html=True)

    if preselected_case:
        log_interaction(
            credentials_path=CREDENTIALS_PATH,
            ip_address=get_user_ip(),
            case_title=preselected_case,
            source="URL Param"
        )
