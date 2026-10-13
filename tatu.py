import streamlit as st
import datetime
import random

st.set_page_config(page_title="TATU v3.0 Voice", page_icon="🥔", layout="centered")

# --- THEME ---
if "light" not in st.session_state:
    st.session_state.light = False

theme = "light" if st.session_state.light else "dark"
bg = "#f5f5f5" if st.session_state.light else "#0e1117"
txt = "#000" if st.session_state.light else "#fff"

st.markdown(f"<style>.stApp {{ background-color: {bg}; color: {txt}; }} </style>", unsafe_allow_html=True)

st.markdown(f"<h1 style='text-align:center'>🥔 TATU v3.0 🇬🇭<br>VOICE + MEMORY 🔊</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center'>Built by Fuseini Manaf aka Popcaan | {datetime.date.today().strftime('%A, %d %B %Y')}</p>", unsafe_allow_html=True)

colA, colB = st.columns(2)
with colA:
    if st.button("🌓 Toggle Light/Dark"):
        st.session_state.light = not st.session_state.light
        st.rerun()
with colB:
    st.caption(f"Mode: {theme.upper()}")

# --- MEMORY ---
for k in ["name","history","moods","goal"]:
    if k not in st.session_state:
        st.session_state[k] = [] if k in ["history","moods"] else ""

name = st.text_input("Akwaaba Unruly Boss! Your name?", value=st.session_state.name)
if not name:
    st.info("Enter name make we start!")
    st.stop()
st.session_state.name = name

# --- DAILY GOAL ---
st.divider()
st.subheader("🎯 Today's Unruly Goal")
goal = st.text_input("Set goal today:", value=st.session_state.goal if isinstance(st.session_state.goal, str) else "", placeholder="eg: Code 1hr, pray, gym...")
if st.button("Save Goal"):
    st.session_state.goal = goal
    st.success(f"Goal locked: {goal} 🔥")

if st.session_state.goal:
    st.info(f"🎯 {name} goal: {st.session_state.goal}")

# --- MOOD ---
st.subheader("😎 Mood Tracker v3.0")
moods_list = ["😊 Happy", "🔥 Unruly", "😔 Low", "😴 Tired", "😤 Stressed", "🥳 Celebrating", "❤️ Loved", "💪 Motivated"]
mood = st.selectbox("Mood:", moods_list)
c1, c2 = st.columns(2)
with c1:
    if st.button("Save Mood 💾", use_container_width=True):
        st.session_state.moods.append({"mood": mood, "time": datetime.datetime.now().strftime("%d %b %H:%M"), "day": str(datetime.date.today())})
        st.balloons()
with c2:
    if st.button("Clear 🗑️", use_container_width=True):
        st.session_state.moods = []
        st.session_state.history = []
        st.rerun()

if st.session_state.moods:
    st.metric("🔥 Streak", f"{len(st.session_state.moods)}", f"Last: {st.session_state.moods[-1]['mood']}")
    chart_data = {}
    for m in st.session_state.moods:
        chart_data[m["mood"]] = chart_data.get(m["mood"], 0) + 1
    st.bar_chart(chart_data)
    with st.expander(f"📜 History ({len(st.session_state.moods)})"):
        for m in reversed(st.session_state.moods[-15:]):
            st.write(f"{m['time']} - {m['mood']}")

# --- CHAT v3.0 WITH VOICE ---
st.divider()
st.subheader("💬 Chat + Voice - Popcaan Style")

popcaan_quotes = [
    "Unruly nuh stop till di casket drop!",
    "Family over money, loyalty over royalty!",
    "We never fail, we only learn!",
    "Real boss nuh need fi talk much!",
    "Kumasi to Kingston, we run di place!"
]

def get_reply_v3(msg, name):
    m = msg.lower().strip()
    now = datetime.datetime.now()

    if m in ["wahgwan","wah gwan","wagwan","weh di","yow","yo","wahgwaan","weagwan","wag"]:
        return random.choice([
            f"YOWWW {name}! Wah gwaan! A TATU v3.0! Mi get VOICE now! Everyting loud! 🔊🔥",
            f"Wah gwaan {name}! Mi deh yah ACTIVE with voice! Kumasi to Kingston link up! 🇬🇭🇯🇲",
            f"Unruly Boss {name}! Wah gwaan? Mi can TALK now! Press speaker! 🔊"
        ])
    if "time" in m:
        return f"⏰ {now.strftime('%I:%M %p')} - {now.strftime('%A, %d %B %Y')}. Unruly time! 🔊"
    if "goal" in m:
        return f"🎯 Your goal: {st.session_state.goal if st.session_state.goal else 'No goal yet! Set one!'} - Unruly focus!"
    if "quote" in m or "popcaan" in m:
        return f"👑 Popcaan Quote: '{random.choice(popcaan_quotes)}' - Big up {name}!"
    if "who" in m:
        return f"🥔 I be TATU v3.0 VOICE EDITION! Built by {name} Popcaan! I get memory, voice, mood chart! Phone built! 📱🔥"
    if "joke" in m:
        return random.choice([f"😂 {name}, TATU get voice now but still potato! 🥔🔊", "Why AI no need sleep? Cause e unruly! No rest! 🔥"])
    if "motivat" in m or "low" in m or "sad" in m:
        return f"💪🏾 {name}, {random.choice(popcaan_quotes)} You build v3.0 from phone! No man can stop you! 🚀"
    if "hello" in m or "hi" in m:
        return f"Wah gwaan {name}! TATU v3.0 ready! I get voice now! Type 'wahgwan' or 'quote'! 🇯🇲"
    return random.choice([
        f"Big up {name}! You say '{msg}' - TATU v3.0 hear with MEMORY! 🧠",
        f"Yo {name}, '{msg}' saved for history! Unruly memory active!",
        f"Real talk {name}, try 'wahgwan', 'quote', 'goal', 'time', 'joke' - v3.0 get many vibes!"
    ])

user_input = st.text_input("Talk to TATU:", placeholder="Type wahgwan, quote, goal, joke...", key="chat")

# VOICE FUNCTION - JS speech
def speak(text):
    # Escape quotes for JS
    safe = text.replace("'", "").replace('"','').replace("\n"," ")
    js = f"""
    <script>
    var msg = new SpeechSynthesisUtterance();
    msg.text = "{safe}";
    msg.rate = 0.95;
    msg.pitch = 0.9;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js, height=0)

if user_input:
    reply = get_reply_v3(user_input, name)
    st.session_state.history.append((user_input, reply))
    st.session_state.last_reply = reply

# Show chats with VOICE button
if "last_reply" in st.session_state and st.session_state.last_reply:
    if st.button("🔊 PLAY VOICE - Make TATU Talk!"):
        speak(st.session_state.last_reply)

for q, a in reversed(st.session_state.history):
    st.chat_message("user").write(f"{name}: {q}")
    st.chat_message("assistant").write(f"TATU: {a}")

st.divider()
st.caption("v3.0 Voice + Memory + Goals + Light/Dark | Next v4.0: Save to database forever! | Built by Popcaan Unruly Boss")
st.caption("Tip: Turn on phone volume! 🔊 Press PLAY VOICE after TATU reply!")