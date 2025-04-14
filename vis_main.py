import streamlit as st
import importlib
import sys
import os
from datetime import datetime

# Set page layout
st.set_page_config(layout="wide")

# Define visualization case titles and module names
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

# Sidebar Navigation
selected_page = st.sidebar.selectbox(
    "Quick Navigation:",
    ["Main Page"] + list(PAGES.keys()),
    key="nav_selection"
)

# ----------------- 🏠 MAIN PAGE CONTENT ----------------- #
if selected_page == "Main Page":
    st.title("⚡ Power System Stability Analysis")
    st.markdown("""
    Explore dynamic responses of inverter-based resources (IBRs), grid-following/grid-forming controls, and synchronous generators in various system configurations.
    """)

    # Section 1: Navigation buttons for all cases
    st.header("🔍 Explore Simulation Cases")
    cols = st.columns(3)
    for i, (title, _) in enumerate(PAGES.items()):
        if cols[i % 3].button(title, key=f"btn_{i}"):
            # Log interaction
            with open("interaction_log.txt", "a") as log:
                log.write(f"{datetime.now().isoformat()} - Clicked: {title}\n")

            # Show transition and load new page
            st.toast(f"Opening {title}", icon="📊")
            st.session_state["nav_selection"] = title
            st.experimental_rerun()

    st.markdown("---")

    # Section 2: System Configurations
    st.header("🗺️ System Configuration Diagrams")
    st.write("Below are representative system layouts used in the ECCE 2025 digest.")
    for case_title in PAGES.keys():
        config_image = f"configurations/{case_title.replace(' ', '_').lower()}.png"
        st.subheader(case_title)
        if os.path.exists(config_image):
            st.image(config_image, width=800, caption="System layout")
        else:
            st.info("📄 No configuration diagram available for this case.")

# ----------------- 📄 CASE PAGE LOADING ----------------- #
else:
    module_name = PAGES[selected_page]

    try:
        # Import or reload the module dynamically
        if module_name in sys.modules:
            module = sys.modules[module_name]
            importlib.reload(module)
        else:
            module = importlib.import_module(module_name)

        # Show transition
        with st.spinner(f"Loading {selected_page}..."):
            st.toast(f"Entering {selected_page}", icon="⚙️")
            module.main()
    except ModuleNotFoundError:
        st.error(f"❌ Module `{module_name}` not found. Check that the file exists in `/Visualization/`.")
    except AttributeError:
        st.error(f"❌ Module `{module_name}` does not contain a `main()` function.")
