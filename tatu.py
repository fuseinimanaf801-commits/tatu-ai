import streamlit as st
from groq import Groq
import re

st.set_page_config(page_title="TATU AI Global V16", page_icon="🌍", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
header{visibility:hidden;}footer{visibility:hidden;}#MainMenu{visibility:hidden;}
.block-container{padding-top:1rem; padding-bottom:5rem;}
a {text-decoration:none !important; color:#60A5FA !important;}
.link-card {
    border:1px solid #333; background:#1a1a1a; padding:12px 16px; border-radius:12px; margin:8px 0;
    display:flex; align-items:center; gap:12px;
}
.link-card:hover {border-color:#60A5FA; background:#222;}
.link-card-icon {font-size:20px;}
.link-card-title {font-weight:600; color:#fff; font-size:14px;}
.link-card-url {font-size:11px; color:#888; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:250px;}
.stChatMessage a {font-weight:600;}
</style>
""", unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY missing")
    st.stop()

client = Groq(api_key=api_key)

def extract_links(text):
    url_pattern = r'https?://[^\s\)\]]+'
    return list(set(re.findall(url_pattern, text)))

def render_link_cards(urls):
    if not urls:
        return
    st.markdown("#### 🔗 Official Sources & Links")
    for url in urls[:6]:
        # clean url
        display = url.replace("https://","").replace("http://","")[:45]
        title = display.split("/")[0]
        st.markdown(f"""
        <a href="{url}" target="_blank" style="text-decoration:none;">
        <div class="link-card">
            <div class="link-card-icon">🌐</div>
            <div>
                <div class="link-card-title">{title}</div>
                <div class="link-card-url">{url[:60]}</div>
            </div>
        </div>
        </a>
        """, unsafe_allow_html=True)

GLOBAL_PROMPT_V16 = """
You are TATU AI Global V16 PREMIUM - Created by Manaf, BTech IT student, Tamale Technical University, Ghana. World AI for everyone.

MISSION: Be powerful, truthful, helpful for any user worldwide. Answer coding, science, business, religion, health, universities, everything.

POWER RULES:
- Use your 120B knowledge to answer anything globally. Don't limit to TATU.
- When explaining tech (ChatGPT, Flutter, etc), always include OFFICIAL links like:
  https://flutter.dev/docs/get-started/install
  https://firebase.google.com/docs
  https://docs.python.org/3/
  https://openai.com/index/chatgpt/
  Use real official docs only, don't invent fake links.
- At end of long answers, add a small section "Sources:" with 2-4 official links.

TRUTH RULES - ANTI-LIE (Important for paid app):
1. For specific numbers that change (fees, cut-off, salaries, live scores, live news today): Don't invent. Say "I don't have verified live 2026 figure, check official site. Cutoff early 2026."
2. Ghana technical universities: Exactly 10: ATU, Bolgatanga TU, CCTU, Dr. Hilla Limann TU, HTU, KTU, KsTU, STU, TTU, TATU. No Jamaica.
3. Ghana public core 15: UG, KNUST, UCC, UEW, UDS, UENR, UHAS, UMaT, UPSA, UESD, CKT-UTAS, SDD-UBIDS, AAMUSTED, UniMAC, GCTU.
4. No duplicate uni in list. No UWI Jamaica for Ghana questions. No UWA repeated.
5. Islamic accuracy: Arkan al-Iman: At-Tawhid, Al-Mala'ikah, Al-Kutub, Ar-Rusul/An-Nubuwwah, Al-Yawm al-Akhir, Al-Qadar. Not Al-Ubudiyyah for prophethood.
6. For France today etc: No live browsing. Say check BBC/Reuters.

STYLE:
- Friendly, senior brother style.
- Use markdown, tables, code blocks where helpful.
- Include official links that are clickable.

INTRO: "Hello! I am TATU AI Global V16, created by Manaf — BTech IT student from Tamale Technical University, Ghana. World AI with official sources and links. How can I help you today?"
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am TATU AI Global V16, created by Manaf — BTech IT student from Tamale Technical University, Ghana. World AI with official sources and links. How can I help you today?"}]

st.caption("Built by Manaf | TATU BTech | V16 Premium - Link Cards + Sources - Paid Ready 💎")
st.title("TATU AI Global 🌍\nWorld AI by Manaf")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"], unsafe_allow_html=True)

prompt = st.chat_input("Ask anything - world knowledge with links...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    msgs = [{"role": "system", "content": GLOBAL_PROMPT_V16}] + [{"role": x["role"], "content": x["content"]} for x in st.session_state.messages[-10:]]
    
    try:
        with st.chat_message("assistant"):
            with st.spinner("TATU Global V16 dey think..."):
                resp = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=msgs,
                    max_tokens=3500,
                    temperature=0.2
                )
                ans = resp.choices[0].message.content
                st.markdown(ans, unsafe_allow_html=True)
                
                # Auto link cards
                urls = extract_links(ans)
                if urls:
                    render_link_cards(urls)
                
                # Save with links extracted note
                st.session_state.messages.append({"role": "assistant", "content": ans})
    except Exception as e:
        st.error(f"Error: {e}")

with st.sidebar:
    st.title("TATU AI V16 💎")
    st.write("Model: gpt-oss-120b Global")
    st.write("Features:")
    st.write("✅ World Knowledge")
    st.write("✅ Clickable Link Cards")
    st.write("✅ Official Sources")
    st.write("✅ No Lie - Truth Mode")
    st.divider()
    st.write("Built by Manaf, Ghana")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()