import json
import re
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from tavily import TavilyClient

st.set_page_config(
    layout="wide",
    page_title="Dissonance Engine",
    initial_sidebar_state="expanded",
)

TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
AI_ENGINE_KEY = st.secrets["AI_ENGINE_KEY"]
GEMINI_MODEL = st.secrets.get("GEMINI_MODEL", "gemini-3.7-flash")

with st.sidebar:
    st.markdown("### System Telemetry\n---")
    st.write("🟢 **Data Fetcher:** Active")
    st.write("🟢 **AI Engine:** Operational")
    st.write("🟢 **Render Engine:** WebGL Adaptive Chroma")
    st.markdown("---")
    st.caption("Vortex Legend:")
    st.markdown("🔴 CONTRADICTION (Turbulence)", unsafe_allow_html=True)
    st.markdown("🟢 CONSENSUS (Smooth Flow)", unsafe_allow_html=True)
    st.markdown("---")
    st.info(
        "🖱️ **Vortex Control:** Hover to feel particle mass. "
        "Click the map to freeze/unfreeze flow. "
        "Red particles will continue to vibrate."
    )


st.title("Dissonance Engine")

st.markdown(
    "Real-time fluid dynamic audit of global narrative logical structures.",
    unsafe_allow_html=True,
)


event = st.text_input(
    "Target Subject / Event",
    placeholder="Enter geopolitical event or global narrative to analyse...",
)


@st.cache_data(ttl=3600)
def calltavilyapi(query):
    tavily = TavilyClient(api_key=TAVILY_API_KEY)

    response = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=6,
    )

    results = response.get("results", [])

    if not results:
        raise ValueError("No verified news sources found.")

    return results


def extract_json(text):
    text = text.strip()

    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")

    if start == -1:
        raise ValueError("Gemini returned no JSON object.")

    depth = 0
    in_string = False
    escaped = False

    for index in range(start, len(text)):
        char = text[index]

        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1

            if depth == 0:
                return json.loads(text[start:index + 1])

    raise ValueError("Gemini returned incomplete JSON.")


