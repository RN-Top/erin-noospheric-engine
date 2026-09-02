import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
import math

# Safe import block
try:
    from google import genai
    GENAI_AVAILABLE = True
except ModuleNotFoundError:
    GENAI_AVAILABLE = False
import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
import math

# Try importing the Google GenAI SDK safely
try:
    from google import genai
    GENAI_AVAILABLE = True
except ModuleNotFoundError:
    GENAI_AVAILABLE = False

# ------------------------------------------------------------------
# 1. GNOSTIC ILLUMINATED DARK THEME CONFIGURATION (CSS)
# ------------------------------------------------------------------
st.set_page_config(
    page_title="ERIN: Noospheric Signal Engine",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
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

# ------------------------------------------------------------------
# 2. SIDEBAR: AI INTERPRETER & GEMINI API CONFIGURATION
# ------------------------------------------------------------------
with st.sidebar:
    st.header("🔮 AI Noospheric Interpreter")
    st.markdown("Connect an API key to enable live conversational explanations.")
    
    gemini_api_key = st.text_input("Google Gemini API Key", type="password", help="Get a free key from Google AI Studio")
    
    client = None
    if gemini_api_key:
        if GENAI_AVAILABLE:
            try:
                client = genai.Client(api_key=gemini_api_key)
                st.success("AI Neural Link Active")
            except Exception as e:
                st.error(f"Initialization Error: {e}")
        else:
            st.error("The `google-genai` package is installing on Streamlit Cloud. Please reboot your app via Manage App menu.")
    else:
        st.info("Operating in Rule-Based Fallback Mode. Enter a Gemini API Key above for full generative AI insights.")

    st.markdown("---")
    st.subheader("💬 Ask ERIN AI")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_query = st.text_input("Ask a question about the grid:")
    if st.button("Send Query"):
        if user_query:
            st.session_state.chat_history.append(("User", user_query))
            if client:
                try:
                    prompt = f"""
                    You are ERIN, an AI Noospheric Signal Engine. You interpret planetary geography mapped to human brain anatomy,
                    the Tree of Life, Flower of Life, and telemetry data. Answer the following user question in an authoritative,
                    illuminated, and clear architectural tone: {user_query}
                    """
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )
                    st.session_state.chat_history.append(("ERIN AI", response.text))
                except Exception as e:
                    st.session_state.chat_history.append(("ERIN AI", f"Error generating response: {e}"))
            else:
                st.session_state.chat_history.append((
                    "ERIN AI", 
                    "To receive custom AI explanations, please enter a valid Google Gemini API key at the top of the sidebar."
                ))

    # Display Chat History
    for role, text in reversed(st.session_state.chat_history):
        st.markdown(f"**{role}:** {text}")

# ------------------------------------------------------------------
# 3. MAIN DASHBOARD HEADER & CODEX
# ------------------------------------------------------------------
st.title("📜 ERIN: NOOSPHERIC SIGNAL ENGINE")
st.markdown("*Planetary Brain Mapping | Sacred Geometry Overlay | Macro-Cognitive Telemetry*")

with st.expander("📖 ABOUT ERIN: System Codex & Architectural Insight", expanded=False):
    st.markdown("""
    **ERIN (Noospheric Signal Engine)** is a macro-cognitive lens designed to map global planetary structures onto human neural geography and sacred geometric matrices. 
    
    * **3D Planetary Brain Map:** Correlates geographic continental masses to neural structures (e.g., North America as the Left Frontal Lobe, Eurasia as the Right Frontal Lobe, and Egypt as the Central Thalamic Relay Hub).
    * **Tree & Flower of Life Layers:** Visualizes geometric pathways (Tree of Life Sephirotic channels) and intersecting harmonic rings (Flower of Life) anchoring global consciousness to physical geography.
    * **Live Planetary Telemetry:** Continuously queries the USGS Earthquake API across 9 major global Sephirotic nodes to measure real-time physical crustal activity.
    * **Linguistic Spectrum Parser:** Translates arbitrary human language strings into OFDMA Wi-Fi 6 channels ($C1 \\rightarrow C8$), determining whether an intent represents an **Open Passage** (`-IN`/`-N`), a **Closed Boundary** (`-O`), or a **Neutral Baseline**.
    * **Doubled-Fibonacci Modeler:** Calculates sequence progression using $F(n) = 2 \\cdot \\text{FIB}_n$, tracking alignment toward the divine target equilibrium of **42**.
    """)

