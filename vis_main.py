import streamlit as st
import importlib
import sys
import os  # Needed to check if images exist

# Set page layout (must be the first Streamlit command)
st.set_page_config(layout="wide")

# Define available visualization pages (Now referencing the `Visualization` folder)
PAGES = {
    "Main Page": None,
    "Case 01: Droop Simplified Infinite": "Visualization.vis_droopSimplified_infinite",
    "Case 02: Droop Infinite": "Visualization.vis_droop_infinite",
    "Case 03: Droop Plant Infinite": "Visualization.vis_droopPlant_infinite",
    "Case 04: GFL Infinite": "Visualization.vis_gfl_infinite",
    "Case 05: GFL Plant Infinite": "Visualization.vis_gflPlant_infinite",
    "Case 06: VSM Infinite": "Visualization.vis_vsm_infinite",
    "Case 07: VSM Plant Infinite": "Visualization.vis_vsmPlant_infinite",
    "Case 08: Droop Droop": "Visualization.vis_droop_droop",
    "Case 09: Droop Plant Droop Plant": "Visualization.vis_droopPlant_droopPlant"
}

# ------------- 📌 Sidebar: Navigation (Dropdown) ------------- #
selected_page = st.sidebar.selectbox(
    "Select Analysis Type:",
    list(PAGES.keys()),
    key="nav_selection"
)

# ----------------- 🏠 Main Page Content ----------------- #
if selected_page == "Main Page":
    st.title("Power System Stability Analysis")
    st.write("""
    This tool allows users to analyze different power system cases. 
    Select a case from the **Navigation Panel** to view simulations.
    """)

    # Case explanations with images
    case_descriptions = {
        "Droop Simplified Infinite": "A simplified droop control model.",
        "Droop Infinite": "A droop-controlled inverter connected to an infinite bus.",
        "Droop Plant Infinite": "A plant-level droop controller interacting with an infinite bus.",
        "GFL Infinite": "A Grid-Following (GFL) inverter connected to an infinite bus.",
        "GFL Plant Infinite": "A GFL plant interacting with an infinite bus.",
        "VSM Infinite": "A Virtual Synchronous Machine (VSM) inverter connected to an infinite bus.",
        "VSM Plant Infinite": "A Virtual Synchronous Machine (VSM) inverter with plant control connected to an infinite bus.",
        "Droop Droop": "A system with two droop-controlled inverters (IBR1 and IBR2) connected to a shared load. This case studies the interaction between two droop controllers and a common load.",
        "Droop Plant Droop Plant": "Two droop plant-controlled inverters interacting."
    }

    for case, description in case_descriptions.items():
        st.subheader(case)
        st.write(description)

        # Construct the image path
        image_path = f"images/{case.replace(' ', '_').lower()}.png"

        # Check if the image exists before loading it
        if os.path.exists(image_path):
            st.image(image_path, width=600)
        else:
            st.warning(f"⚠️ Image for '{case}' not found: {image_path}")

# ----------------- 📌 Load the Selected Page ----------------- #
else:
    module_name = PAGES[selected_page]

    if module_name:
        try:
            if module_name in sys.modules:
                module = sys.modules[module_name]
                importlib.reload(module)  # Reload to reflect any updates
            else:
                module = importlib.import_module(module_name)

            # Call the selected module's main() function, which internally handles parameter tuning
            module.main()
        except ModuleNotFoundError:
            st.error(f"⚠️ The module `{module_name}` was not found. Ensure it is in the `Visualization` directory.")
        except AttributeError:
            st.error(f"⚠️ The module `{module_name}` does not have a `main()` function. Check the module structure.")
