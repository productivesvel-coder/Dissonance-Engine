import json
import re

import google.generativeai as gem
import streamlit as st
import streamlit.components.v1 as components
from tavily import TavilyClient


st.set_page_config(
    layout="wide",
    page_title="Dissonance Engine",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    """,
    unsafe_allow_html=True,
)

TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
AI_ENGINE_KEY = st.secrets["AI_ENGINE_KEY"]


with st.sidebar:
    st.markdown("### System Telemetry\n---")
    st.write("🟢 **Data Fetcher:** Active")
    st.write("🟢 **AI Engine:** Operational")
    st.write("🟢 **Render Engine:** WebGL Adaptive Chroma")

    st.markdown("---")
    st.caption("Vortex Legend:")

    st.markdown(
        "● CONTRADICTION (Turbulence)",
        unsafe_allow_html=True,
    )
    st.markdown(
        "● CONSENSUS (Smooth Flow)",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.info(
        "🖱️ **Vortex Control:** Hover to feel particle mass. "
        "Click the map to freeze/unfreeze flow. "
        "Red particles will continue to vibrate."
    )


st.title("Dissonance Engine")

st.markdown(
    """
    Real-time fluid dynamic audit of global narrative logical structures.
    """,
    unsafe_allow_html=True,
)


event = st.text_input(
    "Target Subject / Event",
    placeholder="Enter geopolitical event or global narrative to analyse...",
)


@st.cache_data(ttl=3600)
def call_tavily_api(query):
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=6,
    )

    if not response.get("results"):
        raise ValueError("No verified news sources found.")

    return response["results"]


def stabilize_vortex(raw_telemetry):
    sanitized_payload = raw_telemetry.strip()

    sanitized_payload = re.sub(
        r'[^}]" \w]$',
        "",
        sanitized_payload,
    )

    if sanitized_payload.count('"') % 2 != 0:
        sanitized_payload += '"'

    integrity_stack = []

    for char in sanitized_payload:
        if char == "{":
            integrity_stack.append("}")

        elif char == "[":
            integrity_stack.append("]")

        elif char in "}]":
            if integrity_stack and integrity_stack[-1] == char:
                integrity_stack.pop()

    return sanitized_payload + "".join(reversed(integrity_stack))


@st.cache_data(ttl=3600)
def gemini_api_call(reports6):
    gem.configure(api_key=AI_ENGINE_KEY)

    model = gem.GenerativeModel("gemini-1.5-flash")

    context = "\n".join(
        f"[{report['title']} | {report['url']}] - {report['content']}"
        for report in reports6
    )

    prompt = f"""
[SYSTEM PROTOCOL: DISSONANCE ENGINE]

Analyze the text for logical consensus and dissonance.
Perform a linguistic bias audit.

Critical requirement:

1. Your "particles" list must be a visual reflection of your summary.
   If you identify a "contradiction" in the summary, you must create
   corresponding particles with "type": "contradiction" to represent
   the turbulence.

2. Divide the summary into multiple distinct subjects/claims.
   Do not write one massive overview.

Return a raw JSON object with exactly this structure.
Keep particle descriptions under 200 characters.

{{
    "particles": [
        {{
            "id": "p1",
            "type": "consensus",
            "name": "Short Topic",
            "description": "Short detail...",
            "source": "Publisher Name",
            "bias_score": 0.2,
            "bias_label": "Neutral"
        }},
        {{
            "id": "p2",
            "type": "contradiction",
            "name": "Short Topic",
            "description": "Short detail...",
            "source": "Publisher Name",
            "bias_score": 0.8,
            "bias_label": "Sensationalized"
        }}
    ],

    "summary": {{
        "common_claims": [
            {{
                "title": "Distinct Consensus 1",
                "detail": "Specific structural breakdown with evidence..."
            }},
            {{
                "title": "Distinct Consensus 2",
                "detail": "Specific structural breakdown with evidence..."
            }}
        ],

        "contradictions": [
            {{
                "title": "Distinct Conflict 1",
                "detail": "Granular analysis of this specific diverging narrative..."
            }},
            {{
                "title": "Distinct Conflict 2",
                "detail": "Granular analysis of this specific diverging narrative..."
            }}
        ]
    }}
}}

Rules:

- Extract 8-12 particles total.
- "type" must be either "consensus" or "contradiction".
- "bias_score" must be a float between 0.0 (Neutral) and 1.0 (Highly Loaded/Partisan).
- NO literal newlines inside strings.
- Output raw JSON only.
- NO markdown.

Context:

{context}
"""

    response = model.generate_content(
        prompt,
        generation_config={
            "response_mime_type": "application/json",
            "max_output_tokens": 8192,
            "temperature": 0.2,
        },
    )

    generated_info = response.text.strip()

    json_match = re.search(
        r"({.*})",
        generated_info,
        re.DOTALL,
    )

    refined_json = (
        json_match.group(1)
        if json_match
        else generated_info
    )

    refined_json = "".join(
        char
        for char in refined_json
        if ord(char) >= 32 or char in "\n\r\t"
    )

    # Remaining JSON cleanup continues here in the original code.


components.html(
    html_code,
    height=620,
)


if st.button("Initialize Logic Audit"):
    if not event.strip():
        st.warning("Query required.")

    else:
        status_container = st.empty()

        try:
            with status_container.status(
                "Deploying Dissonance Engine...",
                expanded=True,
            ) as status:

                st.write("Scanning global intelligence sources...")
                info = call_tavily_api(event)

                st.write("Engine synthesising Pulse Vortex data...")
                payload = gemini_api_call(info)

                st.session_state["audit_payload"] = payload
                st.session_state["audit_info"] = info

                status.update(
                    label="Vortex Synthesis Complete",
                    state="complete",
                    expanded=False,
                )

        except Exception as e:
            status_container.error(
                f"System Halt: {str(e)}"
            )


if (
    "audit_payload" in st.session_state
    and "audit_info" in st.session_state
):
    payload = st.session_state["audit_payload"]
    info = st.session_state["audit_info"]

    summary_data = payload.get("summary", {})

    st.subheader("Narrative Pulse Vortex")

    st.info(
        "🖱️ **Interaction:** Hover over particles for haptic response. "
        "Click the map to **Freeze** orbital flow. "
        "Click particles to view intelligence metadata."
    )

    vortex(payload)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🟢 Consensus Data Stream")

        claims = summary_data.get("common_claims", [])

        if claims:
            for claim in claims:
                st.markdown(
                    f"""
                    ### ✓ {claim.get("title", "Verified Claim")}

                    {claim.get(
                        "detail",
                        "No detailed analysis provided.",
                    )}
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.write("No major consensus detected in the data stream.")

    with col2:
        st.subheader("🔴 Dissonance & Contradictions")

        contradictions = summary_data.get("contradictions", [])

        if contradictions:
            for contradiction in contradictions:
                st.markdown(
                    f"""
                    ### ⚠ {contradiction.get(
                        "title",
                        "Logical Conflict",
                    )}

                    {contradiction.get(
                        "detail",
                        "No detailed analysis provided.",
                    )}
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.write(
                "No major contradictions detected. "
                "The narrative is stable."
            )

    st.markdown("---")
    st.subheader("Verified Data Ledger")

    particle_map = {}

    for particle in payload.get("particles", []):
        source_key = str(
            particle.get("source", "")
        ).strip().lower()

        particle_map[source_key] = particle

    for item in info:
        tavily_source_name = (
            item["title"]
            .split("|")[0]
            .strip()
            .lower()
        )

        matched_particle = particle_map.get(
            tavily_source_name,
            {},
        )

        bias_score = float(
            matched_particle.get(
                "bias_score",
                0.15,
            )
        )

        bias_label = matched_particle.get(
            "bias_label",
            "Standardised",
        )

        bias_pct = bias_score * 100

        bar_color = (
            "#3b82f6"
            if bias_pct < 40
            else "#f59e0b"
            if bias_pct < 70
            else "#ef4444"
        )

        with st.expander(
            f"Source: {item['title']}"
        ):
            st.caption(
                f"URL: {item['url']}"
            )

            st.markdown("Linguistic Bias:")

            st.markdown(
                f"""
                <!-- Bias visualization belongs here -->
                """,
                unsafe_allow_html=True,
            )

            st.write(item["content"])
```
