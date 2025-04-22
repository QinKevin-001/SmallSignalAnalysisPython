import streamlit as st
import importlib
import sys
import os
from datetime import datetime
import time

st.set_page_config(layout="wide")

# Enhanced CSS for consistent row spacing
st.markdown("""
<style>
    .stButton button {
        border: 4px solid rgba(49, 51, 63, 0.2) !important;
        border-radius: 6px !important;
    }

    .row-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    @media (max-width: 640px) {
        .stButton button {
            width: 100%;
            margin: 0 !important;
            padding: 0.5rem !important;
            height: auto;
            min-height: 45px;
            white-space: normal;
            word-wrap: break-word;
        }

        .row-container {
            flex-direction: column;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# CASES dictionary with display titles (removed diagram mapping since it's now on main page)
CASES = {
    "Case 01: Droop Simplified Infinite": {
        "module": "Visualization.case01vis_droopSimplified_infinite",
        "display_title": "Droop Simplified Infinite System Analysis"
    },
    "Case 02: Droop Infinite": {
        "module": "Visualization.case02vis_droop_infinite",
        "display_title": "Droop Infinite System Analysis"
    },
    "Case 03: Droop Plant Infinite": {
        "module": "Visualization.case03vis_droopPlant_infinite",
        "display_title": "Droop Plant Infinite System Analysis"
    },
    "Case 04: GFL Infinite": {
        "module": "Visualization.case04vis_gfl_infinite",
        "display_title": "Grid-Following Infinite System Analysis"
    },
    "Case 05: GFL Plant Infinite": {
        "module": "Visualization.case05vis_gflPlant_infinite",
        "display_title": "Grid-Following Plant Infinite System Analysis"
    },
    "Case 06: VSM Infinite": {
        "module": "Visualization.case06vis_vsm_infinite",
        "display_title": "Virtual Synchronous Machine Infinite System Analysis"
    },
    "Case 07: VSM Plant Infinite": {
        "module": "Visualization.case07vis_vsmPlant_infinite",
        "display_title": "Virtual Synchronous Machine Plant Infinite System Analysis"
    },
    "Case 08: Droop Droop": {
        "module": "Visualization.case08vis_droop_droop",
        "display_title": "Droop-Droop System Analysis"
    },
    "Case 09: Droop Plant Droop Plant": {
        "module": "Visualization.case09vis_droopPlant_droopPlant",
        "display_title": "Droop Plant - Droop Plant System Analysis"
    },
    "Case 10: Droop VSM": {
        "module": "Visualization.case10vis_droop_vsm",
        "display_title": "Droop-VSM System Analysis"
    },
    "Case 11: Droop Plant VSM Plant": {
        "module": "Visualization.case11vis_droopPlant_vsmPlant",
        "display_title": "Droop Plant - VSM Plant System Analysis"
    },
    "Case 12: VSM VSM": {
        "module": "Visualization.case12vis_vsm_vsm",
        "display_title": "VSM-VSM System Analysis"
    },
    "Case 13: VSM Plant VSM Plant": {
        "module": "Visualization.case13vis_vsmPlant_vsmPlant",
        "display_title": "VSM Plant - VSM Plant System Analysis"
    },
    "Case 14: Droop SG": {
        "module": "Visualization.case14vis_droop_sg",
        "display_title": "Droop-Synchronous Generator System Analysis"
    },
    "Case 15: Droop Plant SG": {
        "module": "Visualization.case15vis_droopPlant_sg",
        "display_title": "Droop Plant - Synchronous Generator System Analysis"
    },
    "Case 16: VSM SG": {
        "module": "Visualization.case16vis_vsm_sg",
        "display_title": "VSM-Synchronous Generator System Analysis"
    },
    "Case 17: VSM Plant SG": {
        "module": "Visualization.case17vis_vsmPlant_sg",
        "display_title": "VSM Plant - Synchronous Generator System Analysis"
    }
}

# Initialize session states
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None
if "returning_home" not in st.session_state:
    st.session_state.returning_home = False

# ---------------- CASE VIEW ----------------
if st.session_state.selected_case:
    case_title = st.session_state.selected_case
    case_info = CASES.get(case_title)
    module_path = case_info["module"]
    display_title = case_info["display_title"]

    try:
        # Show only the display title (not the case number)
        st.title(display_title)
        st.markdown("---")  # Add a separator

        # Load and run the case module
        if module_path in sys.modules:
            module = sys.modules[module_path]
            importlib.reload(module)
        else:
            module = importlib.import_module(module_path)

        # Run the main visualization
        module.main()

        # Add spacing before the home button
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Position the button at the bottom left
        if st.button("⬅️ Back to Home", key="home_button"):
            with st.toast("Returning to home..."): time.sleep(1)
            st.session_state.selected_case = None
            st.rerun()

    except Exception as e:
        st.error(f"❌ Error loading `{module_path}`: {e}")

# ---------------- HOME PAGE ----------------
else:
    if st.session_state.returning_home:
        st.session_state.returning_home = False
        st.rerun()

    st.title("Interactive Visualization of Grid Interactive Inverter-Based Resources")
    st.markdown("""
    Explore simulation cases involving inverter-based resources (IBRs), grid-following/grid-forming controllers, and synchronous generators.
    """)

    # Display the TestSystem.png on the main page
    image_path = "fig/TestSystem.png"
    if os.path.exists(image_path):
        st.image(image_path, use_column_width="always") ## double check dep
        caption_html = """
        <p style='
            text-align: center;
            color: black;
            font-size: 18px;
            font-family: Arial;
            font-weight: bold;
            margin-top: -10px;
            margin-bottom: 20px;
        '>
            System Configuration
        </p>
        """
        st.markdown(caption_html, unsafe_allow_html=True)
    else:
        st.info("⚠️ System configuration diagram not found.")

    st.header("Select a Simulation Case")

    # Create rows and columns for case buttons
    container = st.container()
    num_cases = len(CASES)
    cases_per_row = 3
    num_rows = (num_cases + cases_per_row - 1) // cases_per_row
    cases_list = list(CASES.keys())

    def handle_case_click(case_title):
        with open("interaction_log.txt", "a") as log:
            log.write(f"{datetime.now().isoformat()} - Clicked: {case_title}\n")
        with st.toast("Loading case..."): time.sleep(1)
        st.session_state.selected_case = case_title
        st.rerun()

    for row in range(num_rows):
        with container.container():
            st.markdown('<div class="row-container">', unsafe_allow_html=True)

            # Special handling for the last row
            if row == num_rows - 1 and num_cases % cases_per_row != 0:
                cols = st.columns([0.75, 1, 1, 0.75])
                remaining_cases = num_cases % cases_per_row
                for i in range(remaining_cases):
                    case_idx = row * cases_per_row + i
                    if cols[i+1].button(cases_list[case_idx], key=f"btn_{case_idx}", use_container_width=True):
                        handle_case_click(cases_list[case_idx])
            else:
                cols = st.columns(cases_per_row)
                for col in range(cases_per_row):
                    idx = row * cases_per_row + col
                    if idx < num_cases:
                        if cols[col].button(cases_list[idx], key=f"btn_{idx}", use_container_width=True):
                            handle_case_click(cases_list[idx])

            st.markdown('</div>', unsafe_allow_html=True)