import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px

# --- 1. THE MISSING CLASS DEFINITION (The "Blueprint") ---
class SpaceStationAI:
    def __init__(self, astronauts, activity_level):
        self.astronauts = astronauts
        self.activity_level = activity_level
        self.oxygen = 95.0
        self.co2 = 0.04
        self.water = 500.0

    def update_sensors(self):
        # Logic to simulate sensor changes based on activity
        multiplier = 1.5 if self.activity_level == "High" else 1.0
        self.oxygen -= random.uniform(0.01, 0.05) * self.astronauts * multiplier
        self.co2 += random.uniform(0.001, 0.005) * self.astronauts
        self.water -= random.uniform(0.1, 0.5) * self.astronauts
        
        # Keep values within realistic bounds
        self.oxygen = max(0, min(100, self.oxygen))
        self.co2 = max(0.03, self.co2)
        self.water = max(0, self.water)

    def calculate_time_left(self):
        # Rough calculation of hours remaining
        ox_time = self.oxygen * 2.5 
        wat_time = self.water / (self.astronauts * 2)
        return round(ox_time, 1), round(wat_time, 1)

    def check_status(self, ox_time, wat_time):
        messages = []
        if self.oxygen < 85:
            messages.append("⚠️ LOW OXYGEN ALERT")
        if self.co2 > 0.5:
            messages.append("⚠️ HIGH CO2 CONCENTRATION")
        if not messages:
            messages.append("✅ All Systems Nominal")
        return messages

# --- 2. STREAMLIT UI SETUP ---
st.set_page_config(page_title="ISS Life Support Dashboard", layout="wide")

st.title("🚀 ISS Life Support Dashboard")
st.write("Real-time monitoring of Space Station Environment")

# Sidebar for Inputs
st.sidebar.header("Mission Parameters")
astronauts = st.sidebar.slider("Number of Astronauts", 1, 10, 3)
activity = st.sidebar.selectbox("Current Activity Level", ["Low", "Medium", "High"])

# --- 3. INITIALIZING THE CLASS (Line 19 Fix) ---
# This checks if the 'ai' object exists; if not, it creates it using our class above
if "ai" not in st.session_state:
    st.session_state.ai = SpaceStationAI(astronauts, activity)

ai = st.session_state.ai

# --- 4. DASHBOARD LOGIC ---
# Update data
ai.update_sensors()
ox_time, wat_time = ai.calculate_time_left()
status_messages = ai.check_status(ox_time, wat_time)

# Display Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Oxygen Level", f"{ai.oxygen:.2f}%", "-0.02%")
col2.metric("CO2 Level", f"{ai.co2:.3f}%", "0.001%")
col3.metric("Water Reserves", f"{ai.water:.1f} L", "-0.4L")

# Display Status & Predictions
st.subheader("System Status")
for msg in status_messages:
    if "⚠️" in msg:
        st.error(msg)
    else:
        st.success(msg)

st.write(f"**Estimated Oxygen Remaining:** {ox_time} hours")
st.write(f"**Estimated Water Remaining:** {wat_time} hours")

# Simple Data Visualization
chart_data = pd.DataFrame({
    'Metric': ['Oxygen', 'Water (Scaled)'],
    'Value': [ai.oxygen, ai.water / 5] 
})
st.bar_chart(chart_data.set_index('Metric'))

# Auto-refresh button
if st.button('Refresh Telemetry'):
    st.rerun()
    
