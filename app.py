import streamlit as st
import random
import pandas as pd

# --- UI CONFIGURATION ---
st.set_page_config(page_title="LEO Command: The POSG Game", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stMetric { background-color: #0e1117; border: 1px solid #2e7d32; padding: 10px; border-radius: 10px; }
    .stAlert { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE GAME STATE ---
if 'debris' not in st.session_state:
    st.session_state.update({
        'debris': 0.15, 'money': 2000, 'steps': 0, 'history': [],
        'logs': ["🛰️ System Online. Welcome, Commander."],
        'legal_heat': 0, 'tech_level': 1
    })

# --- HEADER ---
st.title("🌌 LEO COMMAND: THE SOVEREIGNTY TRAP")
st.markdown("### *Can you dominate the orbit before the Kessler Syndrome locks you out?*")
st.divider()

# --- SIDEBAR: COMMAND CENTER ---
with st.sidebar:
    st.header("🎮 Player Profile")
    role = st.selectbox("Choose Your Faction", 
        ["Venture Starlink (Fast/Risky)", "State Aegis (Heavy/Defensive)", "Balkan Space Agency (Scrappy/Efficient)"])
    
    st.subheader("🛠️ Tech Upgrades")
    if st.button("Upgrade AI Sensors ($800)"):
        if st.session_state.money >= 800:
            st.session_state.tech_level += 1
            st.session_state.money -= 800
            st.success("Sensors Upgraded! Attribution risk reduced.")
    
    st.divider()
    st.subheader("🕹️ Tactical Action")
    action = st.radio("Maneuver Style", ["Quiet & Cooperative", "Aggressive Persistence", "Shadow Maneuver"])
    signal = st.radio("Signal Protocol", ["Full Transparency", "Encoded/Ambiguous"])
    
    execute = st.button("🚀 EXECUTE ORBITAL TURN", type="primary")

# --- THE GAME ENGINE ---
if execute:
    st.session_state.steps += 1
    
    # 1. Base Logic
    profit = 1200 if action == "Aggressive Persistence" else 400
    if action == "Shadow Maneuver": profit = 800
    
    # 2. Random Event Generator (The "Fun" Part)
    events = [
        {"name": "Solar Flare", "impact": 0.05, "msg": "☀️ Solar Flare! Sensors are noisy. Attribution Void widened."},
        {"name": "Micrometeoroid", "impact": 0.08, "msg": "☄️ Micrometeoroid strike! Debris cloud expanding."},
        {"name": "Cyber Interference", "impact": 0.02, "msg": "👾 Cyber attack! Signal protocols corrupted."},
        {"name": "None", "impact": 0.0, "msg": "🌌 Space is quiet... for now."}
    ]
    event = random.choice(events)
    
    # 3. Payoff & Risk Math
    pa = 0.05 if signal == "Encoded/Ambiguous" else 0.85
    risk_factor = 2.5 if action == "Aggressive Persistence" else 1.0
    
    # 4. Updates
    st.session_state.money += profit
    st.session_state.debris = min(1.0, st.session_state.debris + (event['impact'] * risk_multiplier if 'risk_multiplier' in locals() else 0.05 * risk_factor))
    
    # 5. Legal Heat Mechanic
    if pa > 0.5 and action == "Aggressive Persistence":
        st.session_state.legal_heat += 20
        penalty_msg = "⚖️ International lawyers are watching! Legal Heat +20."
    else:
        st.session_state.legal_heat = max(0, st.session_state.legal_heat - 5)
        penalty_msg = "🕵️ You stayed under the radar."

    st.session_state.logs.insert(0, f"**Turn {st.session_state.steps}**: {event['msg']} {penalty_msg}")

# --- VISUAL DASHBOARD ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Orbital Debris (K)", f"{st.session_state.debris:.1%}")
c2.metric("Treasury ($)", f"{st.session_state.money}")
c3.metric("Legal Heat", f"{st.session_state.legal_heat}%")
c4.metric("Tech Level", f"Lv.{st.session_state.tech_level}")

# --- INTERACTIVE VISUALS ---
st.divider()
st.subheader("📊 Strategic Analysis")
col_chart, col_logs = st.columns([2, 1])

with col_chart:
    if st.session_state.steps > 0:
        chart_data = pd.DataFrame({'Debris': [0.15] + [random.random()*0.1 for _ in range(st.session_state.steps)]}) # Placeholder for real plot
        st.area_chart(chart_data)
    else:
        st.info("Launch a maneuver to see the orbital trend.")

with col_logs:
    st.subheader("📜 Comms Log")
    for log in st.session_state.logs[:5]:
        st.write(log)

# --- THE "SCENARIO" POP-UPS ---
if st.session_state.legal_heat >= 60:
    st.warning("⚠️ **TRIBUNAL ALERT:** A formal claim has been filed against you! Use 'Encoded Signals' to hide intent or pay a $1000 settlement.")
    if st.button("Pay Settlement"):
        st.session_state.money -= 1000
        st.session_state.legal_heat = 0

if st.session_state.debris >= 0.85:
    st.error("💥 **KESSLER COLLAPSE:** The debris has reached critical mass. LEO is closed. Game Over.")
    if st.button("Restart Mission"):
        st.session_state.clear()
        st.rerun()

# --- WHY THIS HAPPENED (The Thesis Bit) ---
with st.expander("📚 Why did I win/lose? (The POSG Theory)"):
    st.write("""
    In this game, **Ambiguous Signals** are your 'Shield'. By making your intent unobservable, 
    you exploit the **Attribution Void**. Even if you cause a collision (High K), 
    the legal system cannot prove 'Fault' because they can't distinguish your maneuver from 
    environmental noise (the Solar Flare event). 
    
    This is the **Sovereignty Trap**: Rational players choose the 'Shadow Maneuver' to get rich, 
    leaving the world to deal with the debris.
    """)
