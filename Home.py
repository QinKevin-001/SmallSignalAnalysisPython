import streamlit as st
import importlib
import sys
import os
from datetime import datetime

st.set_page_config(layout="wide")

# Enhanced CSS with mobile gap fixes
st.markdown("""
<style>
    /* Enhanced button styling */
    .stButton button {
        border: 4px solid rgba(49, 51, 63, 0.2) !important;
        border-radius: 6px !important;
    }

    /* Mobile-specific styling */
    @media (max-width: 640px) {
        .stButton button {
            width: 100%;
            margin: 0 !important;  /* Remove vertical margins */
            padding: 0.5rem !important;  /* Consistent padding */
            height: auto;
            min-height: 45px;
            white-space: normal;
            word-wrap: break-word;
        }

        /* Remove extra spacing between rows */
        .row-widget.stButton {
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Ensure consistent spacing between all rows */
        div[data-testid="column"] {
            padding: 0.1rem !important;
            margin: 0 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Rest of your code remains the same...