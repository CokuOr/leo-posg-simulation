import streamlit as st
import random
import pandas as pd

# --- 1. UX: PAGE CONFIG & DARK THEME ---
st.set_page_config(page_title="LEO MASTER: COMMAND", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a "Cyber/Military" Look
st.markdown("""
    <style>
    .main { background-color: #0b0d14; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; }
    div[data-testid="stExpander"] { border: 1px solid #30363d; background-color: #0d1117; }
    .stButton>button { width: 100%; background-color: #238636; color: white; border: none; font-weight: bold; height: 3em; }
    .stButton>button:hover { background-color: #2ea043; border: 1px solid white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GAME STATE ---
if 'gs' not in st.session_state:
    st.session_state.gs = {
        'turn': 1, 'budget': 5000, 'debris': 0.32, 'intel': 0, 
        'history': [], 'last_outcome': "Systems Ready. Awaiting Input."
    }
gs = st.session_state.gs

# --- 3. UI: TOP NAVIGATION (The "HUD") ---
st.title("🛰️ LEO COMMAND | Tactical Interface")
h1, h2, h3, h4 = st.columns(4)
h1.metric("Orbital Density (K)", f"{gs['debris']:.2%}", delta="CRITICAL" if gs['debris'] > 0.7 else None)
h2.metric("Treasury", f"${gs['budget']:,}")
h3.metric("Intel Level", f"{gs['intel']} XP")
h4.metric("Cycle", f"T-{gs['turn']}")
st.divider()

# --- 4. UX: THE NESTED CHOICE FLOW ---
# We use two main columns: THE ACTION and THE FEEDBACK
col_action, col_visual = st.columns([3, 2], gap="large")

with col_action:
    st.subheader("🛠️ Deployment Sequence")
    
    # LEVEL 1: OBJECTIVE
    mission = st.selectbox("SEQUENCE 01: Select Strategic Objective", 
        ["Commercial Constellation Expansion", "Classified Military Reconnaissance", "Science & Climate Monitoring"])
    
    # LEVEL 2: EXECUTION (Changes based on Level 1)
    st.write("")
    if mission == "Commercial Constellation Expansion":
        st.info("Commercial targets focus on revenue. High volume, low precision.")
        strategy = st.radio("SEQUENCE 02: Launch Profile", ["Vanguard (High Density/Low Cost)", "Sustainable (Low Density/High Cost)"])
    elif mission == "Classified Military Reconnaissance":
        st.error("WARNING: Interacting with Military assets triggers high Legal Heat.")
        strategy = st.radio("SEQUENCE 02: Approach Vector", ["Distant Tracking", "Aggressive RPO (Proximity)"])
    else:
        st.success("Scientific missions reduce global Debris but generate no Profit.")
        strategy = st.radio("SEQUENCE 02: Mission Goal", ["Atmospheric Scan", "Active Debris Cleanup"])

    # LEVEL 3: SIGNAL PROTOCOL (The POSG Attribution Void)
    st.write("")
    telemetry = st.select_slider("SEQUENCE 03: Telemetry Protocol", 
        options=["Open (Auditable)", "Encrypted", "Quantum Shadow (Ambiguous)"],
        help="Ambiguous signals mask your 'Fault' from International Courts.")

    # THE TRIGGER
    if st.button("INITIATE MANEUVER"):
        # Logic - Simplified for brevity
        gs['turn'] += 1
        profit = 1200 if "Vanguard" in strategy or "Aggressive" in strategy else 300
        cost = 800 if "Sustainable" in strategy or "Cleanup" in strategy else 100
        
        # Attribution Void Math
        pa = 0.05 if telemetry == "Quantum Shadow (Ambiguous)" else 0.90
        risk = 0.10 if "Aggressive" in strategy or "Vanguard" in strategy else 0.02
        if "Cleanup" in strategy: risk = -0.05
        
        # Update Stats
        gs['budget'] += (profit - cost)
        gs['debris'] = max(0.05, min(1.0, gs['debris'] + risk))
        
        # Result Narrative
        if pa < 0.1 and risk > 0.05:
            gs['last_outcome'] = "👤 GHOST MOVE: Collision risk detected, but the Attribution Void prevented identification. No fines issued."
        elif pa > 0.5 and risk > 0.05:
            fine = 1500
            gs['budget'] -= fine
            gs['last_outcome'] = f"⚖️ LEGAL BREACH: Your transparent signal allowed a court to assign Fault. Fine: ${fine}."
        else:
            gs['last_outcome'] = "✅ MISSION SUCCESS: Maneuver completed within legal parameters."
        
        gs['history'].insert(0, f"T-{gs['turn']-1}: {gs['last_outcome']}")

with col_visual:
    st.subheader("📡 Real-Time Situational Awareness")
    
    # UX: STATUS MESSAGE BOX
    st.code(gs['last_outcome'], language="markdown")
    
    # UX: THE "REAL-WORLD" CHART
    chart_data = pd.DataFrame([random.uniform(gs['debris']-0.05, gs['debris']+0.05) for _ in range(20)], columns=["Traffic Density"])
    st.area_chart(chart_data, use_container_width=True)
    
    # UX: RECENT HISTORY LOG
    with st.expander("Mission Logs", expanded=True):
        for log in gs['history'][:5]:
            st.caption(log)

# --- 5. THEORY: THE "SOVEREIGNTY TRAP" ---
st.divider()
with st.expander("📚 THEORY OVERVIEW: Why this UI reflects your Thesis"):
    st.write("""
    The UI is designed to force **Choice-Over-Choice**. 
    
    1. **Asymmetric Information:** The 'Quantum Shadow' protocol represents the **Attribution Void**. You chose to hide your 'Fault' ($f$), which is the only way to play aggressively around Military assets.
    2. **Stochastic Transition:** The 'Traffic Density' chart shows how the orbit ($K$) evolves based on your private moves.
    3. **The Trap:** Notice that your Budget grows fastest when you use 'Shadow' protocols. The game (and LEO) rewards defection over cooperation.
    """)

# --- 6. GAME OVER ---
if gs['debris'] >= 0.90:
    st.error("### 💥 KESSLER SYNDROME INITIATED. LEO IS CLOSED.")
    if st.button("RESET SYSTEM"): st.session_state.clear(); st.rerun()