st.markdown("---")

# ------------------------------------------------------------------
# 4. GEOSPATIAL MAP DATA & SACRED GEOMETRY OVERLAYS
# ------------------------------------------------------------------
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

tree_paths = [
    {"path": [[35.21, 31.76], [30.0, 26.0]], "name": "Path 1: Crown to Relay"},
    {"path": [[30.0, 26.0], [20.0, 0.0]], "name": "Path 2: Relay to Foundation"},
    {"path": [[20.0, 0.0], [0.0, -75.0]], "name": "Path 3: Foundation to Base"},
    {"path": [[-100.0, 40.0], [35.21, 31.76]], "name": "Path 4: Binah to Kether"},
    {"path": [[35.21, 31.76], [100.0, 35.0]], "name": "Path 5: Kether to Chokmah"},
    {"path": [[-100.0, 40.0], [100.0, 35.0]], "name": "Path 6: Horizontal Upper Axis"},
    {"path": [[-100.0, 40.0], [30.0, 26.0]], "name": "Path 7: Binah to Tiphereth"},
    {"path": [[100.0, 35.0], [30.0, 26.0]], "name": "Path 8: Chokmah to Tiphereth"},
    {"path": [[-60.0, -15.0], [30.0, 26.0]], "name": "Path 9: Gevurah to Tiphereth"},
    {"path": [[135.0, -25.0], [30.0, 26.0]], "name": "Path 10: Chesed to Tiphereth"},
    {"path": [[-60.0, -15.0], [20.0, 0.0]], "name": "Path 11: Gevurah to Yesod"},
    {"path": [[135.0, -25.0], [20.0, 0.0]], "name": "Path 12: Chesed to Yesod"},
    {"path": [[-170.0, 60.0], [35.21, 31.76]], "name": "Path 13: Da'at Trigger to Crown"}
]
tree_df = pd.DataFrame(tree_paths)

flower_circles = []
centers = [(30.0, 26.0), (35.21, 31.76), (15.0, 54.0), (20.0, 0.0), (-100.0, 40.0), (100.0, 35.0)]
radius_deg = 22.0

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
# 5. PYDECK MAP RENDERING
# ------------------------------------------------------------------
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=nodes_data,
    get_position="[lon, lat]",
    get_color="[212, 175, 55, 230]",
    get_radius=500000,
    pickable=True,
    auto_highlight=True
)

tree_layer = pdk.Layer(
    "PathLayer",
    data=tree_df,
    get_path="path",
    get_color="[244, 196, 48, 180]",
    get_width=35000,
    pickable=True
)

flower_layer = pdk.Layer(
    "PathLayer",
    data=flower_df,
    get_path="path",
    get_color="[216, 207, 179, 100]",
    get_width=18000,
    pickable=False
)

view_state = pdk.ViewState(latitude=20.0, longitude=0.0, zoom=1.2, pitch=30)

