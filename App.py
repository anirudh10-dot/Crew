import streamlit as st
import random
import time

# --- 1. THE CLASS DEFINITION (State-Persistent) ---
class SpaceStationAI:
    def __init__(self, astronauts, activity_level):
        self.astronauts = astronauts
        self.activity_level = activity_level
        
        # Vital Stats (Starting at Nominal ISS levels)
        self.oxygen = 21.0       # Percentage (Earth-like)
        self.co2 = 0.03          # Percentage
        self.water = 500.0       # Liters
        self.temperature = 22.0  # Celsius
        self.humidity = 40.0     # Percentage
        self.pressure = 101.3    # kPa
        
        # Radiation
        self.rad_in = 12.0       # μSv/hr (Hourly rate is more realistic for telemetry)
        self.shielding_eff = 0.94 # 94% efficiency

    def update_sensors(self):
        # Multipliers based on activity
        act_mult = {"Low": 1.0, "Medium": 1.5, "High": 2.2}[self.activity_level]
        
        # 1. Oxygen Depletion & CO2 Rise
        # Humans consume ~0.84kg of O2 per day. In a small volume, % drops slowly.
        o2_drop = (0.005 * self.astronauts * act_mult)
        self.oxygen -= o2_drop
        self.co2 += o2_drop * 0.85  # Respiratory Quotient
        
        # 2. Water Usage & Recovery
        # Simulation of drinking vs. the Water Recovery System (WRS)
        water_used = (0.1 * self.astronauts * act_mult)
        water_recovered = water_used * 0.93 # ISS recovers ~93% of water
        self.water -= (water_used - water_recovered)
        
        # 3. Environment (Heat and Humidity)
        # Body heat and sweat increase temp/humidity
        self.temperature += (0.02 * self.astronauts * act_mult) - 0.05 # Cooling system fights back
        self.humidity += (0.1 * self.astronauts * act_mult) - 0.15    # Dehumidifier fights back
        
        # 4. Pressure (Minor cabin leak simulation)
        self.pressure -= 0.002 
        
        # 5. Radiation (Variable based on solar activity)
        self.rad_in = 12.0 + random.uniform(-2.0, 8.0)
        
    def check_status(self):
        alerts = []
        if self.oxygen < 19.5: alerts.append("🚨 LOW OXYGEN: Check Electrolysis System")
        if self.co2 > 0.5: alerts.append("⚠️ HIGH CO2: Check Scrubbers")
        if self.temperature > 27: alerts.append("🌡️ THERMAL OVERLOAD: Check Cooling Loops")
        if self.pressure < 98.0: alerts.append("🚨 DEPRESSURIZATION DETECTED")
        return alerts

# --- 2. STREAMLIT UI SETUP ---
st.set_page_config(page_title="ISS Mission Control", layout="wide")
st.title("🛰️ ISS Life Support Telemetry")

# Initialize Session State (This keeps the numbers moving instead of resetting)
if "station" not in st.session_state:
    st.session_state.station = SpaceStationAI(3, "Medium")
    st.session_state.history = {"o2": 21.0, "temp": 22.0, "press": 101.3}

ss = st.session_state.station

# Sidebar Controls
st.sidebar.header("Command Center")
ss.astronauts = st.sidebar.slider("Crew Count", 1, 7, ss.astronauts)
ss.activity_level = st.sidebar.selectbox("Current Activity", ["Low", "Medium", "High"], index=1)

# Logic: Store old values for deltas, then update
old_o2 = ss.oxygen
old_temp = ss.temperature
old_press = ss.pressure

if st.button('🔄 Sync Telemetry (Step 1 min)'):
    ss.update_sensors()

# --- 3. DASHBOARD RENDERING ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Atmospheric Composition")
    st.metric("Oxygen", f"{ss.oxygen:.3f}%", f"{ss.oxygen - old_o2:.4f}%", delta_color="normal")
    st.metric("CO2", f"{ss.co2:.3f}%", f"{ss.co2 - (old_o2*0.85):.4f}%", delta_color="inverse")

with col2:
    st.subheader("Cabin Climate")
    st.metric("Temperature", f"{ss.temperature:.2f}°C", f"{ss.temperature - old_temp:.2f}°C")
    st.metric("Pressure", f"{ss.pressure:.3f} kPa", f"{ss.pressure - old_press:.3f} kPa", delta_color="normal")

with col3:
    st.subheader("Resources & Radiation")
    st.metric("Water Reservoir", f"{ss.water:.2f} L")
    net_rad = ss.rad_in * (1 - ss.shielding_eff)
    st.metric("Net Radiation", f"{net_rad:.3f} μSv/h")

# --- 4. ALERTS ---
st.divider()
status_alerts = ss.check_status()
if not status_alerts:
    st.success("✅ All systems nominal. Environmental Control and Life Support System (ECLSS) stable.")
else:
    for alert in status_alerts:
        st.error(alert)

# Reset Button
if st.sidebar.button("Reset Simulation"):
    st.session_state.clear()
    st.rerun()

        
