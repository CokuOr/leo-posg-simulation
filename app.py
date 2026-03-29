import streamlit as st
import numpy as np
import pandas as pd

st.title("🛰️ LEO Master POSG Simulation")
st.write("Welcome to the Orbital Governance Lab.")

# Sidebar for logic
st.sidebar.header("Maneuver Controls")
a_s = st.sidebar.selectbox("Action", ["Evade", "Persist"])
sigma = st.sidebar.selectbox("Signal", ["Transparent", "Ambiguous"])

# Initialize session state for tracking
if 'k' not in st.session_state:
    st.session_state.k = 0.1

# Game logic
if st.button("Execute Step"):
    st.session_state.k += 0.05
    st.write(f"Current Debris Density (K): {st.session_state.k:.2f}")
    if sigma == "Ambiguous":
        st.warning("Attribution Void Active: Liability suppressed.")

st.metric("Orbital Health (K)", f"{st.session_state.k:.2f}")
