import streamlit as st
from groq import Groq

# --- APP CONFIG ---
st.set_page_config(
    page_title="TATU AI - Tamale AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM APP CSS (Makes it look like real app, not website) ---
st.markdown("""
<style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    #MainMenu {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 5rem;}
    .stChatMessage {border-radius: 15px; padding: 10px;}
    h1 {text-align: center; font-size: 28px !important;}
</style>
""", unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

KNOWLEDGE = """You are TATU AI v10 - Official AI of Tamale Technical University, built by Manaf aka Popcaan de Unruly Boss.
GLOBAL: You know everything. 
LOCAL (Tamale, Ghana):
- TaTU = Tamale Technical University, Education Ridge.
- UDS = University for Development Studies.
- Languages: Dagbani basics, Ghana Pidgin, Twi.
- New Life College = Private SHS at Vittin, Tamale.
- Buy computer: Aboabo, Lamashegu near Melcom, Central Market.
- Answer with Ghana examples. Be concise, friendly, helpful for BTech students.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"Dasiba! 🧠 I'm TATU AI v10 - your Tamale + Global brain. Ask me anything!"}]

st.title("TATU AI v10 🧠🔥🇬🇭")
st.caption("Built by Manaf | TaTU BTech | Global + Tamale Heart")

# Chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Voice + Image in nice expander (App style)
with st.expander("📸 🎤 Tools"):
    up = st.file_uploader("Upload image/question", type=["png","jpg","jpeg"])
    if up: st.image(up, use_column_width=True)
    audio = st.audio_input("Tap to speak")
    if audio and client:
        try:
            t = client.audio.transcriptions.create(file=("voice.wav", audio.getvalue()), model="whisper-large-v3-turbo", response_format="text")
            st.session_state.voice_prompt = t
            st.success(f"You said: {t}")
        except Exception as e:
            st.error(f"{e}")

prompt = st.chat_input("Ask TATU anything...")
if "voice_prompt" in st.session_state:
    prompt = st.session_state.voice_prompt
    del st.session_state.voice_prompt

if prompt and client:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    msgs = [{"role":"system","content":KNOWLEDGE}]
    for x in st.session_state.messages[-10:]:
        msgs.append({"role":x["role"],"content":x["content"]})
    with st.chat_message("assistant"):
        try:
            r = client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs, max_tokens=2000)
            ans = r.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role":"assistant","content":ans})
        except Exception as e:
            st.error(f"Error: {e}")

# Sidebar for app info
with st.sidebar:
    st.title("TATU AI App")
    st.write("Version 10.0 - App Edition")
    st.write("By Manaf aka Popcaan de Unruly Boss")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()