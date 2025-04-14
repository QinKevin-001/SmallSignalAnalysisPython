import streamlit as st
import importlib
import sys
import os
from datetime import datetime

st.set_page_config(layout="wide")

# Enhanced CSS for consistent row spacing and better responsive design
st.markdown("""
<style>
    /* Enhanced button styling */
    .stButton button {
        border: 4px solid rgba(49, 51, 63, 0.2) !important;
        border-radius: 6px !important;
        height: 100% !important;
        width: 100% !important;
    }

    /* Main container styling */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Row container styling */
    .row-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
        width: 100%;
    }

    /* Button container styling */
    .button-container {
        flex: 1;
        min-width: 0;
        max-width: 400px;
    }

    /* Last row specific styling */
    .row-container.last-row {
        justify-content: center;
    }

    .row-container.last-row .button-container {
        flex: 0 1 calc(33.33% - 1rem);
    }

    /* Tablet-specific styling (iPad) */
    @media (max-width: 992px) {
        .row-container {
            padding: 0 1rem;
            flex-wrap: wrap;
        }

        .button-container {
            flex: 0 1 calc(50% - 0.5rem);
        }

        .row-container.last-row .button-container {
            flex: 0 1 calc(50% - 0.5rem);
        }
    }

    /* Mobile-specific styling */
    @media (max-width: 640px) {
        .row-container {
            flex-direction: column;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }

        .button-container {
            flex: 1;
            width: 100%;
        }

        .stButton button {
            margin: 0 !important;
            padding: 0.5rem !important;
            min-height: 45px;
            white-space: normal;
            word-wrap: break-word;
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

    # Create a container for better control of layout
    container = st.container()

    # Calculate number of rows needed (ceil division)
    num_cases = len(CASES)
    cases_per_row = 3
    num_rows = (num_cases + cases_per_row - 1) // cases_per_row

    # Convert cases to list for easier indexing
    cases_list = list(CASES.keys())

    # Wrap all rows in a main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Create rows and columns
    for row in range(num_rows):
        start_idx = row * cases_per_row
        end_idx = min((row + 1) * cases_per_row, num_cases)
        cases_in_row = end_idx - start_idx

        # Add last-row class if it's the final row
        row_class = "row-container last-row" if row == num_rows - 1 else "row-container"
        st.markdown(f'<div class="{row_class}">', unsafe_allow_html=True)

        # Create columns for the current row
        cols = st.columns(cases_per_row)

        # Create buttons for this row
        for i in range(cases_in_row):
            case_idx = start_idx + i
            case_title = cases_list[case_idx]
            with cols[i]:
                st.markdown('<div class="button-container">', unsafe_allow_html=True)
                if st.button(case_title, key=f"btn_{case_idx}", use_container_width=True):
                    with open("interaction_log.txt", "a") as log:
                        log.write(f"{datetime.now().isoformat()} - Clicked: {case_title}\n")
                    st.session_state.selected_case = case_title
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.header("🗺️ System Configuration Diagrams")
    for case_title in CASES:
        st.subheader(case_title)
        image_path = f"configurations/{case_title.replace(' ', '_').lower()}.png"
        if os.path.exists(image_path):
            st.image(image_path, width=800)
        else:
            st.info("⚠️ No diagram found.")