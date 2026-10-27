import streamlit as st
from groq import Groq

# --- APP CONFIG ---
st.set_page_config(
    page_title="TATU AI - Tamale AI",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM APP CSS ---
st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
.block-container {padding-top: 1rem; padding-bottom: 5rem;}
.stChatInput {border-radius: 15px; padding: 10px;}
h1 {text-align: center; font-size: 28px !important;}
</style>
""", unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY missing in secrets")
    st.stop()

client = Groq(api_key=api_key)

# --- REAL BRAIN - NO LIES ---
KNOWLEDGE_BASE = """
Tamale Technical University (TATU):
- Established 1951 as Trades Training Centre -> 1960 Junior Technical Institute -> Aug 1992 Polytechnic (PNDC Law 321) -> 2018 Technical University (Act 974).
- Location: Tamale, Northern Region, Savannah Zone.
- Core values: discipline, efficiency, effectiveness, excellence.
- Staff: Lecturer must have PhD. Assistant Lecturer needs MPhil + enrolled in PhD. No official public PhD % published.

Kumasi Technical University (KsTU) VERIFIED 2024 from kstu.edu.gh:
- Total teaching staff 284 (Male 224, Female 60)
- PhD holders 115 (103 male + 12 female) = ~40.5%, Masters 169
- VC reported 116 PhD holders. Only Tech University in Ghana accredited to run pre-engineering and doctoral programmes.
- Do NOT invent 25% or Ghana Telecom story.
"""

SYSTEM_PROMPT = f"""
{KNOWLEDGE_BASE}

CRITICAL RULES:
1. NEVER invent percentages, fees, cut-off, hostel prices. If not in KNOWLEDGE_BASE, say: "I don't have verified official data - check tatu.edu.gh or Academic Affairs. It changes yearly."
2. For TATU vs KsTU comparison: Use KsTU = 115/284 = ~40.5% PhD. For TATU say "Requires PhD for Lecturer, no public % published." Never say 30% UK/US or ex-MTN.
3. Be friendly Ghanaian student, short, helpful.
4. Built by Manaf - Popcaan de Unruly Boss. Glooooballl!

Respond as TATU AI v10.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Baasab! I'm TATU AI v10 - your Tamale AI. Built by Manaf ❤️ TATU BTech. Glooooballl! How I go help you today?"}
    ]
if "voice_prompt" not in st.session_state:
    st.session_state.voice_prompt = ""

st.caption("Built by Manaf | TATU BTech | Tamale Heart")
st.title("TATU AI 🎓\nTamale Technical University AI")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

with st.expander("Tools: Voice & Image"):
    col1, col2 = st.columns(2)
    with col1:
        audio = st.audio_input("Tap to speak")
        if audio:
            try:
                with open("/tmp/voice.wav", "wb") as f:
                    f.write(audio.getvalue())
                with open("/tmp/voice.wav", "rb") as af:
                    transcription = client.audio.transcriptions.create(
                        file=("voice.wav", af.read()),
                        model="whisper-large-v3",
                        response_format="text"
                    )
                st.session_state.voice_prompt = transcription
                st.success(f"You said: {transcription}")
            except Exception as e:
                st.error(f"Voice error: {e}")
    with col2:
        img_file = st.file_uploader("Upload image", type=["png","jpg","jpeg"])
        if img_file:
            st.image(img_file, use_column_width=True)

prompt = st.chat_input("Ask anything about TATU...")
final_prompt = prompt or st.session_state.get("voice_prompt", "")
if st.session_state.get("voice_prompt"):
    st.session_state.voice_prompt = ""

if final_prompt:
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.markdown(final_prompt)

    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    for x in st.session_state.messages[-10:]:
        msgs.append({"role": x["role"], "content": x["content"]})

    try:
        with st.chat_message("assistant"):
            with st.spinner("TATU AI dey think..."):
                resp = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=msgs,
                    max_tokens=2000,
                    temperature=0.4
                )
                ans = resp.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
    except Exception as e:
        st.error(f"Error: {e}")

with st.sidebar:
    st.title("TATU AI App")
    st.write("VERSION 10 - Truth Edition")
    st.write("By Manaf aka Popcaan de Unruly Boss")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()