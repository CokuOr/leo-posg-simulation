import streamlit as st
import pandas as pd
import numpy as np
import random
from skyfield.api import load

# --- 1. ROBUST DATA ENGINE ---
@st.cache_data(ttl=600)
def get_leo_scan():
    """Fetches real LEO data with a synthetic backup."""
    try:
        # Attempt to pull real-time data
        url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
        all_sats = load.tle_file(url)
        selected = random.sample(all_sats, 15)
        names = [s.name for s in selected]
    except:
        # BACKUP: If CelesTrak is down, use these representative LEO objects
        names = ["STARLINK-5102", "COSMOS-2499 (Agile)", "USA-321 (Classified)", 
                 "ISS (ZARYA)", "ONEWEB-0412", "DEBRIS-RS-2022", "YAOGAN-35"]
        st.sidebar.warning("Using Synthetic Backup (Live API Timeout)")

    sector_data = []
    for name in names:
        dist = random.uniform(2.1, 45.0)
        # Your POSG Research Logic
        if "STARLINK" in name or "ONEWEB" in name:
            obj_type, behavior = "Commercial", "Station Keeping"
        elif "COSMOS" in name or "USA" in name or "YAOGAN" in name:
            obj_type, behavior = "Military/Intel", "Agile/Ambiguous"
        else:
            obj_type, behavior = "Debris/Research", "Passive Drift"

        sector_data.append({
            "Object": name, 
            "Type": obj_type, 
            "Dist (km)": round(dist, 2), 
            "Behavior": behavior
        })
    return pd.DataFrame(sector_data).sort_values("Dist (km)")

# --- 2. THE INTERACTIVE DASHBOARD ---
st.title("🛰️ LEO Situational Awareness (POSG Model)")
df = get_leo_scan()
closest = df.iloc[0]

st.metric("Closest Object", closest['Object'], f"{closest['Dist (km)']} km")
st.dataframe(df, use_container_width=True)

# --- 3. THE STRATEGIC TUPLE ---
st.subheader("🕹️ Strategic Action Vector <Ai>")
intent = st.radio("Maneuver Choice", ["Yield (Safety)", "Assert (Slot Protection)"])
sigma = st.select_slider("Signal Protocol (σ)", options=["Transparent", "Masked"])

if st.button("Execute Maneuver"):
    if intent == "Assert (Slot Protection)" and sigma == "Masked":
        st.error("🚨 ATTRIBUTION VOID: You have entered the 'Sovereignty Trap'. Legal fault cannot be determined.")
    else:
        st.success("✅ STABLE EQUILIBRIUM: Maneuver successfully logged in the POSG history.")
