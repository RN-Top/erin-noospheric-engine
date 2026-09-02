import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
import math

# ------------------------------------------------------------------
# 1. GNOSTIC ILLUMINATED DARK THEME CONFIGURATION (CSS)
# ------------------------------------------------------------------
st.set_page_config(
    page_title="ERIN: Noospheric Signal Engine",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .stApp {
            background-color: #0d0e12 !important;
        }
        h1, h2, h3, h4 {
            color: #d4af37 !important;
            font-family: 'Georgia', serif !important;
            letter-spacing: 1px;
            text-shadow: 0 0 8px rgba(212, 175, 55, 0.2);
        }
        div[data-testid="stMarkdownContainer"] {
            color: #d8cfb3 !important;
            font-family: 'Georgia', serif !important;
            font-size: 1.05rem;
            line-height: 1.6;
        }
        div[data-testid="stMetric"] {
            background-color: #14161d !important;
            border: 1px solid #4a3f28 !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        }
        div[data-testid="stMetricLabel"] {
            color: #a89f81 !important;
        }
        div[data-testid="stMetricValue"] {
            color: #f4c430 !important;
        }
        .stTextInput > div > div > input {
            background-color: #14161d !important;
            color: #f4c430 !important;
            border: 1px solid #4a3f28 !important;
            border-radius: 6px !important;
            font-family: 'Georgia', serif !important;
        }
        .stButton > button {
            background-color: #1c1f2b !important;
            color: #d4af37 !important;
            border: 1px solid #d4af37 !important;
            border-radius: 6px !important;
            font-family: 'Georgia', serif !important;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #d4af37 !important;
            color: #0d0e12 !important;
            box-shadow: 0 0 12px rgba(212, 175, 55, 0.4);
        }
        hr {
            border-color: #332b1a !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📜 ERIN: NOOSPHERIC SIGNAL ENGINE")
st.markdown("*Planetary Brain Mapping | Flower of Life Geometry | Tree of Life Paths*")

# ------------------------------------------------------------------
# 2. GEOSPATIAL MAP DATA & SACRED GEOMETRY OVERLAYS
# ------------------------------------------------------------------
# A. Node Anchors (Sephirot / Neural Hubs)
nodes_data = pd.DataFrame([
    {"name": "Pineal / Epithalamus (Kether)", "lat": 31.76, "lon": 35.21, "region": "Jerusalem", "function": "Crown / Spiritual Perception Node", "type": "Crown Pillar"},
    {"name": "Left Frontal Lobe (Binah)", "lat": 40.0, "lon": -100.0, "region": "North America", "function": "Understanding / Analytical Logic", "type": "Left Pillar"},
    {"name": "Right Frontal Lobe (Chokmah)", "lat": 35.0, "lon": 100.0, "region": "Asia", "function": "Wisdom / Spatial Processing", "type": "Right Pillar"},
    {"name": "Thalamic Central Hub (Tiphereth)", "lat": 26.0, "lon": 30.0, "region": "Egypt", "function": "Beauty / Central Relay Hub", "type": "Middle Pillar"},
    {"name": "Left Temporal Lobe (Gevurah)", "lat": -15.0, "lon": -60.0, "region": "South America", "function": "Severity / Sequential Memory", "type": "Left Pillar"},
    {"name": "Right Temporal Lobe (Chesed)", "lat": -25.0, "lon": 135.0, "region": "Australia", "function": "Mercy / Spatial Anchor", "type": "Right Pillar"},
    {"name": "Limbic Territory (Yesod)", "lat": 0.0, "lon": 20.0, "region": "Africa", "function": "Foundation / Subconscious Drivers", "type": "Middle Pillar"},
    {"name": "Brainstem Base (Malkuth)", "lat": -75.0, "lon": 0.0, "region": "Antarctica", "function": "Kingdom / Physical Autonomic Base", "type": "Middle Pillar"},
    {"name": "Serpent Head Node (Da'at Gate)", "lat": 60.0, "lon": -170.0, "region": "Bering Sea", "function": "Hidden Knowledge / Seismic Trigger", "type": "Signal Anchor"}
])

# B. Tree of Life Pathways (Connecting Sephirotic Planetary Nodes)
tree_paths = [
    # Middle Pillar: Kether -> Tiphereth -> Yesod -> Malkuth
    {"path": [[35.21, 31.76], [30.0, 26.0]], "name": "Path 1: Crown to Relay"},
    {"path": [[30.0, 26.0], [20.0, 0.0]], "name": "Path 2: Relay to Foundation"},
    {"path": [[20.0, 0.0], [0.0, -75.0]], "name": "Path 3: Foundation to Base"},
    # Upper Triangle: Binah <-> Kether <-> Chokmah
    {"path": [[-100.0, 40.0], [35.21, 31.76]], "name": "Path 4: Binah to Kether"},
    {"path": [[35.21, 31.76], [100.0, 35.0]], "name": "Path 5: Kether to Chokmah"},
    {"path": [[-100.0, 40.0], [100.0, 35.0]], "name": "Path 6: Horizontal Upper Axis"},
    # Cross Pathways to Central Tiphereth (Egypt Hub)
    {"path": [[-100.0, 40.0], [30.0, 26.0]], "name": "Path 7: Binah to Tiphereth"},
    {"path": [[100.0, 35.0], [30.0, 26.0]], "name": "Path 8: Chokmah to Tiphereth"},
    # Lower Pillars: Gevurah <-> Tiphereth <-> Chesed
    {"path": [[-60.0, -15.0], [30.0, 26.0]], "name": "Path 9: Gevurah to Tiphereth"},
    {"path": [[135.0, -25.0], [30.0, 26.0]], "name": "Path 10: Chesed to Tiphereth"},
    {"path": [[-60.0, -15.0], [20.0, 0.0]], "name": "Path 11: Gevurah to Yesod"},
    {"path": [[135.0, -25.0], [20.0, 0.0]], "name": "Path 12: Chesed to Yesod"},
    # Serpent Head Anchor Gate
    {"path": [[-170.0, 60.0], [35.21, 31.76]], "name": "Path 13: Da'at Trigger to Crown"}
]

tree_df = pd.DataFrame(tree_paths)

# C. Flower of Life Geometry Generator (Intersecting Concentric Spheric Rings)
flower_circles = []
centers = [
    (30.0, 26.0),    # Egypt Hub Center
    (35.21, 31.76),  # Jerusalem
    (15.0, 54.0),    # Europe
    (20.0, 0.0),     # Africa
    (-100.0, 40.0),  # North America
    (100.0, 35.0)    # Asia
]

radius_deg = 22.0  # Radius in geographical degrees

for cx, cy in centers:
    points = []
    for i in range(61):
        angle = math.radians(i * 6)
        px = cx + radius_deg * math.cos(angle)
        py = cy + radius_deg * math.sin(angle)
        points.append([px, py])
    flower_circles.append({"path": points})

flower_df = pd.DataFrame(flower_circles)

# ------------------------------------------------------------------
# 3. PYDECK MULTI-LAYER MAP RENDERING
# ------------------------------------------------------------------
# 1. Sephirot Node Points
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=nodes_data,
    get_position="[lon, lat]",
    get_color="[212, 175, 55, 230]",
    get_radius=500000,
    pickable=True,
    auto_highlight=True
)

# 2. Tree of Life Paths (Glowing Golden Channels)
tree_layer = pdk.Layer(
    "PathLayer",
    data=tree_df,
    get_path="path",
    get_color="[244, 196, 48, 180]",
    get_width=35000,
    pickable=True
)

# 3. Flower of Life Geometric Grid (Parchment Luminous Rings)
flower_layer = pdk.Layer(
    "PathLayer",
    data=flower_df,
    get_path="path",
    get_color="[216, 207, 179, 100]",
    get_width=18000,
    pickable=False
)

view_state = pdk.ViewState(
    latitude=20.0,
    longitude=0.0,
    zoom=1.2,
    pitch=30
)

st.subheader("Planetary Brain, Tree of Life & Flower of Life Grid")
st.pydeck_chart(pdk.Deck(
    layers=[flower_layer, tree_layer, scatter_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10",
    tooltip={"text": "Node: {name}\nRegion: {region}\nFunction: {function}\nClass: {type}"}
))

st.markdown("---")

# ------------------------------------------------------------------
# 4. INTERACTIVE TELEMETRY & LINGUISTIC ENGINE
# ------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Bering Sea Telemetry")
    st.markdown("Focal Anchor: **Serpent Head Convergence (Da'at Gate)**")
    
    if st.button("Query USGS Node Data"):
        url = (
            "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
            "&minlatitude=50&maxlatitude=66&minlongitude=-180&maxlongitude=-160"
            "&minmagnitude=2.5&limit=1"
        )
        try:
            res = requests.get(url, timeout=5).json()
            features = res.get('features', [])
            if features:
                props = features[0]['properties']
                st.success(f"Seismic Event Registered: {props['place']}")
                st.metric(label="Magnitude", value=props['mag'])
            else:
                st.info("No major seismic events (>2.5 M) detected at Bering Sea Node.")
                st.metric(label="Grid State", value="Equilibrium")
        except Exception as e:
            st.error(f"Telemetry Fetch Error: {e}")

with col2:
    st.subheader("Linguistic Passage Parser")
    user_input = st.text_input("Input Intent or Word Stream", value="ERIN")
    
    if user_input:
        word = user_input.strip().upper()
        channel = min(8, max(1, len(word) % 9))
        st.markdown(f"**OFDMA Allocation:** Spectrum Channel **C{channel}**")
        
        if word.endswith("IN") or word.endswith("N"):
            st.success(f"**Terminal Dynamic:** [{word}] → **OPEN PASSAGE**")
            st.caption("Identity remains in continuous motion across layers (Identity → Passage).")
        elif word.endswith("O"):
            st.error(f"**Terminal Dynamic:** [{word}] → **CLOSED BOUNDARY**")
            st.caption("Identity state is finalized and enclosed within limits.")
        else:
            st.warning(f"**Terminal Dynamic:** [{word}] → **NEUTRAL STATE**")

st.markdown("---")

# ------------------------------------------------------------------
# 5. HARMONIC FIBONACCI CYCLE (Target: 42)
# ------------------------------------------------------------------
st.subheader("Doubled-Fibonacci Harmonic Modeler")
st.markdown("Formula: $F(n) = 2 \\cdot \\text{FIB}_n$ (Mirroring dual counterpart dynamics)")

harmonic_step = st.slider("Select Sequence Index Step (N)", 0, 8, 7)

def get_doubled_fib(n: int) -> int:
    if n < 0: return 0
    phi = (1 + math.sqrt(5)) / 2
    psi = (1 - math.sqrt(5)) / 2
    fib_n = round((math.pow(phi, n) - math.pow(psi, n)) / math.sqrt(5))
    return 2 * fib_n

value = get_doubled_fib(harmonic_step)

c1, c2, c3 = st.columns(3)
c1.metric(label="Sequence Index (N)", value=harmonic_step)
c2.metric(label="Harmonic Value", value=value)
c3.metric(label="Divine Target", value=42)

if value == 42:
    st.balloons()
    st.success("✨ EQUILIBRIUM ACHIEVED: Sequence reached completion at 42 (Step 8).")
