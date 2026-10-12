import streamlit as st
import datetime

st.set_page_config(page_title="TATU AI v2.0", page_icon="🥔", layout="centered")

st.markdown("<h1 style='text-align:center'>🥔 TATU AI v2.0 🇬🇭</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Built by Fuseini Manaf - Monday 12 Oct 2026</p>", unsafe_allow_html=True)

if "name" not in st.session_state:
    st.session_state.name = ""
if "history" not in st.session_state:
    st.session_state.history = []

name = st.text_input("Akwaaba! What be your name?", value=st.session_state.name)

if name:
    st.session_state.name = name
    st.success(f"Akwaaba {name}! TATU dey ready! 👊🏾")

    user_input = st.text_input("Talk to TATU:", placeholder="Type like: what time is it in Kumasi?")

    if user_input:
        now = datetime.datetime.now()
        reply = ""
        msg = user_input.lower()
        
        if "time" in msg:
            reply = f"⏰ Time now be {now.strftime('%I:%M %p')} - Monday 12 October 2026, for your phone time!"
        elif "date" in msg or "day" in msg:
            reply = f"📅 Today be Monday, 12 October 2026. We dey Kumasi!"
        elif "who" in msg and "you" in msg:
            reply = f"I be TATU AI v2.0, built by {name} and Fuseini for Kumasi! 🥔"
        elif "hello" in msg or "hi" in msg:
            reply = f"Hi {name}! How you dey? Chale, what you want make I do?"
        else:
            reply = f"Chale {name}, you talk say '{user_input}'. TATU hear you! For v2.1 we go add full AI brain, but for now I fit tell time, date, and gist with you!"

        st.session_state.history.append((user_input, reply))
    
    for q, a in reversed(st.session_state.history):
        st.markdown(f"**You:** {q}")
        st.markdown(f"**TATU:** {a}")
        st.divider()

else:
    st.info("👆 Enter your name first make we start!")