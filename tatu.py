import streamlit as st
import datetime, json, os, random

st.set_page_config(page_title="TATU v5.0 Fixed", page_icon="🥔", layout="centered")

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

st.markdown("<h1 style='text-align:center'>🥔 TATU v5.0 FIXED 🇬🇭<br>REAL AI 🧠</h1>", unsafe_allow_html=True)

has_ai = False
try:
    if "OPENAI_API_KEY" in st.secrets:
        has_ai = True
except:
    has_ai = False

if has_ai:
    st.success("🧠 REAL AI CONNECTED!")
else:
    st.warning("Safe Mode - Add free AI key for super brain!")
    st.info("Get FREE key: console.groq.com -> Create Key -> Streamlit Settings -> Secrets -> OPENAI_API_KEY = gsk_...")

name = st.text_input("Name:", value="Manaf").strip().title()
if not name:
    st.stop()

if name not in st.session_state.db:
    st.session_state.db[name] = {"moods": [], "history": [], "goal": "", "joined": str(datetime.date.today())}
    save_db(st.session_state.db)

moods = st.session_state.db[name]["moods"]
c1,c2 = st.columns(2)
c1.metric(f"{name} Moods", len(moods))
c2.metric("AI", "REAL" if has_ai else "SAFE")

goal = st.text_input("Goal:", value=st.session_state.db[name].get("goal",""))
if st.button("Save Goal"):
    st.session_state.db[name]["goal"] = goal
    save_db(st.session_state.db)
    st.success("Saved!")

mood = st.selectbox("Mood:", ["😊 Happy","🔥 Unruly","😔 Low","😴 Tired","😤 Stressed","🥳 Celebrating"])
if st.button("Save Mood"):
    st.session_state.db[name]["moods"].append({"mood":mood,"time":datetime.datetime.now().strftime("%d %b %H:%M")})
    save_db(st.session_state.db)
    st.balloons()

if moods:
    d={}
    for x in moods: d[x["mood"]]=d.get(x["mood"],0)+1
    st.bar_chart(d)

st.divider()
st.subheader("Chat - Ask Anything")

def unruly_brain(msg, name):
    m=msg.lower()
    if "wahgwan" in m or "wagwan" in m or m in ["yo","yow"]:
        return f"YOWWW {name}! v5.0 FIXED! {len(moods)} moods saved! Ask who is Popcaan!"
    if "stats" in m:
        return f"Stats: {name} has {len(moods)} moods, Goal: {st.session_state.db[name].get('goal')}"
    if "popcaan" in m or "quote" in m:
        return f"Family over money, loyalty over royalty! Big up {name}! Unruly!"
    if "who is popcaan" in m:
        return f"Popcaan is Jamaican dancehall king, Unruly Boss! Like you {name}!"
    return f"Big up {name}! You say {msg} - v5.0 Fixed hears you!"

def real_ai_brain(prompt, name):
    if not has_ai:
        return unruly_brain(prompt, name)
    try:
        from openai import OpenAI
        key = st.secrets["OPENAI_API_KEY"]
        base = "https://api.groq.com/openai/v1" if key.startswith("gsk_") else None
        client = OpenAI(api_key=key, base_url=base) if base else OpenAI(api_key=key)
        model = "llama-3.1-8b-instant" if key.startswith("gsk_") else "gpt-4o-mini"
        system = f"You are TATU v5.0 built by {name} from Kumasi Ghana. Helpful, short, Unruly vibes."
        r = client.chat.completions.create(model=model, messages=[{"role":"system","content":system},{"role":"user","content":prompt}], max_tokens=350)
        return r.choices[0].message.content
    except Exception as e:
        return unruly_brain(prompt, name) + f" (AI error: {str(e)[:50]})"

q=st.text_input("Talk:", placeholder="Who is Popcaan? Stats? Quote?")

if q:
    ans = real_ai_brain(q, name)
    st.session_state.db[name]["history"].append((q, ans))
    st.session_state.db[name]["history"] = st.session_state.db[name]["history"][-20:]
    save_db(st.session_state.db)
    st.session_state.last = ans

if st.session_state.get("last"):
    st.write(f"TATU: {st.session_state.last}")
    if st.button("PLAY VOICE"):
        safe=st.session_state.last.replace("'","").replace('"',"")[:300]
        js=f"<script>var u=new SpeechSynthesisUtterance();u.text='{safe}';speechSynthesis.speak(u);</script>"
        st.components.v1.html(js,height=0)

for item in reversed(st.session_state.db[name]["history"][-10:]):
    try:
        if len(item)>=2:
            st.write(f"You: {item[0]}")
            st.write(f"TATU: {item[1]}")
    except:
        pass

st.caption("v5.0.1 Fixed - No syntax error!")