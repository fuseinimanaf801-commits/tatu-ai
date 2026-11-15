import streamlit as st
import os, requests, urllib.parse
from groq import Groq

st.set_page_config(page_title="TATU AI V25 Global", page_icon="🌍", layout="centered")
st.markdown("### TATU AI V25 Global 🌍 | Built by Manaf | ChatGPT + Google Brain | Knows Everything")
st.title("TATU AI V25 - Global Brain 🌍")

# EXTRA KNOWLEDGE - NOT ONLY TATU. Use only when user asks TATU.
TATU_INFO = """
TATU BTech IT L100 Timetable (Official 10/26/2026):
Mon: FREE
Tue: 10:00-12:00 Algebra S8 Dr Caleb N. Namlyin 0248500137 | Evening African Studies B8 Mr Saifu Alhassan 0242707815
Wed: 8:00-10:00 Critical Thinking and Logic L/HALL 1 Mr John Issah Alhassan 0234462046
Thu: 8:00-10:00 Communication Skills I B8 Mr Ibrahim 0349304170
Fri: 8:00-10:00 Fundamentals of IT L/HALL 2 Abed Timothy Narh 0249222106 | 1:00-3:00 Digital Logic L/HALL 1 Mr Thomas Nanbong 0553997352 | 4:00-6:00 Principles of Programming L/HALL 1 Dr Abdul-Wahab Nawara 0249362906
TATU = Tamale Technical University, Ghana.
"""

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

lang = st.selectbox("Choose Language:", ["English", "Pidgin", "Dagbani"])
st.caption(f"Welcome back, {st.session_state.user_name} | Global AI 🇬🇭🌍 | By Manaf")

st.write("**Ask Anything:**")
c1, c2, c3 = st.columns(3)
quick = ""
if c1.button("🌍 World News"):
    quick = "Tell me about world news today"
if c2.button("📚 My Timetable"):
    quick = "What is my BTech IT L100 timetable?"
if c3.button("💻 Coding"):
    quick = "Teach me Python coding for beginners"

def live_search(query):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
        r = requests.get(url, timeout=8, headers={"User-Agent": "TATU-AI-V25"})
        if r.status_code == 200:
            d = r.json()
            return f"WIKIPEDIA: {d.get('title')}: {d.get('extract','')[:2000]}"
    except:
        pass
    try:
        r = requests.get("https://api.duckduckgo.com/", params={"q": query, "format": "json", "no_html": 1}, timeout=8)
        d = r.json()
        txt = d.get("AbstractText") or ""
        if txt:
            return f"SEARCH: {txt[:2000]}"
    except:
        pass
    return "NO LIVE FACT FOUND"

client = Groq(api_key=st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY")))

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Ask ANYTHING in the world...") or quick

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Searching world... 🌍"):
            facts = live_search(prompt)
        lang_inst = "Answer in clear simple English."
        if lang == "Dagbani":
            lang_inst = "Answer in Dagbani mixed with simple English."
        elif lang == "Pidgin":
            lang_inst = "Answer in Ghana Pidgin."
        MODELS = ["openai/gpt-oss-20b", "openai/gpt-oss-120b"]
        response = None
        for model_name in MODELS:
            try:
                cc = client.chat.completions.create(
                    messages=[{"role": "system", "content": f"You are TATU AI V25 GLOBAL Brain by Manaf, like ChatGPT + Google combined. {lang_inst} You can answer ANYTHING: world news, science, coding, Harvard, study abroad, football, history, anything in the world. You are NOT limited to TATU. Only use this TATU info when user asks about TATU: {TATU_INFO}. RULES: Never invent numbers/dates. If you use live facts, use them: {facts}. If no live fact, use your general knowledge but say if you are not 100% sure. Be friendly and smart."}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    model=model_name,
                )
                response = cc.choices[0].message.content
                break
            except:
                continue
        if response:
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.error("Try again")

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.markdown("<div style='text-align:center; color:#888; font-size:12px;'>Made with ❤️ by Manaf aka Popcaan | TATU AI V25 Global - Knows Everything</div>", unsafe_allow_html=True)