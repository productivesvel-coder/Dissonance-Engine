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
event=st.text_input("Target Subject / Event", placeholder="Enter geopolitical event or global narrative to analyse...")
def stabilize_vortex(raw_telemetry):
    sanitized_payload = raw_telemetry.strip()
    sanitized_payload = re.sub(r'[^}\]" \w]$', '', sanitized_payload)
    if sanitized_payload.count('"') % 2 != 0: 
        sanitized_payload += '"'
    integrity_stack = []
    for char in sanitized_payload:
        if char == '{': 
            integrity_stack.append('}')
        elif char == '[': 
            integrity_stack.append(']')
        elif char in '}]':
            if integrity_stack and integrity_stack[-1] == char: 
                integrity_stack.pop()
    return sanitized_payload + "".join(reversed(integrity_stack))
def geminiapicall(reports6):
    gem.configure(api_key=AI_ENGINE_KEY)
    model = gem.GenerativeModel('gemini-3.5-flash')
    context = "\n".join([f"[{r['title']} | {r['url']}] - {r['content']}" for r in reports6])
    prompt = f"""
    [SYSTEM PROTOCOL: DISONANCE ENGINE]
    Analyze the text for logical consensus and dissonance. Perform a linguistic bias audit.
    
    Critical requirement:
    1. Your 'particles' list must be a visual reflection of your summary. If you identify a 'contradiction' in the summary, you must create corresponding particles with "type": "contradiction" to represent the turbulence.
    2. Divide the summary into multiple distinct subjects/claims. Do not write one massive overview.
    
    Return a raw json object with exactly this structure. Keep particle descriptions under 200 characters.
    {{"particles": [
        {{"id": "p1", "type": "consensus", "name": "Short Topic", "description": "Short detail...", "source": "Publisher Name", "bias_score": 0.2, "bias_label": "Neutral"}},
        {{"id": "p2", "type": "contradiction", "name": "Short Topic", "description": "Short detail...", "source": "Publisher Name", "bias_score": 0.8, "bias_label": "Sensationalized"}}],
      "summary": {{"common_claims": [{{"title": "Distinct Consensus 1", "detail": "Specific structural breakdown with evidence..."}},{{"title": "Distinct Consensus 2", "detail": "Specific structural breakdown with evidence..."}}],
      "contradictions": [{{"title": "Distinct Conflict 1", "detail": "Granular analysis of this specific diverging narrative..."}},{{"title": "Distinct Conflict 2", "detail": "Granular analysis of this specific diverging narrative..."}}]}}}}    
    Rules:
    - extract 8-12 'particles' total.
    - 'type' must be either "consensus" or "contradiction".
    - 'bias_score' must be a float between 0.0 (Neutral) and 1.0 (Highly Loaded/Partisan).
    - NO literal newlines inside strings.
    - output raw json only. NO markdown.
    
    Context: {context}
    """
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json", "max_output_tokens": 8192, "temperature": 0.2})
    generatedinf = response.text.strip()
    json_match = re.search(r'(\{.*\})', generatedinf, re.DOTALL)
    refi = json_match.group(1) if json_match else generatedinf
    refi = "".join(char for char in refi if ord(char) >= 32 or char in "\n\r\t")
    refi = re.sub(r'(?<!\\)\n', ' ', refi)
    try:
        data = json.loads(refinedver, strict=False)
    except json.JSONDecodeError:
        try:
            data = json.loads(stabilise_vortex(refi), strict=False)
        except Exception:
            # Fallback placeholder to prevent app crash
            data = {"particles": [], "summary": {"common_claims": [], "contradictions": [{"title": "Data Parse Error", "detail": "AI output structure failed."}]}}
    
    return data
