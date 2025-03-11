import streamlit as st
import importlib
import sys
import os  # Needed to check if images exist

# Set page layout (must be the first Streamlit command)
st.set_page_config(layout="wide")

# Define available visualization pages (Now referencing the `Visualization` folder)
PAGES = {
    "Main Page": None,
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
        "Droop Plant Droop Plant": "Two droop plant-controlled inverters interacting.",
        "Droop VSM": "A system integrating a droop-controlled inverter with a Virtual Synchronous Machine (VSM) inverter, examining their dynamic responses.",
    "Droop Plant VSM Plant": "An investigation into the interaction between a plant-level droop-controlled inverter and a plant-level VSM inverter.",
    "VSM VSM": "A configuration with two Virtual Synchronous Machine (VSM) inverters connected together, analyzing their control interactions.",
    "VSM Plant VSM Plant": "A system featuring two VSM inverters with plant-level control, focusing on their coordinated dynamics.",
    "Droop SG": "A droop-controlled inverter operating in tandem with a synchronous generator (SG), exploring hybrid control dynamics.",
    "Droop Plant SG": "A plant-level droop-controlled inverter interacting with a synchronous generator, highlighting integration challenges.",
    "VSM SG": "A Virtual Synchronous Machine (VSM) inverter working alongside a synchronous generator, studying complementary control strategies.",
    "VSM Plant SG": "A plant-level VSM-controlled inverter interacting with a synchronous generator, emphasizing system-level performance and integration."
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
