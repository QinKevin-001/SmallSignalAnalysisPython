import streamlit as st
import importlib
import sys
import os
from datetime import datetime

st.set_page_config(layout="wide")

# Enhanced CSS remains the same
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

# CASES dictionary remains the same
CASES = {
    "Case 01: Droop Simplified Infinite": "Visualization.case01vis_droopSimplified_infinite",
    # ... rest of the cases ...
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
        # Show the system configuration diagram for the selected case
        st.header("System Configuration")
        image_path = f"configurations/{case_title.replace(' ', '_').lower()}.png"
        if os.path.exists(image_path):
            st.image(image_path, width=800)
        else:
            st.info("⚠️ No diagram found for this case.")

        st.markdown("---")  # Add a separator

        # Load and run the case module
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
    st.title("Interactive Visualization of Grid Interactive Inverter-Based Resources")
    st.markdown("""
    Explore simulation cases involving inverter-based resources (IBRs), grid-following/grid-forming controllers, and synchronous generators.
    """)

    st.header("Select a Simulation Case")

    # Create a container for better control of layout
    container = st.container()

    # Calculate number of rows needed
    num_cases = len(CASES)
    cases_per_row = 3
    num_rows = (num_cases + cases_per_row - 1) // cases_per_row

    # Convert cases to list for easier indexing
    cases_list = list(CASES.keys())

    # Create rows and columns
    for row in range(num_rows):
        with container.container():
            st.markdown('<div class="row-container">', unsafe_allow_html=True)

            # Special handling for the last row
            if row == num_rows - 1 and num_cases % cases_per_row != 0:
                cols = st.columns([0.75, 1, 1, 0.75])
                remaining_cases = num_cases % cases_per_row
                for i in range(remaining_cases):
                    case_idx = row * cases_per_row + i
                    case_title = cases_list[case_idx]
                    if cols[i+1].button(case_title, key=f"btn_{case_idx}", use_container_width=True):
                        with open("interaction_log.txt", "a") as log:
                            log.write(f"{datetime.now().isoformat()} - Clicked: {case_title}\n")
                        st.session_state.selected_case = case_title
                        st.rerun()
            else:
                cols = st.columns(cases_per_row)
                for col in range(cases_per_row):
                    idx = row * cases_per_row + col
                    if idx < num_cases:
                        case_title = cases_list[idx]
                        if cols[col].button(case_title, key=f"btn_{idx}", use_container_width=True):
                            with open("interaction_log.txt", "a") as log:
                                log.write(f"{datetime.now().isoformat()} - Clicked: {case_title}\n")
                            st.session_state.selected_case = case_title
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)