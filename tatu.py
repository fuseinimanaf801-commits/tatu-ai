import streamlit as st
import datetime, json, os, random

st.set_page_config(page_title="TATU v4.6 Fixed", page_icon="🥔", layout="centered")

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

st.markdown("<h1 style='text-align:center'>🥔 TATU v4.6 🇬🇭<br>ERROR FIXED ✅</h1>", unsafe_allow_html=True)
st.success("✅ Bug fixed! Chat go work now!")

name = st.text_input("Name:", placeholder="Manaf").strip().title()
if not name:
    st.info("Enter name!")
    st.stop()

if name not in st.session_state.db:
    st.session_state.db[name] = {"moods": [], "history": [], "goal": "", "joined": str(datetime.date.today())}
    save_db(st.session_state.db)

moods = st.session_state.db[name]["moods"]
st.metric(f"{name} Moods Forever", len(moods))

goal = st.text_input("Goal:", value=st.session_state.db[name].get("goal",""))
if st.button("Save Goal"):
    st.session_state.db[name]["goal"] = goal
    save_db(st.session_state.db)
    st.success(f"Saved: {goal}")

mood = st.selectbox("Mood:", ["😊 Happy","🔥 Unruly","😔 Low","😴 Tired","😤 Stressed","🥳 Celebrating"])
if st.button("Save Mood 💾"):
    st.session_state.db[name]["moods"].append({"mood":mood,"time":datetime.datetime.now().strftime("%d %b %H:%M")})
    save_db(st.session_state.db)
    st.balloons()
    st.success(f"Saved: {mood}")

if moods:
    d={}
    for x in moods: d[x["mood"]]=d.get(x["mood"],0)+1
    st.bar_chart(d)

st.divider()
st.subheader("Chat - Fixed!")

def reply_func(msg, name):
    ml=msg.lower()
    if "wahgwan" in ml or ml in ["yo","yow","wagwan","wah gwan"]:
        return f"YOWWW {name}! v4.6 FIXED! {len(moods)} moods! Wah gwaan! 🔥"
    if "stats" in ml:
        return f"📊 {name}: {len(moods)} moods, Goal: {st.session_state.db[name].get('goal','None')}"
    if "quote" in ml or "popcaan" in ml:
        return f"👑 Family over money, loyalty over royalty! Big up {name}!"
    return f"Big up {name}! You say '{msg}' - Fixed edition dey work!"

q=st.text_input("Talk:", placeholder="wahgwan, stats, quote")

def speak(text):
    safe=text.replace("'","").replace('"',"")[:300]
    js=f"""<script>var m=new SpeechSynthesisUtterance();m.text="{safe}";speechSynthesis.speak(m);</script>"""
    st.components.v1.html(js,height=0)

if q:
    r=reply_func(q,name)
    # FIXED: save as 2 items only (no time bug)
    st.session_state.db[name]["history"].append((q,r))
    # Keep only last 20
    st.session_state.db[name]["history"] = st.session_state.db[name]["history"][-20:]
    save_db(st.session_state.db)
    st.session_state.last=r

if st.session_state.get("last"):
    st.write(f"TATU: {st.session_state.last}")
    if st.button("🔊 PLAY VOICE"):
        speak(st.session_state.last)

# FIXED LOOP - THIS WAS THE ERROR!
# Old: for a,b in reversed(history) but history had 3 items sometimes
# New: handles both 2 and 3 items
st.write("---")
for item in reversed(st.session_state.db[name]["history"][-15:]):
    try:
        if len(item) == 3:
            qq, aa, tt = item
            st.write(f"You [{tt}]: {qq}")
            st.write(f"TATU: {aa}")
        else:
            qq, aa = item
            st.write(f"You: {qq}")
            st.write(f"TATU: {aa}")
    except:
        st.write(f"Chat: {item}")

st.caption("v4.6 Fixed - Error solved! Built by Popcaan")