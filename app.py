import streamlit as st
import numpy as np
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="LEO Master POSG", layout="centered")

# --- UI HEADER ---
st.title("🛰️ The LEO Game: Strategic Defection Simulator")
st.markdown("### Interactive Structural Misalignment Model")
st.divider()

# --- INITIALIZE STATE ---
if 'debris_k' not in st.session_state:
    st.session_state.debris_k = 0.18
    st.session_state.logs = []
    st.session_state.game_over = False

# --- PLAYERS & SCENARIOS (Hypothetical Data) ---
st.sidebar.header("🕹️ Decision Matrix")

# A. SELECT YOUR PLAYER (Who you are)
st.sidebar.subheader("1. Select Your Player Type")
player_type = st.sidebar.selectbox("Player Type", 
    ["Legacy Commsat (Large, Stable)", 
     "Mega-Constellation (AI-Optimized)", 
     "Military SSA (Small, Fast)"])

# B. SELECT THE SCENARIO (What is happening)
st.sidebar.subheader("2. Select Your Scenario")
scenario = st.sidebar.selectbox("Scenario", 
    ["Routine Station-Keeping", 
     "Conjunction Alert (5% Probability)", 
     "Proximity Operation (Adversary Probe)",
     "Debris Cloud Navigation (High Risk)"])

# C. SELECT YOUR ACTIONS (The POSG variables)
st.sidebar.subheader("3. Select Your Action Vector (a)")
a_s = st.sidebar.radio("Strategic Action (a_s)", ["Evade (Cooperate)", "Persist (Defect)"], help="Evading costs profit; persisting takes the slot.")
sigma = st.sidebar.radio("Signal Transparency (σ)", ["Public & Clear", "Ambiguous/Hidden"], help="Hidden signals block 'Fault' assignment but raise escalation risk.")

# --- CORE LOGIC: POSG ENGINE ---
def run_simulation():
    # 1. Operational Value (V)
    # Persisting gives higher profit (1.5) but evading only 0.5.
    base_v = 1.5 if a_s == "Persist (Defect)" else 0.5
    
    # 2. Probability of Attribution (Pa) - THE attribution void
    # Pa is LOW if signal is Ambiguous, suppressing liability.
    Pa = 0.10 if sigma == "Ambiguous/Hidden" else 0.80
    
    # 3. Information Tax (I)
    # Legacy players pay more for compliance.
    I = 0.4 if player_type == "Legacy Commsat (Large, Stable)" else 0.1
    
    # 4. Payoff Calculation: R_i = V - K - (Pa * Liability) - I
    current_payoff = base_v - st.session_state.debris_k - (Pa * 1.0) - I
    
    # 5. Transition: Debris growth based on risk
    # Scenario and Action together determine debris growth.
    base_growth = {"Routine Station-Keeping": 0.02,
                   "Conjunction Alert (5% Probability)": 0.08,
                   "Proximity Operation (Adversary Probe)": 0.12,
                   "Debris Cloud Navigation (High Risk)": 0.20}[scenario]
    
    risk_multiplier = 2.0 if a_s == "Persist (Defect)" else 1.0
    actual_growth = base_growth * risk_multiplier
    
    # Update State
    st.session_state.debris_k = min(1.0, st.session_state.debris_k + actual_growth)
    
    # Narrative Builder
    attribution_void_active = True if sigma == "Ambiguous/Hidden" else False
    void_status = "⚠️ ATTRIBUTION VOID: Liability suppressed." if attribution_void_active else "✅ AUDITABLE: Liability enforceable."
    
    st.session_state.logs.insert(0, f"**Step {len(st.session_state.logs)+1}**:")
    st.session_state.logs.insert(0, f"Player: {player_type} | Scenario: {scenario} | Action: {a_s}")
    st.session_state.logs.insert(0, f"Result: Profit=${current_payoff:.2f} | Debris K={st.session_state.debris_k:.2f} | {void_status}")
    st.session_state.logs.insert(0, st.session_state.debris_k) # For chart

# --- EXECUTION BUTTON ---
if st.sidebar.button("Execute Step"):
    if not st.session_state.game_over:
        run_simulation()

# --- MAIN DASHBOARD ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 System Evolution")
    if st.session_state.logs:
        # Get debris history from logs
        debris_history = [log for log in st.session_state.logs if isinstance(log, float)]
        st.line_chart(pd.DataFrame(debris_history, columns=["Debris K"]))
    else:
        st.info("Awaiting first maneuver...")

with c2:
    st.subheader("⚠️ Legal/Physical Risk")
    st.metric("Debris Density (K)", f"{st.session_state.debris_k:.2f}")
    
    if st.session_state.debris_k >= 0.8:
        st.session_state.game_over = True
        st.error("🚨 KESSLER THRESHOLD REACHED: Orbital domain collapse. GAME OVER.")
        if st.button("Reset Simulation"):
            st.session_state.clear()
            st.rerun()

# --- MISSION LOGS & LEGAL ANALYSIS ---
st.divider()
st.subheader("📜 Adjudication Record (The 'Sovereignty Trap')")
with st.expander("Show the Adjudication Logic"):
    st.write("""
    **If you choose [Persist] + [Ambiguous]:**
    * **The Operational Value (V):** Is maximized ($1.5). You took the slot.
    * **The Legal Barrier (Pa):** Probability of Attribution (Pa) drops to 10%. 
    * **Result:** No State can assign Fault ($f_i$) under the Liability Convention. You win the slot and neutralize the law. This is the **'Non-Cooperative Equilibrium'.**
    
    **If you choose [Evade] + [Clear]:**
    * **The Operational Value (V):** Is low ($0.5). You yielded.
    * **The Legal Trap:** Since you are transparent, if a stochastic event (e.g., solar flare) causes a collision anyway, *you* are easily identified and held liable. You are 'The Sucker'.
    """)

# Display logs (skipping the debris floats)
for log in [l for l in st.session_state.logs if isinstance(l, str)][:9]:
    st.text(log) 
