import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Wi-Fi RSSI Analyzer",
    page_icon="📶",
    layout="wide"
)


# -----------------------------
# Title
# -----------------------------

st.sidebar.title("⚙️ Controls")
st.sidebar.write("Upload your Wi-Fi measurement data below.")

st.title("📶 Wi-Fi RSSI Analyzer")

st.write(
    "Analyze Wi-Fi signal strength and visualize "
    "network coverage using an interactive heatmap."
)


# -----------------------------
# Load Data
# -----------------------------

uploaded_file = st.sidebar.file_uploader(
    "📤 Upload Wi-Fi CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/sample_wifi_data.csv")


# -----------------------------
# Signal Quality
# -----------------------------

def signal_quality(rssi):

    if rssi >= -50:
        return "Excellent"

    elif rssi >= -60:
        return "Good"

    elif rssi >= -70:
        return "Fair"

    elif rssi >= -80:
        return "Weak"

    else:
        return "Very Weak"


df["quality"] = df["rssi"].apply(signal_quality)


# -----------------------------
# Dashboard Metrics
# -----------------------------

average_rssi = df["rssi"].mean()
best_rssi = df["rssi"].max()
weakest_rssi = df["rssi"].min()

weak_areas = len(
    df[df["rssi"] < -70]
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "📊 Average RSSI",
    f"{average_rssi:.1f} dBm"
)

col2.metric(
    "🟢 Best Signal",
    f"{best_rssi} dBm"
)

col3.metric(
    "🔴 Weakest Signal",
    f"{weakest_rssi} dBm"
)

col4.metric(
    "⚠️ Weak Areas",
    weak_areas
)


st.divider()


# -----------------------------
# Heatmap
# -----------------------------

st.subheader("🗺️ Wi-Fi Signal Heatmap")


center_lat = df["latitude"].mean()
center_lon = df["longitude"].mean()


wifi_map = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=16
)


heat_data = []


for _, row in df.iterrows():

    signal_strength = max(
        0,
        100 + row["rssi"]
    )

    heat_data.append([
        row["latitude"],
        row["longitude"],
        signal_strength
    ])


HeatMap(
    heat_data,
    radius=25,
    blur=20
).add_to(wifi_map)


st_folium(
    wifi_map,
    width=1200,
    height=500
)


# -----------------------------
# RSSI Chart
# -----------------------------

st.subheader("📈 Signal Strength by Location")


fig = px.bar(
    df,
    x="location",
    y="rssi",
    color="quality",
    title="Wi-Fi RSSI"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------
# Data Table
# -----------------------------

st.subheader("📋 Wi-Fi Measurements")


st.dataframe(
    df,
    use_container_width=True
)
