import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
from alpha_engine import AlphaEngine

# Page Config
st.set_page_config(page_title="Supply Chain Monitoring Dashboard", layout="wide")

# Simulation logic for demonstration
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['timestamp', 'activity'])
    st.session_state['engine'] = AlphaEngine(historical_baseline=15.0)

# Sidebar UI
st.sidebar.title("Supply Chain Control Panel")
feed_source = st.sidebar.selectbox("Select Data Feed", ["Real-time Camera (Sim)", "Logistics Port Alpha-1", "Channel Terminal B"])
monitoring_active = st.sidebar.toggle("Activate YOLO Monitoring", value=True)

# Main Dashboard
st.title("Qualitative Alpha Explorer")
st.markdown("---")

col1, col2, col3 = st.columns(3)

# Data generation simulation loop
if monitoring_active:
    # Add new dummy data point for visualization
    new_point = {
        'timestamp': pd.Timestamp.now(),
        'activity': np.random.randint(10, 25)
    }
    st.session_state['data'] = pd.concat([st.session_state['data'], pd.DataFrame([new_point])], ignore_index=True)
    if len(st.session_state['data']) > 50:
        st.session_state['data'] = st.session_state['data'].iloc[1:]

# Metrics
engine = st.session_state['engine']
history = st.session_state['data']
current_idx = engine.calculate_activity_index(history)
trend_status = engine.detect_trends(history)
alpha_signal = engine.get_alpha_signal(current_idx, trend_status)

with col1:
    st.metric("Logistics Activity Index", f"{current_idx}%", delta=f"{round(current_idx - 100, 1)}%")
with col2:
    st.metric("Supply Chain Trend", trend_status)
with col3:
    st.info(f"Alpha Signal: **{alpha_signal}**")

# Visualization
st.subheader("Freight Movement Velocity (Real-time Feed)")
fig = px.line(history, x='timestamp', y='activity', title="Supply Chain Activity Frequency", 
              labels={'activity': 'Unit Count', 'timestamp': 'Time'},
              line_shape='spline', render_mode='svg')
fig.update_traces(line_color='#1f77b4', line_width=3)
st.plotly_chart(fig, use_container_width=True)

# Footer/Status
st.markdown("---")
st.caption("Monitoring Powered by YOLO v11 and Qualitative Alpha Engine.")

if monitoring_active:
    time.sleep(1)
    st.rerun()
