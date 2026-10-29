import streamlit as st
from groq import Groq
import re
import requests
from duckduckgo_search import DDGS

st.set_page_config(page_title="TATU AI V21 Google Brain", page_icon="🔍", layout="centered")

st.markdown("""
<style>
header,footer,#MainMenu{visibility:hidden;}
.block-container{padding-top:1rem; padding-bottom:7rem;}
.link-card{border:1px solid #2a2a2a;background:#151515;padding:12px 16px;border-radius:14px;margin:6px 0;display:flex;gap:12px;align-items:center;}
.link-card:hover{border-color:#4285F4;background:#1f1f1f;}
.link-card-icon{font-size:22px;}
.link-card-title{font-weight:700;color:#fff;font-size:13px;}
.link-card-url{font-size:11px;color:#888;max-width:260px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
</style>
""", unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# --- GOOGLE BRAIN FUNCTION ---
def google_brain_search(query, max_results=5):
    results_text = ""
    links = []
    try:
        # Use DuckDuckGo free - behaves like Google
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=max_results))
            for r in search_results:
                title = r.get('title','')
                body = r.get('body','')
                href = r.get('href','')
                if href:
                    links.append(href)
                    results_text += f"- {title}: {body} | URL: {href}\n"
    except Exception as e:
        results_text = f"Search failed: {e}"
    
    # Fallback: also try official Ghana domains
    if "wassce" in query.lower() or "waec" in query.lower():
        links.extend(["https://www.waecgh.org", "https://gh.waecdirect.org"])
    if "kalpohin" in query.lower():
        links.extend(["https://en.wikipedia.org/wiki/Kalpohin_Senior_High_School", "https://ges.gov.gh"])
    
    return results_text, list(dict.fromkeys(links))[:5] # dedup

def extract_links(text):
    urls = re.findall(r'https?://[^\s\)\]\"\<]+', text)
    seen=set(); uniq=[]
    for u in urls:
        u=u.rstrip('.,;')
        k=u.lower().split('?')[0].rstrip('/')
        if k not in seen:
            seen.add(k); uniq.append(u)
    return uniq[:6]

def render_cards(urls):
    if not urls: return
    st.markdown("### 🔍 Google Brain Sources (Live Search)")
    for url in urls:
        domain = url.replace("https://","").replace("http://","").split("/")[0]
        short = url[:70]
        st.markdown(f"""<a href="{url}" target="_blank"><div class="link-card"><div class="link-card-icon">🌐</div><div><div class="link-card-title">{domain}</div><div class="link-card-url">{short}</div></div></div></a>""", unsafe_allow_html=True)

SYSTEM_V21 = """
You are TATU AI V21 GOOGLE BRAIN - Final Edition, built by Manaf, BTech IT, Tamale Technical University, Ghana.

You have TWO brains:
1. Groq 120B global brain (ChatGPT-level)
2. GOOGLE BRAIN - live search results provided below

RULES:
- If LIVE SEARCH RESULTS are provided, USE THEM FIRST. Do not invent.
- For Kalpohin SHS: motto is Discipline and Hard Work per live search, founded 1987, nickname KALISCO, Category B, mixed, Kalpohin Estates Tamale. Never invent P.O. Box or phone.
- For WASSCE: Use waecgh.org live links
- Ghana technical universities = exactly 10: ATU, Bolgatanga TU, CCTU, Dr. Hilla Limann TU, HTU, KTU, KsTU, STU, TTU, TATU. No Jamaica.
- Mobile-friendly: Use bullets, bold headings, not wide tables
- Provide max 4 unique official links at end
- Truth first: If not sure, say check official ges.gov.gh / waecgh.org
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"🔍 Hello! I am TATU AI V21 Google Brain Edition, built by Manaf — BTech IT, TATU Ghana. I now search live like Google + ChatGPT brain. Ask me anything — SHS motto, WASSCE, coding, Harvard, anything!"}]

st.caption("TATU AI V21 Google Brain 🌍 | Built by Manaf | Live Search + ChatGPT Brain | Final Paid Edition 💎")
st.title("TATU AI V21 - Google Brain 🔍")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"], unsafe_allow_html=True)

prompt = st.chat_input("Ask with Google Brain...")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🔍 Google Brain dey search live..."):
            live_text, live_links = google_brain_search(prompt, max_results=5)
        
        with st.spinner("🧠 Brain dey think with Google results..."):
            # Build prompt with live search
            search_context = f"\nLIVE GOOGLE SEARCH RESULTS FOR QUERY: '{prompt}'\n{live_text}\n\nINSTRUCTION: Use these live results to answer. Cite URLs. If motto/search says Discipline and Hard Work, use that, not invent.\n"
            
            msgs = [{"role":"system","content":SYSTEM_V21 + search_context}] + [{"role":x["role"],"content":x["content"]} for x in st.session_state.messages[-10:]]
            
            resp = client.chat.completions.create(model="openai/gpt-oss-120b", messages=msgs, max_tokens=3500, temperature=0.2)
            ans = resp.choices[0].message.content
            
            st.markdown(ans, unsafe_allow_html=True)
            
            # Combine live links + links from answer
            all_links = live_links + extract_links(ans)
            all_links = list(dict.fromkeys(all_links))[:5]
            if all_links:
                render_cards(all_links)
            
            st.session_state.messages.append({"role":"assistant","content":ans})

with st.sidebar:
    st.title("V21 Google Brain")
    st.success("🔍 Live Search: ON")
    st.write("✅ No fake motto")
    st.write("✅ Live links like Google")
    st.write("✅ Global brain + Ghana truth")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()