import streamlit as st
import random
import pandas as pd

# --- GAME ENGINE SETUP ---
st.set_page_config(page_title="LEO Master: Real-State Sim", layout="wide")

if 'gs' not in st.session_state:
    st.session_state.gs = {
        'turn': 1, 'budget': 5000, 'debris_k': 0.28, 
        'intel': 0, 'history': [], 'incidents': 0
    }

gs = st.session_state.gs

# --- SATELLITE REGISTRY (Based on 2026 Data) ---
# Hypothetical but grounded in current LEO trends
targets = {
    "Starlink-G4-92": {"type": "Commercial", "value": 200, "risk": 0.01, "desc": "High-speed broadband node."},
    "USA-321 (Top Secret)": {"type": "Military", "value": 800, "risk": 0.15, "desc": "Electronic Intelligence (SIGINT) platform. High escalation risk."},
    "Kosmos-2558": {"type": "Military", "value": 900, "risk": 0.18, "desc": "Inspector satellite. Likely equipped with kinetic interceptors."},
    "Sentinel-6": {"type": "Civil/Science", "value": 100, "risk": 0.05, "desc": "Ocean topography mission. Low strategic value."},
    "Yaogan-35": {"type": "Military", "value": 750, "risk": 0.12, "desc": "Remote sensing for maritime surveillance."}
}

# --- HEADER ---
st.title("🛰️ LEO MASTER: REAL-STATE OPERATOR")
cols = st.columns(3)
cols[0].metric("Operational Budget", f"${gs['budget']}")
cols[1].metric("LEO Congestion (K)", f"{gs['debris_k']:.2%}")
cols[2].metric("Strategic Intel", gs['intel'])
st.divider()

# --- THE GAME LOOP: TARGET ACQUISITION ---
st.header(f"📍 Turn {gs['turn']}: Select Orbital Target")

target_id = st.selectbox("Identify Satellite in Sector", list(targets.keys()))
target_info = targets[target_id]

# UI Visual Feedback for Military Assets
if target_info['type'] == "Military":
    st.error(f"⚠️ **CLASSIFIED ASSET DETECTED:** {target_info['desc']}")
else:
    st.info(f"ℹ️ **UNCLASSIFIED ASSET:** {target_info['desc']}")

# --- NESTED CHOICES ---
col_choice, col_shield = st.columns(2)

with col_choice:
    st.subheader("Level 1: Choose Action")
    action = st.radio("Maneuver Vector", 
        ["Passive Tracking (Safe)", "Close Proximity Inspection (Risky)", "Signal Jamming (Hostile)"])

with col_shield:
    st.subheader("Level 2: Signal Protocol")
    telemetry = st.radio("Encryption", 
        ["Open Source (Auditable)", "Stealth Burst (Ambiguous)"],
        help="Stealth Burst creates an Attribution Void, preventing military retaliation.")

# --- EXECUTION ---
if st.button("🚀 INITIATE MANEUVER", type="primary"):
    gs['turn'] += 1
    
    # 1. Calculate Results
    # Military targets give more Intel but cost more Risk
    intel_gain = (target_info['value'] // 100) if action != "Passive Tracking (Safe)" else 1
    if action == "Signal Jamming (Hostile)": intel_gain *= 2
    
    risk_factor = target_info['risk']
    if action == "Close Proximity Inspection (Risky)": risk_factor *= 2
    if action == "Signal Jamming (Hostile)": risk_factor *= 4
    
    # 2. The Attribution Void Math
    is_stealth = (telemetry == "Stealth Burst (Ambiguous)")
    detection_prob = 0.05 if is_stealth else 0.80
    
    # 3. Apply Updates
    gs['intel'] += intel_gain
