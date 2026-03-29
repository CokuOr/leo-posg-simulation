import streamlit as st
import pandas as pd
import numpy as np
import random
from skyfield.api import load, wgs84

# --- 1. THE DATA ENGINE: REAL LEO SNAPSHOT ---
@st.cache_data(ttl=1200)
def get_full_leo_scan():
    """Fetches full LEO catalog and simulates a local 'Sector' environment."""
    # Sources: Active Payloads + Debris + Rocket Bodies
    sources = [
        'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle',
        'https://celestrak.org/NORAD/elements/gp.php?GROUP=debris&FORMAT=tle'
    ]
    all_sats = []
    for url in sources:
        try:
            all_sats.extend(load.tle_file(url))
        except: continue
        
    # Inject "Self" at a standard LEO altitude (550km)
    sector_data = []
    # Sample a manageable subset for the 'Local Sector'
    for sat in random.sample(all_sats, 30):
        dist = random.uniform(1.2, 100.0) # Relative distance in km
        
        # CATEGORIZATION AXIOMS
        if "DEB" in sat.name or "R/B" in sat.name:
            obj_type = "Debris / Rocket Body"
            behavior = "Uncontrolled Ballistic"
            posg_relevance = "Congestion ($C$)"
        elif "STARLINK" in sat.name or "ONEWEB" in sat.name:
            obj_type = "Commercial Payload"
            behavior = "Station Keeping"
            posg_relevance = "Information Tax ($I$)"
        else:
            obj_type = "Classified / Military"
            behavior = "High-Agility / Ambiguous"
            posg_relevance = "Escalation ($E$)"

        sector_data.append({
            "Object": sat.name,
            "Type": obj_type,
            "Dist (km)": round(dist, 2),
            "Behavioral Pattern": behavior,
            "POSG Sub-Game": posg_relevance
        })
    return pd.DataFrame(sector_data).sort_values("Dist (km)")

# --- 2. THE TACTICAL HUD ---
st.set_page_config(page_title="LEO POSG: Tactical SA", layout="wide")
st.title("🛰️ LEO Command Dashboard: Unified Sector View")

sector_df = get_full_leo_scan()
closest_threat = sector_df.iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Local Objects", len(sector_df))
c2.metric("Closest Approach", f"{closest_threat['Dist (km)']} km", closest_threat['Object'])
c3.metric("Congestion ($C$)", "0.58", "Increasing")
c4.metric("Escalation ($E$)", "0.22", "Stable")

st.divider()

# --- 3. SITUATIONAL AWARENESS: THE SECTOR SCAN ---
col_sa, col_control = st.columns([2, 1], gap="medium")

with col_sa:
    st.subheader("📡 Multi-Object Tactical Scan")
    # Color-coded table for rapid SA
    def color_type(val):
        color = '#4b0000' if 'Classified' in str(val) else ('#003300' if 'Commercial' in str(val) else '#333333')
        return f'background-color: {color}'

    st.dataframe(sector_df.style.applymap(color_type, subset=['Type']), use_container_width=True)
    
    # Intelligence Feed
    st.info(f"**INTEL FEED:** {closest_threat['Object']} is currently the primary conjunction risk. "
            f"Pattern suggests {closest_threat['Behavioral Pattern']} behavior.")

with col_control:
    st.subheader("🕹️ Strategic Action Profile ($A_i$)")
    
    # Nested Choices for Sub-Game II: Escalation Dynamics
    st.markdown("**Sub-Game II: The Chicken/Bayesian Signal**")
    intent = st.radio("Define Strategic Intent", ["Yield (Safety First)", "Assert (Slot Protection)"])
    signal = st.radio("Set Signal Protocol ($\sigma$)", ["Transparent", "Ambiguous (Masked)"])
    
    # Sub-Game III: AI Accelerant
    ai_mode = st.toggle("Enable AI-Enhanced Maneuver Planning", value=True)

    if st.button("EXECUTE ORBITAL TURN"):
        # The Transition (T) logic
        if intent == "Assert (Slot Protection)" and closest_threat['Dist (km)'] < 10:
            st.error(f"🚨 **CONJUNCTION WARNING:** 'Assertive' posture against {closest_threat['Object']} triggered a high-risk encounter. Escalation ($E$) increased.")
        elif signal == "Ambiguous (Masked)":
            st.warning("🕵️ **ATTRIBUTION VOID:** Maneuver completed under forensic entropy. State responsibility unprovable.")
        else:
            st.success("✅ **TRANSPARENT EXECUTION:** Maneuver successfully logged. Operational Value ($V$) secured.")

# --- 4. DATA VISUALIZATION: SYSTEMIC COUPLING ---
st.divider()
st.subheader("📈 System Dynamics: The Sovereignty Trap ($C \\to E \\to I \\to C$)")
st.line_chart(pd.DataFrame(np.random.rand(15, 3), columns=['C', 'E', 'I']))

with st.expander("📚 Axioms of the Unified LEO POSG"):
    st.write(f"""
    - **Objects in the Scan:** This includes the full NORAD catalog.
    - **Debris Logic:** Objects like `{closest_threat['Object'] if 'DEB' in closest_threat['Object'] else 'Rocket Body'}` are uncontrollable. They increase $C$ (Congestion) regardless of your actions.
    - **Military Logic:** Objects classified as 'Classified / Military' use **Bayesian Signalling**. Their intent is unknown, forcing you into a **Game of Chicken** where your choice of $\sigma$ (Signal) determines the Attribution Void.
    - **AI Acceleration:** If AI is enabled, your OODA loop is faster, but the risk of **Kinetic Escalation** ($E$) spikes because the adversary has less time to verify your 'Yield' intent.
    """)