@st.cache_data(ttl=3600)
def geminiapicall(reports6):
    client = genai.Client(api_key=AI_ENGINE_KEY)

    context = "\n".join(
        f"[{report.get('title', 'Unknown Source')} | "
        f"{report.get('url', '')}] - "
        f"{report.get('content', '')}"
        for report in reports6
    )

    prompt = f"""[SYSTEM PROTOCOL: DISSONANCE ENGINE]

Analyze the supplied news material for logical consensus, contradiction, and linguistic bias.

Critical requirements:

1. The particles must visually reflect the summary.
2. Every contradiction identified in the summary must have corresponding contradiction particles.
3. Divide the analysis into distinct claims rather than one broad overview.
4. Use only evidence present in the supplied sources.
5. Do not invent publishers, claims, or URLs.

Return JSON only in exactly this structure:

{{
  "particles": [
    {{
      "id": "p1",
      "type": "consensus",
      "name": "Short Topic",
      "description": "Short detail under 200 characters.",
      "source": "Publisher Name",
      "bias_score": 0.2,
      "bias_label": "Neutral"
    }}
  ],
  "summary": {{
    "common_claims": [
      {{
        "title": "Distinct Consensus",
        "detail": "Specific structural breakdown with evidence."
      }}
    ],
    "contradictions": [
      {{
        "title": "Distinct Conflict",
        "detail": "Specific explanation of the diverging narratives."
      }}
    ]
  }}
}}

Rules:
- Extract 8-12 particles total.
- "type" must be exactly "consensus" or "contradiction".
- "bias_score" must be between 0.0 and 1.0.
- Keep particle descriptions under 200 characters.
- No markdown.
- No commentary outside the JSON.

Context:

{context}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "temperature": 0.2,
            "max_output_tokens": 8192,
        },
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    payload = extract_json(response.text)

    if not isinstance(payload, dict):
        raise ValueError("Invalid Gemini response structure.")

    payload.setdefault("particles", [])
    payload.setdefault("summary", {})
    payload["summary"].setdefault("common_claims", [])
    payload["summary"].setdefault("contradictions", [])

    return payload


def vortex(payload):
    particles = []

    for index, particle in enumerate(payload.get("particles", [])):
        particles.append({
            "id": particle.get("id", f"p{index + 1}"),
            "type": particle.get("type", "consensus"),
            "name": particle.get("name", "Unknown Topic"),
            "description": particle.get("description", ""),
            "source": particle.get("source", "Unknown Source"),
            "bias_score": float(particle.get("bias_score", 0.15)),
            "bias_label": particle.get("bias_label", "Standardised"),
        })

    particle_json = json.dumps(particles).replace("</", "<\\/")

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
                background: #05070c;
                font-family: Inter, Arial, sans-serif;
            }}

            canvas {{
                display: block;
                width: 100%;
                height: 620px;
                cursor: crosshair;
            }}

            #info {{
                position: absolute;
                display: none;
                pointer-events: none;
                max-width: 260px;
                padding: 12px;
                border: 1px solid rgba(255,255,255,.16);
                border-radius: 10px;
                background: rgba(8,10,18,.94);
                color: #fff;
                font-size: 12px;
                line-height: 1.45;
                box-shadow: 0 12px 30px rgba(0,0,0,.35);
            }}

            #info strong {{
                display: block;
                margin-bottom: 5px;
                font-size: 13px;
            }}
        </style>
    </head>

    <body>
        <canvas id="vortex"></canvas>
        <div id="info"></div>

        <script>
            const canvas = document.getElementById("vortex");
            const ctx = canvas.getContext("2d");
            const info = document.getElementById("info");
            const sourceParticles = {particle_json};

            let frozen = false;
            let hovered = null;
            let particles = [];

            function resize() {{
                const ratio = window.devicePixelRatio || 1;

                canvas.width = canvas.clientWidth * ratio;
                canvas.height = canvas.clientHeight * ratio;

                ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
            }}

            function createParticles() {{
                particles = [];

                sourceParticles.forEach((particle, index) => {{
                    const angle =
                        (index / Math.max(sourceParticles.length, 1))
                        * Math.PI * 2;

                    const radius = 120 + Math.random() * 120;

                    particles.push({{
                        ...particle,
                        x: canvas.clientWidth / 2 + Math.cos(angle) * radius,
                        y: 310 + Math.sin(angle) * radius * 0.7,
                        baseX: canvas.clientWidth / 2 + Math.cos(angle) * radius,
                        baseY: 310 + Math.sin(angle) * radius * 0.7,
                        vx: 0,
                        vy: 0,
                        phase: Math.random() * Math.PI * 2,
                        radius: 5 + Math.random() * 4
                    }});
                }});
            }}

            function updateParticle(particle) {{
                const contradiction = particle.type === "contradiction";
                const time = performance.now() * 0.001;

                if (!frozen || contradiction) {{
                    if (contradiction) {{
                        particle.phase += 0.13;
                        particle.x += Math.sin(particle.phase * 2.1) * 0.9;
                        particle.y += Math.cos(particle.phase * 1.7) * 0.9;
                    }} else {{
                        particle.phase += 0.008;
                    }}

                    const orbit =
                        0.2 + Math.sin(time * 0.7 + particle.phase) * 0.08;

                    particle.vx +=
                        (particle.baseX - particle.x) * 0.0015;

                    particle.vy +=
                        (particle.baseY - particle.y) * 0.0015;

                    particle.x +=
                        particle.vx +
                        Math.cos(time + particle.phase) * orbit;

                    particle.y +=
                        particle.vy +
                        Math.sin(time + particle.phase) * orbit;

                    particle.vx *= 0.985;
                    particle.vy *= 0.985;
                }}
            }}

            function drawParticle(particle) {{
                const contradiction =
                    particle.type === "contradiction";

                const active = hovered === particle;
                const size = active
                    ? particle.radius * 1.8
                    : particle.radius;

                const gradient = ctx.createRadialGradient(
                    particle.x,
                    particle.y,
                    0,
                    particle.x,
                    particle.y,
                    size * 4
                );

                gradient.addColorStop(
                    0,
                    contradiction
                        ? "rgba(239,68,68,1)"
                        : "rgba(120,190,255,1)"
                );

                gradient.addColorStop(
                    0.35,
                    contradiction
                        ? "rgba(239,68,68,.45)"
                        : "rgba(120,190,255,.28)"
                );

                gradient.addColorStop(1, "rgba(0,0,0,0)");

                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(
                    particle.x,
                    particle.y,
                    size * 4,
                    0,
                    Math.PI * 2
                );
                ctx.fill();

                ctx.fillStyle = contradiction
                    ? "#ef4444"
                    : "#78beff";

                ctx.beginPath();
                ctx.arc(
                    particle.x,
                    particle.y,
                    size,
                    0,
                    Math.PI * 2
                );
                ctx.fill();
            }}

            function drawConnections() {{
                for (let i = 0; i < particles.length; i++) {{
                    for (let j = i + 1; j < particles.length; j++) {{
                        const a = particles[i];
                        const b = particles[j];

                        const dx = a.x - b.x;
                        const dy = a.y - b.y;
                        const distance = Math.sqrt(dx * dx + dy * dy);

                        if (distance > 210) continue;

                        const alpha = (1 - distance / 210) * 0.12;

                        ctx.strokeStyle =
                            a.type === "contradiction" ||
                            b.type === "contradiction"
                                ? `rgba(239,68,68,${{alpha}})`
                                : `rgba(120,190,255,${{alpha}})`;

                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(a.x, a.y);
                        ctx.lineTo(b.x, b.y);
                        ctx.stroke();
                    }}
                }}
            }}

            function particleAt(x, y) {{
                return particles.find(particle => {{
                    const dx = particle.x - x;
                    const dy = particle.y - y;
                    return Math.sqrt(dx * dx + dy * dy) < 18;
                }});
            }}

            function render() {{
                ctx.clearRect(
                    0,
                    0,
                    canvas.clientWidth,
                    canvas.clientHeight
                );

                ctx.fillStyle = "#05070c";
                ctx.fillRect(
                    0,
                    0,
                    canvas.clientWidth,
                    canvas.clientHeight
                );

                drawConnections();

                particles.forEach(updateParticle);
                particles.forEach(drawParticle);

                requestAnimationFrame(render);
            }}

            canvas.addEventListener("mousemove", event => {{
                const rect = canvas.getBoundingClientRect();
                const x = event.clientX - rect.left;
                const y = event.clientY - rect.top;

                hovered = particleAt(x, y);

                if (!hovered) {{
                    info.style.display = "none";
                    return;
                }}

                info.innerHTML = `
                    <strong>${{hovered.name}}</strong>
                    ${{hovered.description}}<br><br>
                    <b>Source:</b> ${{hovered.source}}<br>
                    <b>Bias:</b> ${{hovered.bias_label}}
                    (${{hovered.bias_score.toFixed(2)}})
                `;

                info.style.display = "block";
                info.style.left =
                    `${{Math.min(x + 18, canvas.clientWidth - 280)}}px`;

                info.style.top =
                    `${{Math.min(y + 18, canvas.clientHeight - 150)}}px`;
            }});

            canvas.addEventListener("mouseleave", () => {{
                hovered = null;
                info.style.display = "none";
            }});

            canvas.addEventListener("click", event => {{
                const rect = canvas.getBoundingClientRect();
                const x = event.clientX - rect.left;
                const y = event.clientY - rect.top;

                const clicked = particleAt(x, y);

                if (clicked) {{
                    hovered = clicked;
                    return;
                }}

                frozen = !frozen;
            }});

            window.addEventListener("resize", () => {{
                resize();
                createParticles();
            }});

            resize();
            createParticles();
            render();
        </script>
    </body>
    </html>
    """

    components.html(html_code, height=620)


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
                info = calltavilyapi(event)

                st.write("Engine synthesising Pulse Vortex data...")
                payload = geminiapicall(info)

                st.session_state["audit_payload"] = payload
                st.session_state["audit_info"] = info

                status.update(
                    label="Vortex Synthesis Complete",
                    state="complete",
                    expanded=False,
                )

        except Exception as e:
            status_container.error(f"System Halt: {e}")


