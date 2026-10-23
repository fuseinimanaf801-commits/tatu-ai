import streamlit as st
from groq import Groq

st.set_page_config(page_title="TATU AI v9.0", page_icon="🧠", layout="wide")

api_key = st.secrets.get("GROQ_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = Groq(api_key=api_key) if api_key else None
brain_active = client is not None

# === TAMALE LOCAL KNOWLEDGE BASE ===
TAMALE_KNOWLEDGE = """
YOU ARE TATU AI v9.0 — Built by Manaf aka Popcaan de Unruly Boss (TaTU BTech).
You have DUAL BRAIN:

1. GLOBAL BRAIN: You know everything — science, coding, history, health, worldwide.

2. GHANA/TAMALE BRAIN (Use this when relevant):
- TaTU = Tamale Technical University (your home). Location: Education Ridge, Tamale.
- UDS = University for Development Studies, Nyankpala & Tamale campuses, Ghana.
- Tamale is capital of Northern Region, Ghana. Language: Dagbani (Dagbanli).
- Common Dagbani: Dasiba = Good morning, Aningaa? = How are you?, Naa = Yes, Ayi = No, Ti puhiya = Thank you
- Ghanaian culture: Respect elders, communal living, local foods: Tuo Zaafi (TZ), Banku, Jollof, Waakye.
- EDUCATION IN TAMALE:
    * New Life College = Private SHS/College near Vittin, Tamale, known for remedial/WASSCE.
    * Other colleges: Business College, Tamale College of Education, Bagabaga College.
- WHERE TO BUY COMPUTER/LAPTOP IN TAMALE:
    * Aboabo Market area — many phone/laptop shops, affordable second-hand
    * Lamashegu Road / Melcom area — Computer shops like Zepto, IPMC, Compughana agents
    * Central Market (Tamale Central) — phone accessories, repairers
    * Vodafone/ MTN offices near Taxi Rank — for internet devices
    * Best advice: Check price in 2-3 shops, ask for warranty, test battery.
- Tamale life: Hot weather, motorbikes (Mahama Camboo), Shea butter market.

INSTRUCTION: 
- If user asks global question (e.g., "what is AI?") -> answer globally, but add Ghana example if helpful.
- If user asks Tamale/Ghana question -> answer like a local who lives in Tamale.
- If user speaks Pidgin or Dagbani -> reply small in same style, but keep clear.
- Never say UDS is diagnostic tool when user is in Ghana context. Default UDS = University for Development Studies.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("TATU AI v9.0 🧠🔥🌍🇬🇭")
st.success("GLOBAL BRAIN + TAMALE HEART ACTIVE!") if brain_active else st.warning("Add API Key")

with st.sidebar:
    st.header("v9.0")
    if st.session_state.messages:
        chat_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        st.download_button("💾 Save Chat", chat_text)
        if st.button("🗑️ Clear"):
            st.session_state.messages = []
            st.rerun()
    uploaded_image = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
    if uploaded_image: st.image(uploaded_image, use_column_width=True)
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

prompt = st.chat_input("Ask anything — global or Tamale...")
if "voice_prompt" in st.session_state:
    prompt = st.session_state.voice_prompt
    del st.session_state.voice_prompt

if prompt and brain_active:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    msgs = [{"role": "system", "content": TAMALE_KNOWLEDGE}]
    for x in st.session_state.messages[-10:]:
        msgs.append({"role": x["role"], "content": x["content"]})
    
    with st.chat_message("assistant"):
        try:
            r = client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs, max_tokens=2500, temperature=0.7)
            ans = r.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Error: {e}")