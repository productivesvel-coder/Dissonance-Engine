import streamlit as st
from tavily import TavilyClient
import google.generativeai as gem
import json
import re
import streamlit.components.v1 as components
st.set_page_config(layout="wide",page_title="Dissonance Engine",initial_sidebar_state="expanded")
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 2rem; font-family: 'Inter', sans-serif; }
    .stTextInput input { border-radius: 8px; background-color: #0f172a; color: #f8fafc; border: 1px solid #334155; }
    .stButton>button {border-radius: 8px;background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);color: white; font-weight: 600; border: none; padding: 10px 24px; transition: 0.3s; width: 100%;}
    
    /* Audit Card CSS for Distinct Sections */
    .audit-card {background-color: #0f172a;border-radius: 12px;padding: 20px;margin-bottom: 15px;border: 1px solid #1e293b;transition: border-color 0.2s ease;}
    .audit-card:hover { border-color: #3b82f6; }
    .card-title { font-weight: 700; font-size: 1.1rem; margin-bottom: 8px; }
    .card-detail { color: #94a3b8; font-size: 0.95rem; line-height: 1.5; }
    .consensus-accent { border-left: 4px solid #00ff7f; }
    .dissonance-accent { border-left: 4px solid #ff003c; }

    div[data-testid="stExpander"] { background-color: #0B0F19; border: 1px solid #1e293b; border-radius: 8px; }
    div[data-testid="stExpander"] summary p { font-weight: 600; color: #f8fafc; }
    /* Bias Meter CSS */
    .bias-bar-bg { width: 100%; background: #1e293b; height: 6px; border-radius: 3px; margin-top: 5px; margin-bottom: 12px; }
    .bias-bar-fill { height: 100%; border-radius: 3px; transition: width 0.5s ease-in-out; }
</style>
""", unsafe_allow_html=True)

#apikeys
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
AI_ENGINE_KEY = st.secrets["AI_ENGINE_KEY"]
with st.sidebar:
    st.markdown("### System Telemetry")
    st.markdown("---")
    st.write("🟢 **Data Fetcher:** Active")
    st.write("🟢 **AI Engine:** Operational")
    st.write("🟢 **Render Engine:** WebGL Adaptive Chroma")
    st.markdown("---")
    st.caption("Vortex Legend:")
    st.markdown("<span style='color: #ff003c; font-weight: bold;'>●</span> CONTRADICTION (Turbulence)", unsafe_allow_html=True)
    st.markdown("<span style='color: #00ff7f; font-weight: bold;'>●</span> CONSENSUS (Smooth Flow)", unsafe_allow_html=True)
    st.markdown("---")
    st.info("🖱️ **Vortex Control:** Hover to feel particle mass. Click the map to freeze/unfreeze flow. Red particles will continue to vibrate.")
st.title("Dissonance Engine")
st.markdown("<p style='color: #94a3b8; font-size: 1.1rem;'>Real-time fluid dynamic audit of global narrative logical structures.</p>", unsafe_allow_html=True)
event=st.text_input(""Target Subject / Event", placeholder="Enter geopolitical event or global narrative to analyse...")
