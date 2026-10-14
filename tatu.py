import streamlit as st
import datetime, json, os, random

st.set_page_config(page_title="TATU v4.5 Stable", page_icon="🥔", layout="centered")

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

st.markdown("<h1 style='text-align:center'>🥔 TATU v4.5 🇬🇭<br>STABLE 🔥</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center'>{datetime.date.today()}</p>", unsafe_allow_html=True)
st.success("✅ v4.5 Stable - Forever Save Active!")

name = st.text_input("Name:", placeholder="Manaf").strip().title()
if not name:
    st.info("Enter name!")
    st.stop()

if name not in st.session_state.db:
    st.session_state.db[name] = {"moods": [], "history": [], "goal": "", "joined": str(datetime.date.today())}
    save_db(st.session_state.db)

moods = st.session_state.db[name]["moods"]
st.metric("Moods Forever", len(moods))

goal = st.text_input("Goal:", value=st.session_state.db[name].get("goal",""))
if st.button("Save Goal"):
    st.session_state.db[name]["goal"] = goal
    save_db(st.session_state.db)
    st.success("Saved!")

m = st.selectbox("Mood:", ["😊 Happy","🔥 Unruly","😔 Low","😴 Tired","😤 Stressed","🥳 Celebrating"])
if st.button("Save Mood 💾"):
    st.session_state.db[name]["moods"].append({"mood":m,"time":datetime.datetime.now().strftime("%d %b %H:%M")})
    save_db(st.session_state.db)
    st.balloons()

if moods:
    d={}
    for x in moods: d[x["mood"]]=d.get(x["mood"],0)+1
    st.bar_chart(d)

st.divider()
st.subheader("Chat")

def reply(msg, name):
    ml=msg.lower()
    if "wahgwan" in ml or ml in ["yo","yow","wagwan"]:
        return f"YOWWW {name}! v4.5 Stable! {len(moods)} moods saved forever! 🔥"
    if "stats" in ml:
        return f"📊 {name}: {len(moods)} moods forever! Goal: {st.session_state.db[name].get('goal')}"
    if "quote" in ml:
        return f"👑 Family over money, loyalty over royalty! Big up {name}!"
    return f"Big up {name}! You say '{msg}' - v4.5 stable dey hear you!"

q=st.text_input("Talk:", placeholder="wahgwan, stats, quote")
if q:
    r=reply(q,name)
    st.session_state.db[name]["history"].append((q,r))
    save_db(st.session_state.db)
    st.session_state.last=r

if st.session_state.get("last"):
    st.write(f"TATU: {st.session_state.last}")
    if st.button("🔊 PLAY VOICE"):
        safe=st.session_state.last.replace("'","").replace('"',"")[:300]
        js=f"""<script>var m=new SpeechSynthesisUtterance();m.text="{safe}";speechSynthesis.speak(m);</script>"""
        st.components.v1.html(js,height=0)

for a,b in reversed(st.session_state.db[name]["history"][-10:]):
    st.write(f"You: {a} | TATU: {b}")

st.caption("v4.5 Stable - Black screen fixed!")