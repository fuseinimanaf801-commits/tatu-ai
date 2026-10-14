import streamlit as st
import datetime, json, os, random

st.set_page_config(page_title="TATU v5.1 Smart", page_icon="🥔", layout="centered")

DB_FILE = "tatu_forever_db.json"
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}
def save_db(d):
    try:
        with open(DB_FILE, "w") as f: json.dump(d, f)
    except: pass

if "db" not in st.session_state:
    st.session_state.db = load_db()

st.markdown("<h1 style='text-align:center'>🥔 TATU v5.1 🇬🇭 SMART 🧠</h1>", unsafe_allow_html=True)
st.success("✅ v5.1 Smart Offline - No key needed! Answers photosynthesis!")

name = st.text_input("Name:", value="Manaf").strip().title()
if not name: st.stop()
if name not in st.session_state.db:
    st.session_state.db[name] = {"moods": [], "history": [], "goal": "", "joined": str(datetime.date.today())}
    save_db(st.session_state.db)

moods = st.session_state.db[name]["moods"]
st.metric(f"{name} Moods", len(moods))

# SMART BRAIN - NO API NEEDED!
def smart_brain(q, name):
    m = q.lower()
    # Science
    if "photosynthesis" in m:
        return f"🌱 Photosynthesis be how plants make food! Plants use sunlight + CO2 + water -> make sugar (glucose) + oxygen! Equation: 6CO2 + 6H2O + sunlight -> C6H12O6 + 6O2. Plants be chefs! Big up {name}! 🇬🇭"
    if "mitosis" in m or "meiosis" in m:
        return f"🧬 Mitosis = 1 cell -> 2 identical cells (for growth). Meiosis = 1 cell -> 4 different cells (for babies). Mitosis for body, meiosis for reproduction! 🔥"
    if "gravity" in m or "newton" in m:
        return f"🍎 Gravity = force wey pull everything down! Newton: F=ma. Einstein say gravity bend space-time! Why you no float go sky? Gravity hold you! {name}!"
    if "water" in m and "formula" in m:
        return "💧 Water na H2O - 2 Hydrogen + 1 Oxygen! Life no dey without am!"
    # Math
    if "2+2" in m or "2 + 2" in m:
        return f"🧮 2+2 = 4! Unruly math! {name} you smart!"
    # Popcaan
    if "who is popcaan" in m:
        return "👑 Popcaan na Jamaican dancehall superstar! Real name Andre Sutherland. Hit songs: Only Man She Want, Family. Unruly Boss! 🇯🇲"
    if "fuseini manaf" in m or "who is manaf" in m:
        return f"👑 Fuseini Manaf aka Popcaan na Kumasi boss! Built TATU v5.1 from phone! No laptop! Real Unruly dev! From Ghana to the world! {name} be legend! 🚀"
    # General
    if "wahgwan" in m or "wagwan" in m or m in ["yo","yow"]:
        return f"YOWWW {name}! v5.1 SMART! I fit answer photosynthesis, science, math now! No key needed! Ask me anything! 🔥"
    if "stats" in m:
        return f"📊 {name}: {len(moods)} moods forever, Goal: {st.session_state.db[name].get('goal','Set goal')}, Joined: {st.session_state.db[name].get('joined')}"
    if "quote" in m:
        return random.choice(["Family over money, loyalty over royalty! - Popcaan", "Unruly nuh stop till casket drop!", "Kumasi to Kingston, we run di place!", "We never fail, we only learn!"])
    if "joke" in m:
        return f"😂 Why potato never fight? Because e be TATU! 🥔 Big up {name}!"
    if "code" in m or "python" in m:
        return f"💻 Python example:\nprint('Unruly {name}!')\nfor i in range(3): print(f'Big up {{i}}')\n# TATU v5.1 from Kumasi! 🇬🇭"
    # Fallback smart
    if len(m) > 3:
        return f"🧠 Yo {name}, you ask '{q}'. My smart brain: I know photosynthesis, gravity, mitosis, math, Popcaan, coding! Try 'what is photosynthesis' or 'who is Popcaan' or 'tell me joke'! If you want ChatGPT-level, add free Groq key later! 🔥"
    return f"Big up {name}! Ask me 'what is photosynthesis' now e go work!"

q = st.text_input("Ask SMART TATU:", placeholder="What is photosynthesis? Who is Popcaan? 2+2?")

if q:
    ans = smart_brain(q, name)
    st.session_state.db[name]["history"].append((q, ans))
    st.session_state.db[name]["history"] = st.session_state.db[name]["history"][-20:]
    save_db(st.session_state.db)
    st.session_state.last = ans

if st.session_state.get("last"):
    st.write(f"TATU v5.1: {st.session_state.last}")
    if st.button("🔊 PLAY"):
        safe=st.session_state.last.replace("'","").replace('"',"")[:350]
        st.components.v1.html(f"<script>var u=new SpeechSynthesisUtterance();u.text='{safe}';speechSynthesis.speak(u);</script>",height=0)

for item in reversed(st.session_state.db[n]):
    a, b = item[:2] if len(item) >= 2 else (item[0], "")
    st.write(f"You: {a}")
    st.write(f"TATU: {b}")
    st.write("---")

st.caption("v5.1 Smart Offline - Answers science without key!")