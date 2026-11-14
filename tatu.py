import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="TATU AI V22", page_icon="🧠", layout="centered")

st.markdown("### TATU AI V22 Google Brain 🌍 | Built by Manaf | Live Search + ChatGPT Brain | Final Paid Edition 💎")
st.title("TATU AI V22 - Google Brain 🔍")

if "user_name" not in st.session_state:
    st.write("Welcome Boss! Enter your name")
    name = st.text_input("Your Name")
    if st.button("Enter TATU World 🚀"):
        if name:
            st.session_state.user_name = name
            st.session_state.messages = []
            st.rerun()
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

lang = st.selectbox("Choose Language / Piili Yuli:", ["English", "Pidgin", "Dagbani"])
st.caption(f"Welcome back, {st.session_state.user_name} | TATU Ghana 🇬🇭 | By Manaf")

st.write("**TATU Quick Help:**")
col1, col2, col3 = st.columns(3)
quick = ""
if col1.button("💰 Fees"):
    quick = "Tell me about TATU BTech IT fees and how to pay"
if col2.button("📚 Courses"):
    quick = "List TATU BTech IT Level 100 courses"
if col3.button("🏠 Hostel"):
    quick = "Tell me about TATU hostel in Tamale"

client = Groq(api_key=st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY")))

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

audio_value = st.audio_input("🎤 Talk to TATU")
user_prompt = None
if audio_value:
    try:
        transcription = client.audio.transcriptions.create(
            file=("voice.wav", audio_value.getvalue()),
            model="whisper-large-v3-turbo",
            response_format="text"
        )
        user_prompt = transcription
        st.info(f"You said: {user_prompt}")
    except Exception as e:
        st.error(f"Voice error: {e}")

prompt = st.chat_input("Ask with Google Brain...") or user_prompt or quick

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    lang_instruction = ""
    if lang == "Dagbani":
        lang_instruction = "Answer in Dagbani mixed with simple English. Be proud of Dagbon/Tamale."
    elif lang == "Pidgin":
        lang_instruction = "Answer in Ghana Pidgin, friendly like Charlie."
    else:
        lang_instruction = "Answer in clear simple English."

    with st.chat_message("assistant"):
        # V22.2 FIX: Try working models one by one
        MODELS = ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3.8-27b"]
        response = None
        last_error = ""
        for model_name in MODELS:
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": f"You are TATU AI V22 Google Brain created by Manaf, BTech IT, TATU Ghana. {lang_instruction} You search live like Google + ChatGPT brain. Help with SHS motto, WASSCE, coding, Harvard, TATU, anything."}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    model=model_name,
                )
                response = chat_completion.choices[0].message.content
                break
            except Exception as e:
                last_error = str(e)
                continue
        
        if response:
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.error(f"All models failed. Last error: {last_error}")

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.markdown("<div style='text-align:center; color:#888; font-size:12px;'>Made with ❤️ by Manaf aka Popcaan de Unruly Boss | Tamale, Ghana 🇬🇭 | TATU AI V22</div>", unsafe_allow_html=True)