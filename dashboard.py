import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from alpha_engine import AlphaEngine
from forecaster import SupplyForecaster
from storage import DataStorage
from alternative_data_sim import AlternativeDataSim

# Page Config
st.set_page_config(page_title="Supply Chain Research Lab", layout="wide")

# Persistent State Management
if 'storage' not in st.session_state:
    st.session_state['storage'] = DataStorage()
    st.session_state['engine'] = AlphaEngine(historical_baseline=15.0)
    st.session_state['forecaster'] = SupplyForecaster()
    st.session_state['alt_sim'] = AlternativeDataSim()
    # Pre-populate history for research demo
    dummy_hist = pd.DataFrame({
        'timestamp': pd.date_range(end=pd.Timestamp.now(), periods=50, freq='min'),
        'activity': np.random.randint(10, 25, 50)
    })
    st.session_state['data'] = dummy_hist

# Sidebar UI
st.sidebar.title("🚀 Supply Chain Terminal")
mode = st.sidebar.radio("Navigation", ["Live Monitoring", "Research Lab", "Historical Audit"])
st.sidebar.markdown("---")
st.sidebar.subheader("Terminal Status")
st.sidebar.success("YOLO v11 Engine: ONLINE")
st.sidebar.info("Database: SQLite Connected")

# Shared Logic
engine = st.session_state['engine']
history = st.session_state['data']
forecaster = st.session_state['forecaster']
storage = st.session_state['storage']
alt_sim = st.session_state['alt_sim']

if mode == "Live Monitoring":
    st.title("🛰️ Live Logistics Intelligence")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Simulate Real-time Ingestion
    new_activity = np.random.randint(12, 28)
    new_point = {'timestamp': pd.Timestamp.now(), 'activity': new_activity}
    st.session_state['data'] = pd.concat([st.session_state['data'], pd.DataFrame([new_point])], ignore_index=True)
    
    # Advanced Metrics
    current_z = engine.calculate_z_score(new_activity, history)
    current_trend = engine.detect_trends(history)
    alpha_signal = engine.get_alpha_signal(current_z, current_trend)
    
    # Log to CSV/DB
    storage.log_activity("TERMINAL-ALPHA", int(new_activity), current_z, alpha_signal)

    with col1:
        st.metric("Activity Z-Score", f"{current_z}σ", delta=f"{current_z}σ")
    with col2:
        st.metric("Logistics Trend", "Expansion" if "Expansion" in current_trend else "Contraction")
    with col3:
        st.write("**Alpha Signal**")
        if "BUY" in alpha_signal:
            st.success(alpha_signal)
        elif "SELL" in alpha_signal:
            st.error(alpha_signal)
        else:
            st.info(alpha_signal)
    with col4:
        st.metric("Terminal Volume", f"{new_activity} Units")

    # Live Chart
    fig = px.area(history.tail(30), x='timestamp', y='activity', title="Supply Chain Pulse (Rolling Window)")
    st.plotly_chart(fig, use_container_width=True)

    # Forecasting
    st.subheader("🔮 Predictive Logistics Forecast")
    future_vals = forecaster.forecast_next_periods(history)
    if future_vals:
        forecast_df = pd.DataFrame({
            'T+1': [future_vals[0]],
            'T+2': [future_vals[1]],
            'T+3': [future_vals[2]]
        })
        st.table(forecast_df)

elif mode == "Research Lab":
    st.title("🔬 Quantitative Research Lab")
    st.markdown("Deep dive into logistical correlation and statistical anomalies.")
    
    macro_data = alt_sim.generate_macro_indicators()
    corr_val = alt_sim.calculate_correlation(history, macro_data)
    
    st.info(f"Correlation (Visual Activity vs. Fuel Price Index): **{corr_val}**")

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Statistical Distribution")
        fig_dist = px.histogram(history, x="activity", nbins=20, title="Freight Volume Distribution")
        st.plotly_chart(fig_dist)
        
    with col_b:
        st.subheader("Macro Correlation Map")
        # Visualizing macro trends
        fig_macro = px.line(macro_data, x='date', y=['fuel_price_index', 'global_shipping_index'], 
                           title="Global Macro Supply Chain Indicators")
        st.plotly_chart(fig_macro)

elif mode == "Historical Audit":
    st.title("📜 Documented Alpha History")
    db_history = storage.get_history(50)
    st.dataframe(db_history, use_container_width=True)
    
    if st.button("Export Research Report (CSV)"):
        csv = db_history.to_csv(index=False).encode('utf-8')
        st.download_button("Download Report", data=csv, file_name="supply_chain_alpha.csv")

# Autorefresh for Live Monitoring
if mode == "Live Monitoring":
    time.sleep(2)
    st.rerun()
