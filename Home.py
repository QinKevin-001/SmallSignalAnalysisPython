# Add this near the top of the file, after the imports
def show_loading_message():
    with st.spinner("Loading..."):
        progress_bar = st.progress(0)
        for i in range(100):
            progress_bar.progress(i + 1)
            time.sleep(0.01)  # Adjust this value to control loading speed

# Add the time import at the top
import streamlit as st
import importlib
import sys
import os
from datetime import datetime
import time

# ... (keep all the CSS and CASES dictionary the same)

# Initialize session states
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None
if "loading" not in st.session_state:
    st.session_state.loading = False
if "returning_home" not in st.session_state:
    st.session_state.returning_home = False

# ---------------- CASE VIEW ----------------
if st.session_state.selected_case:
    case_title = st.session_state.selected_case
    case_info = CASES.get(case_title)
    module_path = case_info["module"]
    diagram_file = case_info["diagram"]

    st.sidebar.success(f"Viewing: {case_title}")
    if st.button("⬅️ Home"):
        st.session_state.returning_home = True
        show_loading_message()
        st.session_state.selected_case = None
        st.rerun()

    try:
        if st.session_state.loading:
            show_loading_message()
            st.session_state.loading = False
            st.rerun()

        # Show the system configuration diagram for the selected case
        st.header("System Configuration")
        image_path = f"fig/{diagram_file}"
        if os.path.exists(image_path):
            st.image(image_path, use_column_width="always")
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
    if st.session_state.returning_home:
        st.session_state.returning_home = False
        st.rerun()

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
                        st.session_state.loading = True
                        show_loading_message()
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
                            st.session_state.loading = True
                            show_loading_message()
                            st.session_state.selected_case = case_title
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)