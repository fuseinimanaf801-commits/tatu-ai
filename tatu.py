import streamlit as st
import datetime
import random

st.set_page_config(page_title="TATU v2.1 Unruly", page_icon="🥔", layout="centered")

# --- STYLES ---
st.markdown("""
<style>
.big {font-size:30px; text-align:center; font-weight:bold}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big'>🥔 TATU AI v2.1 🇬🇭<br>UNRULY EDITION 🔥</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center'>Built by Fuseini Manaf aka Popcaan Unruly Boss - {datetime.date.today().strftime('%A, %d %B %Y')}</p>", unsafe_allow_html=True)

# --- SESSION ---
if "name" not in st.session_state:
    st.session_state.name = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "moods" not in st.session_state:
    st.session_state.moods = []
if "streak" not in st.session_state:
    st.session_state.streak = 1
if "last_date" not in st.session_state:
    st.session_state.last_date = str(datetime.date.today())

# --- NAME ---
name = st.text_input("Akwaaba! What be your name? Unruly boss!", value=st.session_state.name)
if not name:
    st.info("👆 Enter your name make we start the unruly vibes!")
    st.stop()

st.session_state.name = name
st.success(f"Yo {name}! TATU v2.1 UNRULY dey active! Wah gwaan? 👊🏾🔥")

# --- MOOD TRACKER ---
st.divider()
st.subheader("😎 How your mood dey today?")
mood = st.selectbox("Select mood:", ["😊 Happy", "🔥 Unruly / Energetic", "😔 Low", "😴 Tired", "😤 Stressed", "🥳 Celebrating", "❤️ Loved"])
if st.button("Save Mood"):
    st.session_state.moods.append({"date": str(datetime.date.today()), "mood": mood, "time": datetime.datetime.now().strftime("%H:%M")})
    st.balloons()
    st.toast(f"Mood saved: {mood}")

# Show streak
if st.session_state.moods:
    st.metric("🔥 Current Streak", f"{len(st.session_state.moods)} days", "Unruly streak!")
    # Simple chart
    st.caption("📊 Your Mood Journey:")
    mood_counts = {}
    for m in st.session_state.moods:
        mood_counts[m["mood"]] = mood_counts.get(m["mood"], 0) + 1
    st.bar_chart(mood_counts)

# --- CHAT ---
st.divider()
st.subheader(f"💬 Chat with TATU - Popcaan Style")

user_input = st.text_input("Talk to TATU:", placeholder="Try: who are you, joke, motivation, time, Popcaan style...")

def get_reply(msg, name):
    msg = msg.lower()
    now = datetime.datetime.now()
    
    popcaan_vibes = [
        f"Yo {name}, a di Unruly Boss TATU dis! Every ting set, yuh dun know! 🔥",
        f"Unruly neva stop! {name}, we a run di place! Kumasi to Kingston! 🇬🇭🇯🇲",
        f"Rude bwoy {name}, TATU deh yah fi yuh! No worry, we active!",
    ]
    
    if "time" in msg:
        return f"⏰ {random.choice(popcaan_vibes)} Time now be {now.strftime('%I:%M %p')} - {now.strftime('%A, %d %B %Y')}"
    elif "date" in msg or "day" in msg:
        return f"📅 Today be {now.strftime('%A, %d %B %Y')}. Unruly day, yuh know! 🔥"
    elif "who" in msg:
        return f"🥔 Yo {name}! I be TATU v2.1 UNRULY EDITION! Built by Popcaan de Unruly Boss - Fuseini Manaf for Kumasi! I dey track mood, draw chart, and gist like Popcaan! 🇬🇭"
    elif "popcaan" in msg or "unruly" in msg:
        return random.choice(popcaan_vibes) + " Popcaan say: 'Unruly nuh stop till di casket drop!' Real vibes!"
    elif "joke" in msg:
        jokes = [
            "Why potato no dey fight? Because e be TATU - e too cool! 🥔😂",
            "Unruly joke: Why Ghana jollof always win? Because e get UNRULY flavor! 🔥",
            "Popcaan joke: Mi nuh joke, mi serious! But TATU funny still! 😂"
        ]
        return random.choice(jokes)
    elif "motivat" in msg or "inspire" in msg:
        return f"🔥 Yo {name}, Popcaan voice: Yuh a star! From Kumasi phone you build AI! No boy can stop yuh! Keep coding, keep unruly! Unruly Boss believe in yuh! 👊🏾💪🏾"
    elif "hello" in msg or "hi" in msg or "yo" in msg:
        return f"Wah gwaan {name}! A TATU! Yuh good? We dey ya, active! What yuh want? Time, joke, or unruly vibes? 🇯🇲🇬🇭"
    elif "love" in msg:
        return f"❤️ Unruly love for you {name}! TATU love you like Popcaan love di music! Big up yourself!"
    else:
        replies = [
            f"Yo {name}, yuh say '{msg}'? TATU hear yuh loud! Unruly vibes activated! Ask me for time, joke, motivation, or Popcaan style! 🔥",
            f"Real talk {name}, '{msg}'? Mi understand! TATU v2.1 still dey learn, but mood tracker dey work! Save your mood today!",
            f"Unruly Boss {name}, you talk '{msg}' - TATU respect that! Try type 'joke' or 'motivation' make you see magic!"
        ]
        return random.choice(replies)

if user_input:
    reply = get_reply(user_input, name)
    st.session_state.history.append((user_input, reply))

# Show chat
for q, a in reversed(st.session_state.history):
    st.markdown(f"**{name}:** {q}")
    st.markdown(f"**🥔 TATU Unruly:** {a}")
    st.divider()

st.caption("v2.1 - Tracks mood, detects streaks, draws charts, talks Popcaan! Next: v3.0 with voice!")