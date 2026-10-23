import streamlit as st
from groq import Groq

st.set_page_config(page_title="TATU AI v9.1", page_icon="🧠", layout="wide")

api_key = st.secrets.get("GROQ_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = Groq(api_key=api_key) if api_key else None

st.title("TATU AI v9.1 🧠🔥🌍🇬🇭")

if client:
    st.success("GLOBAL BRAIN + TAMALE HEART ACTIVE!")
else:
    st.warning("Add GROQ_API_KEY in Secrets")

KNOWLEDGE = """
You are TATU AI v9.1 built by Manaf aka Popcaan de Unruly Boss, TaTU BTech.
GLOBAL BRAIN: You know everything worldwide.
TAMALE BRAIN:
- TaTU = Tamale Technical University, Education Ridge, Tamale.
- UDS = University for Development Studies, Tamale, Ghana (founded 1992).
- Dagbani greetings: Dasiba=Good morning, Ti puhiya=Thank you.
- New Life College = Private SHS/College near Vittin, Tamale for WASSCE remedial.
- Computer shops in Tamale: Aboabo Market (affordable/2nd hand), Lamashegu Road near Melcom/Zepto, Central Market for accessories/repairs.
- Foods: Tuo Zaafi (TZ), Banku, Jollof. Transport: Mahama Camboo motorbikes.
RULE: When user says UDS in Ghana context, always mean University for Development Studies. Be friendly, use small pidgin if user uses it.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Menu")
    if st.session_state.messages:
        txt = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        st.download_button("💾 Save Chat", txt)
        if st.button("🗑️ Clear"):
            st.session_state.messages = []
            st.rerun()
    up = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
    if up: st.image(up, use_column_width=True)
    audio = st.audio_input("Voice")
    if audio and client:
        try:
            t = client.audio.transcriptions.create(file=("voice.wav", audio.getvalue()), model="whisper-large-v3-turbo", response_format="text")
            st.success(f"You said: {t}")
            st.session_state.voice_prompt = t
        except Exception as e:
            st.error(f"Voice error: {e}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Ask anything...")
if "voice_prompt" in st.session_state:
    prompt = st.session_state.voice_prompt
    del st.session_state.voice_prompt

if prompt and client:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    msgs = [{"role": "system", "content": KNOWLEDGE}]
    for x in st.session_state.messages[-8:]:
        msgs.append({"role": x["role"], "content": x["content"]})
    with st.chat_message("assistant"):
        try:
            r = client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs, max_tokens=2000)
            ans = r.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Error: {e}")