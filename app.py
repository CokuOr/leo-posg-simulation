import streamlit as st
import pandas as pd
import numpy as np
import random

# --- 1. SYSTEM CONFIG ---
st.set_page_config(page_title="LEO POSG: Escalation Dynamics", layout="wide")
st.markdown("""<style>.main { background-color: #0d1117; color: #c9d1d9; }</style>""", unsafe_allow_html=True)

# --- 2. GAME STATE ---
if 'posg' not in st.session_state:
    st.session_state.posg = {
        'C': 0.25, 'E': 0.15, 'I': 0.10, 'history': [], 'turn': 1
    }
p = st.session_state.posg

# --- 3. THE HUD ---
st.title("🛰️ Sub-Game II: Escalation Dynamics")
st.write("Modeling the 'Game of Chicken' with Bayesian Signalling under AI Acceleration.")

m1, m2, m3 = st.columns(3)
m1.metric("Congestion ($C$)", f"{p['C']:.2f}")
m2.metric("Escalation Risk ($E$)", f"{p['E']:.2f}")
m3.metric("Information Tax ($I$)", f"{p['I']:.2f}")
st.divider()

# --- 4. THE DECISION MATRIX ---
col_strat, col_logic = st.columns([1, 2], gap="large")

with col_strat:
    st.subheader("📡 Bayesian Signalling Profile")
    
    # 1. Type Selection (The Player's Secret 'State')
    my_type = st.radio("Your Strategic Type ($\Theta$)", 
                       ["Cooperative (Yield-prone)", "Assertive (Chicken-prone)"])
    
    # 2. Signaling Choice (The Observable Action)
    signal_fidelity = st.select_slider("Signal Fidelity ($\sigma$)", 
                                       options=["Transparent", "Ambiguous", "Deceptive"])
    
    # 3. AI OODA Loop (The Accelerant)
    ai_enabled = st.toggle("Enable AI-Enhanced Decision Support", value=True)
    
    execute = st.button("EXECUTE MANEUVER (T+1)", type="primary")

# --- 5. THE ESCALATION ENGINE ---
if execute:
    # Bayesian Logic: Adversary updates beliefs based on sigma
    adversary_belief = 0.8 if signal_fidelity == "Transparent" else 0.2
    
    # Game of Chicken Outcome Logic
    # If both 'Assertive' (Hidden or Real) -> Escalation Spikes
    escalation_spike = 0.0
    if my_type == "Assertive (Chicken-prone)":
        if signal_fidelity != "Transparent":
            escalation_spike = 0.25  # High risk of "Collision of Wills"
        else:
            escalation_spike = 0.10  # Known deterrence
    else:
        escalation_spike = 0.02 # Defensive yield
        
    # AI Acceleration Factor
    if ai_enabled:
        escalation_spike *= 1.5  # Compressed OODA loops reduce reaction time
        
    # Update Coupled Variables
    p['E'] = min(1.0, p['E'] + escalation_spike)
    p['I'] = min(1.0, p['E'] * 0.6) # Info tax scales with uncertainty and risk
    p['C'] += 0.03 # Natural growth
    
    p['history'].append({
        "Turn": p['turn'], "E": p['E'], "I": p['I'], "Belief": adversary_belief
    })
    p['turn'] += 1

# --- 6. VISUALIZING THE EVOLUTION ---
with col_logic:
    st.subheader("📉 Bayesian Update & Escalation Trend")
    if p['history']:
        df = pd.DataFrame(p['history'])
        st.line_chart(df.set_index("Turn")[["E", "I"]])
        
        # Scenario Feedback
        if p['E'] > 0.6:
            st.error("🚨 ESCALATION CRITICAL: Maneuver interpreted as 'Hostile Intent'. Tactical warning thresholds breached.")
        elif signal_fidelity == "Ambiguous":
            st.warning("🕵️ ATTRIBUTION VOID: Adversary cannot distinguish between 'Mechanical Failure' and 'Strategic Defection'.")
        else:
            st.success("✅ STABLE: Signal fidelity maintains the 'Deterrence Equilibrium'.")
    else:
        st.info("Select your strategic profile and execute the first maneuver.")

# --- 7. THEORETICAL SUMMARY ---
st.divider()
with st.expander("📚 Theoretical Framework: Chicken + Bayesian Signalling"):
    st.write("""
    **The Game of Chicken:** In LEO, two actors approaching a 'Conjunction' are in a Game of Chicken. 
    The one who 'Yields' (maneuvers) loses operational value ($V$). 
    
    **Bayesian Signalling:** Because you can't see the adversary's 'Type' ($\Theta$), you rely on signals ($\sigma$). 
    * **Transparent signals** reduce $I$ (Info Tax) but make you predictable.
    * **Ambiguous signals** create an **Attribution Void**, which hides your defection but causes $E$ (Escalation) to spiral as the adversary assumes the worst-case 'Type'.
    
    **AI Acceleration:** AI compresses the decision window. When OODA loops are faster than human diplomacy, 
    the probability of a 'Chicken' collision increases, driving the system toward a **Pareto-inefficient equilibrium**.
    """)

if p['E'] >= 0.90:
    st.error("### 💥 KINETIC EXCHANGE: Escalation has reached terminal levels. Orbital access lost.")
    if st.button("Reset Simulation"): st.session_state.clear(); st.rerun()
