import streamlit as st

def apply_custom_css():
    st.markdown(
        """
        <style>
        .css-1d391kg {
            padding: 0.25rem;
        }
        .css-1q3ss1k {
            min-width: 200px;  # Adjust the sidebar width here
            width: 10%;        # Adjust the percentage of the screen width
        }
        </style>
        """, unsafe_allow_html=True
    )