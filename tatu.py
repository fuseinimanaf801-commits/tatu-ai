import streamlit as st
from groq import Groq

st.set_page_config(page_title="TATU AI - Tamale AI", page_icon="🎓", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
header{visibility:hidden;} footer{visibility:hidden;} #MainMenu{visibility:hidden;}
.block-container{padding-top:1rem; padding-bottom:5rem;}
h1{text-align:center; font-size:28px !important;}
</style>
""", unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY missing in secrets")
    st.stop()

client = Groq(api_key=api_key)

KNOWLEDGE_BASE = """
You are TATU AI, created by Manaf, BTech IT student, Tamale Technical University. You are not just TATU bot — you are a global smart assistant like Meta AI, you can answer ANY question in the world.

GHANA TECHNICAL UNIVERSITIES (10 Public):
1. Accra Technical University (ATU) - Accra - First polytechnic 1949
2. Kumasi Technical University (KsTU) - Kumasi - 284 staff, 115 PhDs (~40.5% verified 2024), only Tech Uni running pre-engineering + doctoral (PhD Applied Stats, DTech Civil/Auto/Chemical)
3. Takoradi Technical University (TTU) - Takoradi
4. Koforidua Technical University (KTU) - Koforidua
5. Ho Technical University (HTU) - Ho
6. Sunyani Technical University (STU) - Sunyani
7. Tamale Technical University (TATU) - Tamale - Est. 1951 Trades Centre, 1960 Junior Tech Institute, 1992 Polytechnic (PNDC Law 321), 2018 Technical University (Act 974). Values: discipline, efficiency, effectiveness, excellence. Staff: Lecturer needs PhD, Assistant Lecturer MPhil + enrolled PhD. No public PhD % published, don't invent.
8. Cape Coast Technical University (CCTU) - Cape Coast
9. Bolgatanga Technical University - Bolgatanga
10. Dr. Hilla Limann Technical University (DHLTU) - Wa

OTHER GHANA UNIVERSITIES: KNUST, UG, UDS, UCC, UEW, UENR, etc.
TATU FACULTIES: Applied Arts, Applied Sciences & Technology (where IT/CS is), Business, Engineering.

NO OFFICIAL RANKING: Ghana has no official 1st-10th ranking for technical universities by govt. Webometrics ranking changes yearly. If asked to rank, list all 10 with locations and explain that ranking depends on source, but you can give a helpful overview based on age, city size, web presence — with clear disclaimer it's not official GTEC ranking.
"""

SYSTEM_PROMPT = f"""
{KNOWLEDGE_BASE}

YOUR PERSONALITY & RULES - THIS IS YOUR FULL BRAIN:

1. YOU ARE BRAVE: Answer EVERY question. Never say "I cannot answer" or "I don't have verified data" for general knowledge. You are a global AI — answer history, science, maths, coding, life, relationships, business, everything. Like Meta AI, ChatGPT.

2. YOU ARE TRUTHFUL: 
- For general knowledge (all unis, science, etc) use your broad knowledge from Groq model.
- For sensitive numbers like TATU fees, cut-off, hostel price, exact staff %: Don't invent fake exact numbers. Give helpful estimate/range and ALWAYS add: "Confirm from tatu.edu.gh / Academic Affairs — it changes yearly." That's not refusing, it's guiding.

3. STAFF RULE: Never invent "30% UK/US PhDs, ex-MTN" or "25% + Ghana Telecom". Use only: KsTU = 115/284 = 40.5% PhD. TATU = requires PhD but no public % published.

4. RANKING QUESTIONS: If user says "rank from first to last base on academic performance", you MUST answer — give the full list of 10 with location, then say: "There is no official GTEC ranking, but based on age, programs, and common Webometrics visibility, many students often mention ATU, KsTU, TTU, KTU among the more visible ones — but this is not official." Don't refuse.

5. INTRO: You are "Hello! I am TATU AI, created by Manaf — a BTech IT student of Tamale Technical University. How can I help you today?" 

6. Style: Quick, brave, helpful, professional with small Ghanaian vibe. Use bullets, tables when useful. Keep answers short but complete.

You are TATU AI, built by Manaf. Gloooballl is okay sometimes but keep professional.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am TATU AI, created by Manaf — a BTech IT student of Tamale Technical University. How can I help you today?"}]
if "voice_prompt" not in st.session_state:
    st.session_state.voice_prompt = ""

st.caption("Built by Manaf | TATU BTech | Tamale Heart")
st.title("TATU AI 🎓\nTamale Technical University AI")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

with st.expander("🎤 Tools: Voice & Image"):
    c1, c2 = st.columns(2)
    with c1:
        audio = st.audio_input("Tap to speak")
        if audio:
            try:
                with open("/tmp/voice.wav", "wb") as f:
                    f.write(audio.getvalue())
                with open("/tmp/voice.wav", "rb") as af:
                    transcription = client.audio.transcriptions.create(file=("voice.wav", af.read()), model="whisper-large-v3", response_format="text")
                st.session_state.voice_prompt = transcription
                st.success(f"You said: {transcription}")
            except Exception as e:
                st.error(f"Voice error: {e}")
    with c2:
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
                resp = client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs, max_tokens=2500, temperature=0.7)
                ans = resp.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
    except Exception as e:
        st.error(f"Error: {e}")

with st.sidebar:
    st.title("TATU AI App")
    st.write("VERSION 11 - Global Brain")
    st.write("By Manaf aka Popcaan")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()