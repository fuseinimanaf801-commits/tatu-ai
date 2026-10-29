import streamlit as st
from groq import Groq
import re

st.set_page_config(page_title="TATU AI V17", page_icon="🌍", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
header{visibility:hidden;}footer{visibility:hidden;}#MainMenu{visibility:hidden;}
.block-container{padding-top:1rem; padding-bottom:6rem;}
a {text-decoration:none !important; color:#60A5FA !important;}
.link-card {border:1px solid #2a2a2a; background:#151515; padding:12px 16px; border-radius:14px; margin:6px 0; display:flex; gap:12px; align-items:center;}
.link-card:hover {border-color:#60A5FA; background:#1f1f1f;}
.link-card-icon {font-size:22px;}
.link-card-title {font-weight:700; color:#fff; font-size:13px;}
.link-card-url {font-size:11px; color:#888; max-width:260px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;}
/* Make tables scrollable on mobile */
div[data-testid="stMarkdownContainer"] table {display:block; overflow-x:auto; white-space:nowrap;}
/* Step cards */
.step-box {border:1px solid #2a2a2a; background:#121212; padding:14px; border-radius:12px; margin:8px 0;}
</style>
""", unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def extract_unique_links(text):
    urls = re.findall(r'https?://[^\s\)\]\"\<]+', text)
    # clean and dedup by domain+path
    seen = set()
    unique = []
    for u in urls:
        u = u.rstrip('.,;')
        key = u.lower().split('?')[0].rstrip('/')
        if key not in seen:
            seen.add(key)
            unique.append(u)
    return unique[:5]

def render_link_cards(urls):
    if not urls: return
    st.markdown("### 🔗 Official Sources & Links")
    for url in urls:
        domain = url.replace("https://","").replace("http://","").split("/")[0]
        short = url[:65]
        st.markdown(f"""<a href="{url}" target="_blank"><div class="link-card"><div class="link-card-icon">🌐</div><div><div class="link-card-title">{domain}</div><div class="link-card-url">{short}</div></div></div></a>""", unsafe_allow_html=True)

SYSTEM_V17 = """
You are TATU AI V17 Premium - Created by Manaf, BTech IT, Tamale Technical University, Ghana. World AI.

IMPROVEMENT INSTRUCTIONS FOR V17:
1. MOBILE FRIENDLY: Don't use wide 3-column markdown tables that cut off on phone. Instead use:
   - Numbered steps with bold headings
   - Or 2-column tables max
   - Use bullet points for details
   Example GOOD:
   **Step 1: Verify official portal**
   Go to https://www.waecgh.org - official WAEC Ghana.
   
   BAD: | Step | What to Do | Details | - too wide, cuts on phone.

2. NO LINK DUPLICATION: Provide max 3-4 UNIQUE official links. Don't repeat same domain 4 times. Use:
   - https://www.waecgh.org
   - https://www.waecgh.org/result-checker (online)
   - https://www.waecgh.org/sms-result-checker (if exists) or contact page
   Not 4x same.

3. PRACTICAL & GHANA FOCUSED for WASSCE/WAEC: Give exact SMS format: Example: WASSCE*2024*1234567890*... etc if known, else say check site. Give PIN/serial advice, scam warning.

4. GLOBAL BRAIN still: Can answer ChatGPT, coding, business, religion, top world universities, everything worldwide.

5. TRUTH RULES: No fake fees, no inventing. For live/today: say check official. Ghana tech universities = 10 exactly: ATU, Bolgatanga TU, CCTU, Dr. Hilla Limann TU, HTU, KTU, KsTU, STU, TTU, TATU. No Jamaica. No duplicate uni. Islamic terms correct: At-Tawhid, Al-Mala'ikah, Al-Kutub, Ar-Rusul, Al-Yawm al-Akhir, Al-Qadar.

6. At end of answer, add 2-4 official links max, unique.

INTRO: "Hello! I am TATU AI V17, created by Manaf — BTech IT, Tamale Technical University, Ghana. Improved for mobile & premium links. How can I help?"

Be concise, mobile-friendly, premium.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am TATU AI V17, created by Manaf — BTech IT, Tamale Technical University, Ghana. Improved for mobile & premium links. How can I help you today?"}]

st.caption("Built by Manaf | TATU BTech | V17 Improved - Mobile + No Duplicate Links 💎")
st.title("TATU AI Global V17 🌍")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"], unsafe_allow_html=True)

prompt = st.chat_input("Ask anything...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    msgs = [{"role": "system", "content": SYSTEM_V17}] + [{"role": x["role"], "content": x["content"]} for x in st.session_state.messages[-12:]]
    with st.chat_message("assistant"):
        with st.spinner("V17 dey think..."):
            resp = client.chat.completions.create(model="openai/gpt-oss-120b", messages=msgs, max_tokens=3200, temperature=0.2)
            ans = resp.choices[0].message.content
            st.markdown(ans, unsafe_allow_html=True)
            urls = extract_unique_links(ans)
            if urls:
                render_link_cards(urls)
            st.session_state.messages.append({"role": "assistant", "content": ans})

with st.sidebar:
    st.title("V17 Change Log")
    st.write("✅ Fixed duplicate links")
    st.write("✅ Fixed table cut on phone")
    st.write("✅ Mobile-friendly steps")
    st.write("✅ Cleaner premium UI")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()