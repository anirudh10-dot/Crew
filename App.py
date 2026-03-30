
        import streamlit as st
import random
import pandas as pd

# --- 1. THE CLASS DEFINITION (Now with Environmental Sensors) ---
class SpaceStationAI:
    def __init__(self, astronauts, activity_level):
        self.astronauts = astronauts
        self.activity_level = activity_level
        
        # Life Support Base Levels
        self.oxygen = 95.0
        self.water = 500.0
        self.co2 = 0.04
        
        # New Environmental Sensors
        self.temperature = 22.0  # Celsius
        self.humidity = 45.0     # Percentage
        self.pressure = 101.3    # kPa (Standard Earth pressure)
        self.rad_in = 150.0      # mSv (Incoming Radiation)
        self.rad_out = 145.0     # mSv (Shielding/Reflected)

    def update_sensors(self):
        multiplier = 1.5 if self.activity_level == "High" else 1.0
        
        # Resource Depletion
        self.oxygen -= random.uniform(0.01, 0.03) * self.astronauts * multiplier
        self.water -= random.uniform(0.05, 0.2) * self.astronauts
        
        # Environmental Fluctuations
        self.temperature += random.uniform(-0.5, 0.5) * multiplier
        self.humidity += random.uniform(-1, 1) * self.astronauts * 0.1
        self.pressure += random.uniform(-0.01, 0.01)
        
        # Radiation Logic (Varies based on "orbit" simulation)
        self.rad_in = 150.0 + random.uniform(-20, 50)
        self.rad_out = self.rad_in * 0.95 # Assume 95% is shielded/reflected

    def calculate_time_left(self):
        ox_time = self.oxygen * 2.5 
        wat_time = self.water / (self.astronauts * 2)
        return round(ox_time, 1), round(wat_time, 1)

    def check_status(self):
        messages = []
        if self.temperature > 28 or self.temperature < 18:
            messages.append(f"⚠️ TEMP ANOMALY: {self.temperature:.1f}°C")
        if self.pressure < 95:
            messages.append("🚨 CRITICAL: DEPRESSURIZATION DETECTED")
        if (self.rad_in - self.rad_out) > 15:
            messages.append("☢️ HIGH RADIATION EXPOSURE")
        if not messages:
            messages.append("✅ Environmental Systems Nominal")
        return messages

# --- 2. STREAMLIT UI SETUP ---
st.set_page_config(page_title="ISS Life Support Pro", layout="wide")
st.title("🛰️ Advanced ISS Environmental Monitor")

# Sidebar
st.sidebar.header("Station Controls")
astronauts = st.sidebar.slider("Crew Size", 1, 10, 3)
activity = st.sidebar.selectbox("Activity level", ["Low", "Medium", "High"])

# Initialize session state
if "ai" not in st.session_state:
    st.session_state.ai = SpaceStationAI(astronauts, activity)

ai = st.session_state.ai
ai.update_sensors()
status_messages = ai.check_status()

# --- 3. METRIC DASHBOARD ---
# Row 1: Vital Resources
st.subheader("💧 Vital Resources")
c1, c2, c3 = st.columns(3)
c1.metric("Oxygen", f"{ai.oxygen:.2f}%")
c2.metric("CO2", f"{ai.co2:.3f}%")
c3.metric("Water", f"{ai.water:.1f} L")

# Row 2: Environment
st.subheader("🌡️ Cabin Environment")
e1, e2, e3 = st.columns(3)
e1.metric("Temperature", f"{ai.temperature:.1f}°C")
e2.metric("Humidity", f"{ai.humidity:.1f}%")
e3.metric("Pressure", f"{ai.pressure:.2f} kPa")

# Row 3: Radiation Telemetry
st.subheader("☢️ Radiation Flux")
r1, r2, r3 = st.columns(3)
net_rad = ai.rad_in - ai.rad_out
r1.metric("Incoming (Sun/Cosmic)", f"{ai.rad_in:.1f} mSv")
r2.metric("Outgoing (Shielded)", f"{ai.rad_out:.1f} mSv")
r3.metric("Net Absorption", f"{net_rad:.2f} mSv", delta_color="inverse", delta=f"{net_rad:.2f}")

# --- 4. ALERTS & CONTROLS ---
st.divider()
for msg in status_messages:
    if "⚠️" in msg or "🚨" in msg or "☢️" in msg:
        st.error(msg)
    else:
        st.success(msg)

if st.button('Update Station Telemetry'):
    st.rerun()
    
