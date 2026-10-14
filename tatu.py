import streamlit as st
import datetime, json, os, random

st.set_page_config(page_title="TATU v4.0 Forever", page_icon="🥔", layout="centered")

# --- FOREVER SAVE SYSTEM ---
DB_FILE = "tatu_forever_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db(data):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f)
    except:
        pass

if "db" not in st.session_state:
    st.session_state.db = load_db()

st.markdown("<h1 style='text-align:center'>🥔 TATU v4.0 🇬🇭<br>FOREVER EDITION 💾</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center'>Built by Fuseini Manaf aka Popcaan | {datetime.date.today().strftime('%A, %d %B %Y')}</p>", unsafe_allow_html=True)
st.caption("💾 New: Your moods & chats save FOREVER! Even after you close app!")

# --- LOGIN / MULTI-USER ---
st.divider()
st.subheader("🔐 Login - Unruly Family")

name = st.text_input("Enter your Unruly Name:", placeholder="eg: Manaf, Hajia Rams...").strip()
if not name:
    st.info("👆 Enter name to load your forever data!")
    st.stop()

name = name.title()
# Load or create user
if name not in st.session_state.db:
    st.session_state.db[name] = {"moods": [], "history": [], "goal": "", "joined": str(datetime.date.today())}
    save_db(st.session_state.db)

user_data = st.session_state.db[name]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("👤 User", name)
with col2:
    st.metric("📅 Joined", user_data.get("joined","Today"))
with col3:
    st.metric("🔥 Total Moods", len(user_data["moods"]))

# --- GOAL FOREVER ---
st.subheader("🎯 Forever Goal")
goal = st.text_input("Today's goal:", value=user_data.get("goal",""), placeholder="Code TATU v5.0")
if st.button("Save Goal Forever 💾"):
    st.session_state.db[name]["goal"] = goal
    save_db(st.session_state.db)
    st.success(f"Goal saved forever for {name}: {goal}")
    st.balloons()

# --- MOOD FOREVER ---
st.subheader("😎 Mood Tracker - FOREVER SAVE")
moods_list = ["😊 Happy", "🔥 Unruly", "😔 Low", "😴 Tired", "😤 Stressed", "🥳 Celebrating", "❤️ Loved", "💪 Motivated", "🧠 Focused"]
mood = st.selectbox("How you dey?", moods_list)

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Save Mood 💾", use_container_width=True):
        entry = {"mood": mood, "time": datetime.datetime.now().strftime("%d %b %H:%M"), "date": str(datetime.date.today())}
        st.session_state.db[name]["moods"].append(entry)
        save_db(st.session_state.db)
        st.success(f"Saved forever: {mood}")
        st.balloons()
with c2:
    if st.button("Weekly 📊", use_container_width=True):
        st.session_state.show_weekly = True
with c3:
    if st.button("Clear My Data 🗑️", use_container_width=True):
        st.session_state.db[name] = {"moods": [], "history": [], "goal": "", "joined": str(datetime.date.today())}
        save_db(st.session_state.db)
        st.rerun()

moods = st.session_state.db[name]["moods"]
if moods:
    # Chart
    chart_data = {}
    for m in moods:
        chart_data[m["mood"]] = chart_data.get(m["mood"], 0) + 1
    st.bar_chart(chart_data)

    # Weekly
    if st.session_state.get("show_weekly"):
        st.info(f"📅 This week: {len(moods)} moods tracked. Last 7: " + ", ".join([m['mood'] for m in moods[-7:]]))

    with st.expander(f"📜 {name} Forever History ({len(moods)})"):
        for m in reversed(moods[-20:]):
            st.write(f"{m['time']} - {m['mood']}")

# --- CHAT FOREVER ---
st.divider()
st.subheader("💬 Chat + Voice - Forever Memory")

popcaan_quotes = [
    "Family over money, loyalty over royalty!",
    "We never fail, we only learn!",
    "Kumasi to Kingston, we run di place!",
    "Unruly nuh stop till di casket drop!",
    "Real boss move in silence!",
    "From phone we build empire - Unruly!",
    "Every ghetto youth can be star!",
    "No weapon formed against us shall prosper!"
]