if "audit_payload" in st.session_state and "audit_info" in st.session_state:
    payload = st.session_state["audit_payload"]
    info = st.session_state["audit_info"]
    summary_data = payload.get("summary", {})

    st.subheader("Narrative Pulse Vortex")

    st.info(
        "🖱️ **Interaction:** Hover over particles for metadata. "
        "Click empty space to **Freeze/Unfreeze** orbital flow. "
        "Contradiction particles continue vibrating."
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
                    f"**✓ {claim.get('title', 'Verified Claim')}**\n\n"
                    f"{claim.get('detail', 'No detailed analysis provided.')}"
                )
        else:
            st.write("No major consensus detected in the data stream.")

    with col2:
        st.subheader("🔴 Dissonance & Contradictions")
        contradictions = summary_data.get("contradictions", [])

        if contradictions:
            for contradiction in contradictions:
                st.markdown(
                    f"**⚠ {contradiction.get('title', 'Logical Conflict')}**\n\n"
                    f"{contradiction.get('detail', 'No detailed analysis provided.')}"
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
        source_title = item.get("title", "Unknown Source")
        source_name = source_title.split("|")[0].strip().lower()

        matched_particle = particle_map.get(source_name, {})

        bias_score = float(
            matched_particle.get("bias_score", 0.15)
        )

        bias_label = matched_particle.get(
            "bias_label",
            "Standardised",
        )

        with st.expander(f"Source: {source_title}"):
            st.caption(f"URL: {item.get('url', '')}")
            st.write(
                f"**Linguistic Bias:** {bias_label} "
                f"({bias_score:.2f})"
            )
            st.write(
                item.get(
                    "content",
                    "No source content available.",
                )
            )
