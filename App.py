import streamlit as st
import random
import time
import pandas as pd

# Reuse your SpaceStationAI class logic here (copy-paste your class)
# ... [Insert your SpaceStationAI class here] ...

st.set_page_config(page_title="ISS Life Support Dashboard", layout="wide")
st.title("🚀 Space Station AI Monitor")

# Sidebar for Inputs
st.sidebar.header("Mission Configuration")
astronauts = st.sidebar.slider("Number of Astronauts", 1, 10, 3)
activity = st.sidebar.selectbox("Activity Level", ["Low", "Medium", "High"])

# Initialize the AI in Session State so it persists
if 'ai' not in st.session_state:
    st.session_state.ai = SpaceStationAI(astronauts, activity)

ai = st.session_state.ai

# Layout: Metric Columns
col1, col2, col3 = st.columns(3)
ai.update_sensors()
ox_time, wat_time = ai.calculate_time_left()

col1.metric("Oxygen Level", f"{ai.oxygen:.2f}%", "-0.15%")
col2.metric("CO₂ Level", f"{ai.co2:.2f}%", "0.04%", delta_color="inverse")
col3.metric("Water Supply", f"{ai.water:.1f}L")

# Status and Predictions
st.subheader("System Status")
for s in ai.check_status(ox_time, wat_time):
    if "danger" in s.lower() or "critical" in s.lower():
        st.error(s)
    else:
        st.success(s)

# Trigger a rerun to simulate real-time updates
time.sleep(2)
st.rerun()
