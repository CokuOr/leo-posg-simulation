import streamlit as st
import random
import pandas as pd

# --- UI & THEME ---
st.set_page_config(page_title="LEO Master: Decision Tree", layout="wide")
st.markdown("""<style>.stRadio>label { font-weight: bold; color: #4CAF50; }</style>""", unsafe_allow_html=True)

# --- INITIALIZE STATE ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'k': 0.15, 'budget': 2500, 'intel': 10, 'turn': 1,
        'history': [], 'alerts': ["🛰️ Orbital Slot 7-Alpha Secured. Awaiting orders."]
    }

gs = st.session_state.game_state

# --- HEADER ---
st.title("🛰️ LEO MASTER: THE SOVEREIGNTY TRAP")
st.write(f"**Turn:** {gs['turn']} | **Budget:** ${gs['budget']} | **Orbital Debris (K):** {gs['k']:.2%}")
st.divider()

# --- STEP 1: FACTION SELECTION (Only on Turn 1) ---
if gs['turn'] == 1:
    faction = st.selectbox("Choose Your Organization", 
        ["Global Constellation Corp", "National Defense Space Command", "Balkan Research Consortium"])
    st.info(f"Welcome, Director of {faction}. Your choices today define the orbit of tomorrow.")

# --- STEP 2: MULTI-LEVEL DECISION TREE ---
st.header("🛠️ Tactical Command")

# CHOICE LEVEL 1: THE MISSION
mission = st.selectbox("Phase 1: Select Mission Objective", 
    ["Expand Network Coverage", "Perform Proximity Inspection (RPO)", "Emergency Collision Avoidance"])

# CHOICE LEVEL 2: THE EXECUTION (Changes based on Phase 1)
st.subheader("Phase 2: Execution Strategy")
if mission == "Expand Network Coverage":
    exec_strategy = st.radio("How will you deploy?", 
        ["Safe Orbit (High Cost, Low Risk)", "Aggressive Stacking (Low Cost, High Debris)"])
elif mission == "Perform Proximity Inspection (RPO)":
    exec_strategy = st.radio("How will you approach the target?", 
        ["Public Observation (Scientific)", "Shadow Maneuver (Intelligence Gathering)"])
else: # Collision Avoidance
    exec_strategy = st.radio("Maneuver Priority?", 
        ["Full Burn (Save Satellite, Export Debris)", "Controlled Drift (Risk Satellite, Save Orbit)"])

# CHOICE LEVEL 3: THE LEGAL SHIELD (The Attribution Void)
st.subheader("Phase 3: Telemetry Protocol")
telemetry = st.radio("Signal Encryption Level", 
    ["Open Broadcast (Auditable)", "Quantum Masking (Ambiguous/Unobservable)"],
    help="Ambiguous signals make it impossible for international courts to prove your 'Fault'.")

# --- EXECUTE TURN ---
if st.button("🚀 INITIATE MANEUVER", type="primary"):
    gs['turn'] += 1
    
    # Logic Calculations
    revenue = 1000 if "Aggressive" in exec_strategy or "Shadow" in exec_strategy else 400
    risk_inc = 0.08 if "Aggressive" in exec_strategy or "Full Burn" in exec_strategy else 0.02
    
    # The "Attribution Void" Logic
    pa = 0.05 if telemetry == "Quantum Masking (Ambiguous/Unobservable)" else 0.90
    
    # Apply results
    gs['budget'] += revenue
    gs['k'] = min(1.0, gs['k'] + risk_inc)
    
    # Narrative Outcome
    outcome = f"Turn {gs['turn']-1}: {mission} via {exec_strategy} complete."
    if telemetry == "Quantum Masking (Ambiguous/Unobservable)":
        outcome += " 🛡️ ATTRIBUTION VOID ACTIVE: You are immune to legal claims."
    else:
        outcome += " ⚖️ AUDITABLE: You are legally vulnerable if a collision occurs."
    
    gs['alerts'].insert(0, outcome)

# --- RESULTS & VISUALS ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 System Health & Trends")
    # Simple growth chart
    chart_data = pd.DataFrame({'Debris Density': [0.15, gs['k']]})
    st.line_chart(chart_data)
    
with col2:
    st.subheader("📜 Comms Log")
    for alert in gs['alerts'][:5]:
        st.write(alert)

# --- THE "HIDDEN CHOICE" (Random Events) ---
if gs['k'] > 0.40:
    st.warning("🚨 **Congestion Alert:** A minor collision has occurred in a neighboring sector!")
    investigate = st.selectbox("Reaction?", ["Ignore (Save Budget)", "Fund Cleanup (-$500)", "Blame Competitor (Requires Intel)"])
    if investigate == "Fund Cleanup (-$500)":
        gs['budget'] -= 500
        gs['k'] -= 0.05
        st.success("You spent funds to stabilize the orbit.")

# --- GAME OVER ---
if gs['k'] >= 0.85:
    st.error("### 💥 KESSLER SYNDROME REACHED. THE ORBIT IS LOST.")
    if st.button("Restart Simulation"):
        st.session_state.clear()
        st.rerun()

# --- THE THEORY (For your thesis) ---
with st.expander("📚 Behind the Scenes: The POSG Math"):
    st.write("""
    This simulation demonstrates **Sequential Decision Making**. 
    
    By choosing **Aggressive Stacking** + **Quantum Masking**, you maximize your $V$ (Value) 
    while driving your $P_a$ (Probability of Attribution) to near zero. 
    
    In a 'Choices over Choices' environment, rational actors will always nest their 
    risky physical moves inside an 'Ambiguous' legal signal to avoid the Liability Convention.
    """)