st.subheader("Planetary Brain, Tree of Life & Flower of Life Grid")
st.pydeck_chart(pdk.Deck(
    layers=[flower_layer, tree_layer, scatter_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10",
    tooltip={"text": "Node: {name}\nRegion: {region}\nFunction: {function}\nClass: {type}"}
))

st.markdown("---")

# ------------------------------------------------------------------
# 6. EXPANDED MULTI-NODE TELEMETRY & LINGUISTIC ENGINE
# ------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Global Telemetry Monitor (9 Sephirotic Hubs)")
    
    node_bounds = {
        "Jerusalem Node (Kether)": {"minlat": 29, "maxlat": 33, "minlon": 34, "maxlon": 36},
        "North America Node (Binah)": {"minlat": 30, "maxlat": 50, "minlon": -120, "maxlon": -80},
        "Asia Node (Chokmah)": {"minlat": 20, "maxlat": 45, "minlon": 80, "maxlon": 120},
        "Egypt Relay Hub (Tiphereth)": {"minlat": 20, "maxlat": 32, "minlon": 25, "maxlon": 36},
        "South America Node (Gevurah)": {"minlat": -30, "maxlat": 0, "minlon": -80, "maxlon": -40},
        "Australia Node (Chesed)": {"minlat": -40, "maxlat": -10, "minlon": 110, "maxlon": 155},
        "Africa Node (Yesod)": {"minlat": -10, "maxlat": 15, "minlon": 10, "maxlon": 35},
        "Antarctica Base (Malkuth)": {"minlat": -85, "maxlat": -60, "minlon": -180, "maxlon": 180},
        "Bering Sea Node (Da'at Gate)": {"minlat": 50, "maxlat": 66, "minlon": -180, "maxlon": -160}
    }
    
    selected_node = st.selectbox("Select Target Sephirotic Node", list(node_bounds.keys()))
    
    if st.button("Poll Live Node Telemetry"):
        bounds = node_bounds[selected_node]
        url = (
            f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
            f"&minlatitude={bounds['minlat']}&maxlatitude={bounds['maxlat']}"
            f"&minlongitude={bounds['minlon']}&maxlongitude={bounds['maxlon']}"
            f"&minmagnitude=2.0&limit=1"
        )
        try:
            res = requests.get(url, timeout=5).json()
            features = res.get('features', [])
            if features:
                props = features[0]['properties']
                st.success(f"Seismic Activity Registered: {props['place']}")
                st.metric(label="Magnitude (M)", value=props['mag'])
            else:
                st.info(f"No active seismic triggers detected at {selected_node}.")
                st.metric(label="Node Energy Level", value="Quiescent")
        except Exception as e:
            st.error(f"Telemetry Network Error: {e}")

with col2:
    st.subheader("Linguistic Passage & AI Interpreter")
    user_input = st.text_input("Input Intent or Word Stream", value="ERIN")
    
    if user_input:
        word = user_input.strip().upper()
        channel = min(8, max(1, len(word) % 9))
        st.markdown(f"**OFDMA Channel:** **C{channel}**")
        
        if word.endswith("IN") or word.endswith("N"):
            dynamic = "OPEN PASSAGE"
            st.success(f"**Terminal Dynamic:** [{word}] → **OPEN PASSAGE**")
        elif word.endswith("O"):
            dynamic = "CLOSED BOUNDARY"
            st.error(f"**Terminal Dynamic:** [{word}] → **CLOSED BOUNDARY**")
        else:
            dynamic = "NEUTRAL STATE"
            st.warning(f"**Terminal Dynamic:** [{word}] → **NEUTRAL STATE**")
            
        # Generative AI dynamic insight generation
        if client:
            try:
                ai_prompt = f"In 2 brief sentences, interpret the word '{word}' assigned to spectrum C{channel} with dynamic '{dynamic}' within a cybernetic noospheric planetary grid context."
                ai_response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=ai_prompt
                ).text
                st.markdown(f"> **AI Generative Analysis:** *{ai_response}*")
            except Exception:
                st.markdown(f"> **AI Insight:** *Signal '{word}' resonates as a {dynamic} state across Spectrum Channel C{channel}.*")
        else:
            st.markdown(f"> **Fallback Insight:** *Signal '{word}' acts as a {dynamic} vector on Spectrum Channel C{channel}.*")

st.markdown("---")

# ------------------------------------------------------------------
# 7. HARMONIC FIBONACCI CYCLE (Target: 42)
# ------------------------------------------------------------------
st.subheader("Doubled-Fibonacci Harmonic Modeler")
st.markdown("Formula: $F(n) = 2 \\cdot \\text{FIB}_n$ (Tracking alignment toward divine equilibrium)")

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
