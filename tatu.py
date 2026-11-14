import streamlit as st
import os, requests, urllib.parse
from groq import Groq

st.set_page_config(page_title="TATU AI V23", page_icon="✅", layout="centered")
st.markdown("### TATU AI V23 Truth Mode ✅ | Built by Manaf | Real Live Search | No Lies")
st.title("TATU AI V23 - Truth Mode 🔍")

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
st.caption(f"Welcome back, {st.session_state.user_name} | TATU Ghana 🇬🇭 | By Manaf")

def live_search(query):
    # Real search from Wikipedia - no guessing
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
        r = requests.get(url, timeout=8, headers={"User-Agent": "TATU-AI-V23"})
        if r.status_code == 200:
            d = r.json()
            return f"WIKIPEDIA FACT: {d.get('title')}: {d.get('extract','')[:2000]} Source: {d.get('content_urls',{}).get('desktop',{}).get('page','')}"
    except Exception as e:
        pass
    # Fallback: DuckDuckGo Instant Answer
    try:
        r = requests.get("https://api.duckduckgo.com/", params={"q": query, "format": "json", "no_html": 1}, timeout=8)
        d = r.json()
        txt = d.get("AbstractText") or d.get("Answer") or ""
        if txt:
            return f"SEARCH FACT: {txt[:2000]} Source: {d.get('AbstractURL','')}"
    except:
        pass
    return "NO LIVE FACT FOUND - DO NOT GUESS NUMBERS."

client = Groq(api_key=st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY")))

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Ask with Truth Mode...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching live... 🔍"):
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
                    messages=[{"role": "system", "content": f"You are TATU AI V23 Truth Mode by Manaf. {lang_inst} RULES: 1. NEVER invent numbers, dates, or statistics. 2. Only use the LIVE FACTS below. 3. If LIVE FACT says NO FACT FOUND, say 'I no find confirmed data, make I no lie you' and give general advice only. 4. Never repeat same country twice in a list. 5. Always say where you got the fact and the year. 6. If unsure, say you are not sure. LIVE FACTS: {facts}"}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    model=model_name,
                )
                response = cc.choices[0].message.content
                break
            except Exception as e:
                continue
        if response:
            st.markdown(response)
            st.caption("✅ Checked with live search - if e no find am, e go tell you")
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.error("Model error, try again")

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.markdown("<div style='text-align:center; color:#888; font-size:12px;'>Made with ❤️ by Manaf aka Popcaan | TATU AI V23 Truth Mode - No Lies</div>", unsafe_allow_html=True)