def get_v4_reply(msg, name):
    m = msg.lower().strip()
    now = datetime.datetime.now()
    moods = st.session_state.db[name]["moods"]
    last_mood = moods[-1]["mood"] if moods else "No mood yet"

    if m in ["wahgwan","wagwan","yo","yow","wah gwan","wahgwaan","weagwan"]:
        return random.choice([
            f"YOWWW {name}! Wah gwaan! v4.0 FOREVER! I remember you! You get {len(moods)} moods saved! 🔊🔥",
            f"Wah gwaan {name}! I remember your last mood be {last_mood}! Unruly memory never forget! 🇬🇭🇯🇲",
            f"Yo {name}! Welcome back! Forever edition! Your data dey safe! {len(moods)} memories! 💾"
        ])
    if "time" in m:
        return f"⏰ {now.strftime('%I:%M %p')} - {now.strftime('%A, %d %B %Y')} | Your forever moods: {len(moods)} 🔥"
    if "how many" in m or "stats" in m or "my moods" in m:
        return f"📊 {name}, you get {len(moods)} moods forever! Last be {last_mood}. Goal be: {st.session_state.db[name].get('goal','No goal')}"
    if "quote" in m or "popcaan" in m:
        return f"👑 Popcaan: '{random.choice(popcaan_quotes)}' - Big up {name}! Forever unruly! 🔥"
    if "who" in m:
        return f"🥔 I be TATU v4.0 FOREVER! I remember {name} since {st.session_state.db[name].get('joined')}. {len(moods)} moods, I never forget! 📱💾"
    if "joke" in m:
        return f"😂 {name}, v4.0 joke: I never forget because I be elephant potato! 🐘🥔 {len(moods)} memories!"
    if "motivat" in m or "low" in m:
        return f"💪🏾 {name}, you from v1 to v4.0! {len(moods)} moods tracked! {random.choice(popcaan_quotes)} You dey go far! 🚀"
    if "goal" in m:
        return f"🎯 {name} goal forever: {st.session_state.db[name].get('goal','Set one!')} - Keep pushing!"
    return random.choice([
        f"Big up {name}! '{msg}' saved forever! 🧠💾",
        f"Yo {name}, '{msg}'? Noted! I remember everything now! Forever! 🔥",
        f"Real talk {name}, try 'wahgwan', 'stats', 'quote', 'goal' - v4.0 remember you!"
    ])

chat_input = st.text_input("Talk to Forever TATU:", placeholder="wahgwan, stats, quote, joke...", key="v4chat")

def speak(text):
    safe = text.replace("'", "").replace('"','').replace("\n"," ")[:300]
    js = f"""<script>var msg=new SpeechSynthesisUtterance();msg.text="{safe}";msg.rate=0.95;window.speechSynthesis.speak(msg);</script>"""
    st.components.v1.html(js, height=0)

if chat_input:
    reply = get_v4_reply(chat_input, name)
    st.session_state.db[name]["history"].append((chat_input, reply, datetime.datetime.now().strftime("%H:%M")))
    if len(st.session_state.db[name]["history"]) > 50:
        st.session_state.db[name]["history"] = st.session_state.db[name]["history"][-50:]
    save_db(st.session_state.db)
    st.session_state.last_reply = reply

if st.session_state.get("last_reply"):
    if st.button("🔊 PLAY VOICE"):
        speak(st.session_state.last_reply)

# Show forever chat
history = st.session_state.db[name]["history"]
for q, a, t in reversed(history[-15:]):
    st.chat_message("user").write(f"{name} [{t}]: {q}")
    st.chat_message("assistant").write(f"TATU Forever: {a}")

st.divider()
st.caption(f"💾 v4.0 Forever | User: {name} | {len(moods)} moods | Built by Popcaan Unruly Boss | Next v5.0: AI API!")
st.caption("Data saves forever in cloud! Even Hajia Rams call can't delete am! 😂🔥")