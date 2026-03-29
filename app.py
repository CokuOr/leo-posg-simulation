import pandas as pd
import numpy as np
import random
from skyfield.api import load

# --- THE ENGINE ---
def get_leo_scan():
    url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
    try:
        all_sats = load.tle_file(url)
        selected = random.sample(all_sats, 10)
    except:
        return "Connection Error. Try again in a moment."

    sector_data = []
    for sat in selected:
        dist = random.uniform(1.0, 50.0)
        # Your POSG Logic
        if "STARLINK" in sat.name:
            b, game = "Station Keeping", "Congestion (C)"
        else:
            b, game = "Agile/Ambiguous", "Escalation (E)"

        sector_data.append({"Object": sat.name, "Dist (km)": round(dist, 2), "Behavior": b, "Sub-Game": game})
    
    return pd.DataFrame(sector_data).sort_values("Dist (km)")

# --- RUN SCAN ---
print("🛰️ LEO SITUATIONAL AWARENESS SCAN")
print("-" * 40)
df = get_leo_scan()
print(df)

# --- THE INTERACTIVE CHOICE ---
print("\n--- STRATEGIC TUPLE <Ai> ---")
intent = input("Choose Posture: [1] Yield (Safety) or [2] Assert (Slot Protection): ")
sigma = input("Choose Signal: [1] Transparent or [2] Masked (Attribution Void): ")

if intent == "2" and sigma == "2":
    print("\n⚠️ RESULT: You have entered the SOVEREIGNTY TRAP. High utility, but Attribution Void triggered.")
else:
    print("\n✅ RESULT: Maneuver logged. System remains in Stable Equilibrium.")
