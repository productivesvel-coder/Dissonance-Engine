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
def calltavilyapi(query):
    tavilycur=TavilyClient(api_key=TAVILY_API_KEY)
    response=tavilycur.search(query=query, search_depth="advanced", max_results=6)
    if not response.get('results'):
        raise ValueError("No verified news sources found.")
    return response['results']
def stabilize_vortex(raw_telemetry):
    sanitized_payload=raw_telemetry.strip()
    sanitized_payload=re.sub(r'[^}\]" \w]$', '',sanitized_payload)
    if sanitized_payload.count('"')%2!=0: 
        sanitized_payload+='"'
    integrity_stack=[]
    for char in sanitized_payload:
        if char=='{': 
            integrity_stack.append('}')
        elif char=='[': 
            integrity_stack.append(']')
        elif char in '}]':
            if integrity_stack and integrity_stack[-1]==char: 
                integrity_stack.pop()
    return sanitized_payload+"".join(reversed(integrity_stack))
def geminiapicall(reports6):
    gem.configure(api_key=AI_ENGINE_KEY)
    model=gem.GenerativeModel('gemini-3.5-flash-lite')
    context="\n".join([f"[{r['title']} | {r['url']}] - {r['content']}" for r in reports6])
    prompt=f"""
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
    response=model.generate_content(prompt, generation_config={"response_mime_type": "application/json", "max_output_tokens": 8192, "temperature": 0.2})
    generatedinf=response.text.strip()
    json_match=re.search(r'(\{.*\})', generatedinf, re.DOTALL)
    refi=json_match.group(1) if json_match else generatedinf
    refi="".join(char for char in refi if ord(char) >= 32 or char in "\n\r\t")
    refi=re.sub(r'(?<!\\)\n', ' ',refi)
    try:
        data=json.loads(refi, strict=False)
    except json.JSONDecodeError:
        try:
            data=json.loads(stabilise_vortex(refi), strict=False)
        except Exception:
            data={"particles": [], "summary": {"common_claims": [], "contradictions": [{"title": "Data Parse Error", "detail": "AI output structure failed."}]}}
    return data
    
def vortex(vortex_data):
    particles=vortex_data.get("particles", [])
    vortex_json=json.dumps(particles)
    # calculating Dissonance Ratio(0.0 to 1.0) for colour of the particle which would be green/red
    contra_count=sum(1 for p in particles if p.get('type') == 'contradiction')
    ratio=contra_count / len(particles) if particles else 0.0
    html_code=f"""
    <div id="graph-wrapper" style="position: relative; border-radius: 12px; background: #05080F; overflow: hidden; height: 600px; border: 1px solid #1e293b;">
        <div id="info-panel" style="position: absolute; top: 15px; right: 15px; width: 320px; background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(10px); color: white; padding: 20px; border-radius: 12px; display: none; border: 1px solid #334155; z-index: 100; font-family: 'Inter', sans-serif;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h3 id="info-title" style="margin: 0; color: #60a5fa; font-size: 18px; line-height: 1.2;"></h3>
                <span id="info-badge" style="font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: bold; text-transform: uppercase;"></span>
            </div>
            <hr style="border: 0; border-top: 1px solid #334155; margin: 0 0 12px 0;">
            <div id="info-content"></div>
        </div>
        <div id="vortex" style="width: 100%; height: 100%; cursor: crosshair;"></div>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    
    <script>
      window.onload=function() {{
          const pData={vortex_json};
          const disRatio={ratio};
          const elem=document.getElementById('vortex');
          let isPaused=false;
          
          // Scene Setup
          const scene=new THREE.Scene();
          
          // Adaptive Chroma: Interpolate between Deep Teal and Bruised Purple
          const colorStable=new THREE.Color(0x002b2d);
          const colorChaos=new THREE.Color(0x2e004f);
          const bgColor=colorStable.clone().lerp(colorChaos, disRatio);
          scene.background=bgColor;
          scene.fog=new THREE.FogExp2(bgColor, 0.015);
          
          const camera=new THREE.PerspectiveCamera(60, elem.clientWidth / elem.clientHeight, 0.1, 1000);
          camera.position.set(0, 30, 60);
          
          const renderer=new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
          renderer.setSize(elem.clientWidth, elem.clientHeight);
          renderer.setPixelRatio(window.devicePixelRatio);
          elem.appendChild(renderer.domElement);
          
          const controls=new THREE.OrbitControls(camera, renderer.domElement);
          controls.enableDamping = true;
          controls.dampingFactor = 0.05;
          controls.autoRotate = true;
          controls.autoRotateSpeed = 1.0;
          
          // Core Vortex Pillar
          const coreGeo=new THREE.CylinderGeometry(0.5, 0.5, 100, 16);
          const coreMat=new THREE.MeshBasicMaterial({{ color: 0x1e293b, transparent: true, opacity: 0.3 }});
          const core=new THREE.Mesh(coreGeo, coreMat);
          scene.add(core);

          // Particle System
          const meshes=[];
          pData.forEach((p, i) => {{
              const isContra=p.type==='contradiction';
              const color=isContra ? 0xff003c : 0x00ff7f;
              
              const geo=new THREE.SphereGeometry(isContra ? 1.5 : 1.0, 16, 16);
              const mat=new THREE.MeshBasicMaterial({{ color: color, wireframe: isContra }});
              const mesh=new THREE.Mesh(geo, mat);
              
              mesh.userData={{
                  angle: Math.random()*Math.PI*2,
                  radius: 10 + Math.random()*25,
                  speed: (isContra ? 0.04 : 0.015)+Math.random()*0.01,
                  yOffset: (Math.random()-0.5)*40,
                  isContra: isContra,
                  info: p
              }};
              
              const glowGeo=new THREE.SphereGeometry(isContra ? 2.5 : 1.8, 16, 16);
              const glowMat=new THREE.MeshBasicMaterial({{ color: color, transparent: true, opacity: 0.2 }});
              const glow=new THREE.Mesh(glowGeo, glowMat);
              mesh.add(glow);
              
              scene.add(mesh);
              meshes.push(mesh);
          }});

          // Interaction (Raycasting & Pause Toggle)
          const raycaster=new THREE.Raycaster();
          const mouse=new THREE.Vector2();
          
          elem.addEventListener('pointermove', (event) => {{
              const rect=elem.getBoundingClientRect();
              mouse.x=((event.clientX - rect.left) / rect.width) * 2 - 1;
              mouse.y=-((event.clientY - rect.top) / rect.height) * 2 + 1;
          }});
          
          elem.addEventListener('pointerdown', (event) => {{
              // Toggle Pause logic
              isPaused = !isPaused;
              controls.autoRotate = !isPaused;

              const rect = elem.getBoundingClientRect();
              mouse.x = ((event.clientX-rect.left)/rect.width)*2-1;
              mouse.y = -((event.clientY-rect.top)/rect.height)*2+1;
              
              raycaster.setFromCamera(mouse, camera);
              const intersects=raycaster.intersectObjects(meshes);
              
              if (intersects.length>0) {{
                  const ud=intersects[0].object.userData;
                  const panel=document.getElementById('info-panel');
                  panel.style.display='block';
                  
                  document.getElementById('info-title').innerText = ud.info.name || 'Data Point';
                  const badge=document.getElementById('info-badge');
                  badge.innerText=ud.isContra ? 'Conflict' : 'Consensus';
                  badge.style.backgroundColor=ud.isContra ? 'rgba(255, 0, 60, 0.2)' : 'rgba(0, 255, 127, 0.2)';
                  badge.style.color=ud.isContra ? '#ff003c' : '#00ff7f';
                  
                  const infoText=ud.info.description || 'No detailed data available.';
                  const sourceText=ud.info.source || 'Unknown Publisher';
                  const biasLabel=ud.info.bias_label || 'Neutral';
                  
                  document.getElementById('info-content').innerHTML = `
                      <p style="font-size: 14px; line-height: 1.5; color: #e2e8f0; margin-bottom: 15px;">${{infoText}}</p>
                      <p style="font-size: 12px; color: #94a3b8; border-top: 1px dashed #334155; padding-top: 10px;">
                          <strong>Source:</strong> ${{sourceText}}<br>
                          <strong>Bias Audit:</strong> ${{biasLabel}}
                      </p>
                  `;
              }}
          }});

          // Animation Loop
          function animate() {{
              requestAnimationFrame(animate);
              
              raycaster.setFromCamera(mouse,camera);
              const hoverIntersects=raycaster.intersectObjects(meshes);
              const hoveredObj=hoverIntersects.length > 0 ? hoverIntersects[0].object : null;
              
              meshes.forEach(m => {{
                  let ud=m.userData;
                  
                  // Magnetic Haptics: Scale up and 'tug' visually when hovered
                  if (m===hoveredObj) {{
                      m.scale.lerp(new THREE.Vector3(1.6, 1.6, 1.6), 0.15);
                  }} else {{
                      m.scale.lerp(new THREE.Vector3(1, 1, 1), 0.1);
                  }}
                  
                  // Only increment angle if not paused
                  if (!isPaused) {{
                      ud.angle+=ud.speed;
                  }}
                  
                  // Base Circular Orbit (Calculated every frame to allow jitter offset)
                  let bx=Math.cos(ud.angle)*ud.radius;
                  let bz=Math.sin(ud.angle)*ud.radius;
                  let by=ud.yOffset;

                  // Apply Constant Jitter to Contradictions (even if paused)
                  if(ud.isContra) {{
                      m.position.x=bx+(Math.random()-0.5)*1.5;
                      m.position.y=by+(Math.random()-0.5)*1.5;
                      m.position.z=bz+(Math.random()-0.5)*1.5;
                  }} else {{
                      m.position.set(bx, by, bz);
                  }}
              }});
              
              controls.update();
              renderer.render(scene, camera);
          }}
          
          window.addEventListener('resize', () => {{
              camera.aspect=elem.clientWidth/elem.clientHeight;
              camera.updateProjectionMatrix();
              renderer.setSize(elem.clientWidth, elem.clientHeight);
          }});
          
          animate();
      }};
    </script>
    """
    components.html(html_code,height=620)
if st.button("Initialize Logic Audit"):
    if not event.strip():
        st.warning("Query required.")
    else:
        status_container=st.empty()
        try:
            with status_container.status(" Deploying Dissonance Engine... ", expanded=True) as status:
                st.write(" Scanning global intelligence sources... ")
                info=calltavilyapi(event)
                
                st.write(" Engine synthesising Pulse Vortex data... ")
                payload=geminiapicall(info)
                
                summary_data=payload.get("summary", {})
                
                status.update(label="Vortex Synthesis Complete", state="complete", expanded=False)
            
            #Interaction
            st.subheader("Narrative Pulse Vortex")
            st.info("🖱️ **Interaction:** Hover over particles for haptic response. Click the map to **Freeze** orbital flow. Click particles to view intelligence metadata.")
            vortex(payload)
            st.markdown("<br><hr>", unsafe_allow_html=True)
            col1, col2=st.columns(2)
            with col1:
                st.subheader("🟢 Consensus Data Stream")
                claims=summary_data.get("common_claims", [])
                if claims:
                    for claim in claims:
                        st.markdown(f"""
                            <div class="audit-card consensus-accent">
                                <div class="card-title">✓ {claim.get('title', 'Verified Claim')}</div>
                                <div class="card-detail">{claim.get('detail', 'No detailed analysis provided.')}</div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("No major consensus detected in the data stream.")    
            with col2:
                st.subheader("🔴 Dissonance & Contradictions")
                contradictions = summary_data.get("contradictions", [])
                if contradictions:
                    for contra in contradictions:
                        st.markdown(f"""
                            <div class="audit-card dissonance-accent">
                                <div class="card-title">⚠️ {contra.get('title', 'Logical Conflict')}</div>
                                <div class="card-detail">{contra.get('detail', 'No detailed analysis provided.')}</div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("No major contradictions detected. The narrative is stable.")
            
            st.markdown("---")
            st.subheader("Verified Data Ledger")
            particle_map={}
            for p in payload.get('particles', []):
                src_key=str(p.get('source', '')).strip().lower()
                particle_map[src_key] = p 
            for item in info:
                tavily_source_name=item['title'].split('|')[0].strip().lower()
                matched_particle=particle_map.get(src_key, {})
                bias_score=float(matched_particle.get('bias_score', 0.15))
                bias_label=matched_particle.get('bias_label', 'Standardised')
                bias_pct=bias_score * 100
                bar_color='#3b82f6' if bias_pct < 40 else '#f59e0b' if bias_pct < 70 else '#ef4444'
                with st.expander(f"Source: {item['title']}"):
                    st.caption(f"URL: {item['url']}")
                    #display bias
                    st.markdown(f"Linguistic Bias:")
                    st.markdown(f"""
                        <div class="bias-bar-bg">
                            <div class="bias-bar-fill" style="width: {bias_pct}%; background: {bar_color};"></div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.write(item['content'])
        except Exception as e:
            status_container.error(f"System Halt: {str(e)}")
