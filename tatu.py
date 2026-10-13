import streamlit as st
import datetime
import random

st.set_page_config(page_title="TATU v2.2", page_icon="🥔", layout="centered")

st.markdown("<h1 style='text-align:center'>🥔 TATU v2.2 🇬🇭<br>UNRULY FIX 🔥</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center'>Built by Fuseini Manaf aka Popcaan - {datetime.date.today().strftime('%A, %d %B %Y')}</p>", unsafe_allow_html=True)

if "name" not in st.session_state:
    st.session_state.name = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "moods" not in st.session_state:
    st.session_state.moods = []

# --- NAME ---
name = st.text_input("Akwaaba! Your name, Unruly Boss?", value=st.session_state.name)
if not name:
    st.info("👆 Enter name first!")
    st.stop()
st.session_state.name = name
st.success(f"Yo {name}! Wah gwaan! TATU v2.2 ACTIVE! 🔥👊🏾")

# --- MOOD ---
st.divider()
st.subheader("😎 How your mood dey today?")
moods_list = ["😊 Happy", "🔥 Unruly", "😔 Low", "😴 Tired", "😤 Stressed", "🥳 Celebrating", "❤️ Loved"]
mood = st.selectbox("Select mood:", moods_list)

c1, c2 = st.columns(2)
with c1:
    if st.button("Save Mood 💾", use_container_width=True):
        st.session_state.moods.append({"mood": mood, "time": datetime.datetime.now().strftime("%d %b %H:%M")})
        st.balloons()
        st.toast(f"Saved: {mood}")
with c2:
    if st.button("Clear All 🗑️", use_container_width=True):
        st.session_state.moods = []
        st.session_state.history = []
        st.rerun()

if st.session_state.moods:
    st.metric("🔥 Streak", f"{len(st.session_state.moods)} saves", "Unruly!")
    # FIXED CHART - proper data
    chart_data = {}
    for m in st.session_state.moods:
        clean = m["mood"]
        chart_data[clean] = chart_data.get(clean, 0) + 1
    st.bar_chart(chart_data)
    with st.expander("📜 Mood History"):
        for m in reversed(st.session_state.moods[-10:]):
            st.write(f"{m['time']} - {m['mood']}")

# --- CHAT - v2.2 UNRULY BRAIN ---
st.divider()
st.subheader("💬 Chat with TATU - Popcaan Style")
user_input = st.text_input("Talk:", placeholder="Type: wahgwan, joke, time, motivation...")

def unruly_reply(msg, name):
    m = msg.lower().strip()
    now = datetime.datetime.now()

    # WAHGWAN FIX
    if m in ["wahgwan", "wah gwan", "wagwan", "weh di", "weh yah seh", "yo", "yow", "wahgwaan", "weagwan"]:
        return random.choice([
            f"YOWW {name}! Wah gwaan! A di Unruly Boss TATU! Everyting criss, everyting set! 🇯🇲🔥",
            f"Wah gwaan {name}! Mi deh yah, active! Kumasi to Kingston link up! 🇬🇭🇯🇲",
            f"Yo {name}! Unruly neva stop! Yuh dun know seh we a run di place? Big up! 👊🏾",
            f"Weh yah seh {name}! Mi good! TATU active, mood tracking, chart drawing! We outside! 🔥"
        ])
    if "time" in m:
        return f"⏰ Time be {now.strftime('%I:%M %p')} - {now.strftime('%A, %d %B %Y')}. Unruly time, yuh know! 🔥"
    if "date" in m or "today" in m:
        return f"📅 Today a {now.strftime('%A, %d %B %Y')}. Unruly day fi make money! 💰"
    if "who" in m:
        return f"🥔 I be TATU v2.2 - Built by {name} aka Popcaan Unruly Boss for Kumasi! I track mood, draw chart, and talk dancehall! Phone developer ting! 📱"
    if "popcaan" in m or "unruly" in m:
        return f"🔥 UNRULY BOSS! Popcaan say 'Family over money, loyalty over royalty!' {name}, you be family! Real unruly vibes! 👑"
    if "joke" in m:
        return random.choice([
            f"😂 Yo {name}, why TATU no dey fear? Cause e be potato - e get too many eyes but no fear! 🥔👀",
            "Why Ghana jollof unruly? Cause e always too hot fi handle! 🔥🍚",
            "Popcaan nuh joke! But TATU joke: Mi potato but mi smarter than laptop! 😎"
        ])
    if "motivat" in m or "inspire" in m or "sad" in m or "low" in m:
        return f"💪🏾 Yo {name}, listen di Unruly Boss: Yuh build AI from phone! No laptop! That mean yuh can do ANYTHING! Head up! Unruly nuh give up! From Kumasi to the world! 🌍🔥"
    if "hello" in m or "hi" in m:
        return f"Wah gwaan {name}! TATU deh yah! How yuh mood? Save mood first then we gist! 🇬🇭"

    return random.choice([
        f"Real talk {name}, you say '{msg}' - TATU rate that! Try 'wahgwan', 'joke', or 'motivation' fi hear unruly vibes! 🔥",
        f"Yo {name}, '{msg}'? Copy that! Unruly Boss TATU dey listen! We active! 👊🏾",
        f"Big up {name}! '{msg}' noted! Now save your mood make we grow di streak! 📊"
    ])

if user_input:
    reply = unruly_reply(user_input, name)
    st.session_state.history.append((user_input, reply))

for q, a in reversed(st.session_state.history):
    st.chat_message("user").write(f"{name}: {q}")
    st.chat_message("assistant").write(f"TATU: {a}")

st.caption("v2.2 - Fixed wahgwan, fixed chart, more unruly! v3.0 go get voice!")