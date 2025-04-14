import streamlit as st
import importlib
import sys
import os
from datetime import datetime

st.set_page_config(layout="wide")

# Map of display name to module path
CASES = {
    "Case 01: Droop Simplified Infinite": "Visualization.case01vis_droopSimplified_infinite",
    # ... rest of your cases ...
}

# Initialize session
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None

# ---------------- CASE VIEW ----------------
if st.session_state.selected_case:
    # ... your existing case view code ...

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

    # Create rows and columns
    for row in range(num_rows):
        cols = container.columns(cases_per_row)
        for col in range(cases_per_row):
            idx = row * cases_per_row + col
            if idx < num_cases:
                case_title = cases_list[idx]
                if cols[col].button(case_title, key=f"btn_{idx}", use_container_width=True):
                    with open("interaction_log.txt", "a") as log:
                        log.write(f"{datetime.now().isoformat()} - Clicked: {case_title}\n")
                    st.session_state.selected_case = case_title
                    st.rerun()

    st.markdown("---")
    st.header("🗺️ System Configuration Diagrams")
    for case_title in CASES:
        st.subheader(case_title)
        image_path = f"configurations/{case_title.replace(' ', '_').lower()}.png"
        if os.path.exists(image_path):
            st.image(image_path, width=800)
        else:
            st.info("⚠️ No diagram found.")