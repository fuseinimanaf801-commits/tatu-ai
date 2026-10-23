import streamlit as st
from groq import Groq

st.set_page_config(page_title="TATU AI v7.1", page_icon="🧠", layout="wide")

api_key = st.secrets.get("GROQ_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = Groq(api_key=api_key) if api_key else None
brain_active = client is not None

st.title("TATU AI v7.1 🧠🔥")
if brain_active:
    st.success("BRAIN ACTIVE! Voice + Image Ready!")
else:
    st.warning("Add API Key")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("v7.1 Controls")
    if st.session_state.messages:
        chat_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        st.download_button("💾 Save Chat", chat_text)
        if st.button("🗑️ Clear"):
            st.session_state.messages = []
            st.rerun()
    uploaded_image = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
    if uploaded_image:
        st.image(uploaded_image, use_column_width=True)
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

if prompt and brain_active:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    msgs = [{"role": "system", "content": "You are TATU AI v7.1 by Manaf aka Popcaan de Unruly Boss. Helpful TaTU tutor."}]
    for x in st.session_state.messages[-10:]:
        msgs.append({"role": x["role"], "content": x["content"]})
    with st.chat_message("assistant"):
        try:
            r = client.chat.completions.create(model="llama-3.1-8b-instant", messages=msgs, max_tokens=2000)
            ans = r.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Error: {e}")