import streamlit as st
import datetime, json, os, random

st.set_page_config(page_title="TATU v5.0 Real AI", page_icon="🥔", layout="centered")

# --- FOREVER DB ---
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

st.markdown("<h1 style='text-align:center'>🥔 TATU v5.0 🇬🇭<br>REAL AI 🧠</h1>", unsafe_allow_html=True)

# --- CHECK AI ---
has_ai = False
ai_status = "Unruly Brain v4.6 (Safe Mode)"
try:
    if "OPENAI_API_KEY" in st.secrets:
        has_ai = True
        ai_status = "🧠 REAL AI CONNECTED!"
except:
    has_ai = False

if has_ai:
    st.success(f"{ai_status} - Ask anything!")
else:
    st.warning("⚠️ Safe Mode - Add free AI key for super brain!")
    with st.expander("🔑 FREE AI Key - 1 min (Groq)"):
        st.markdown("""
        **Get FREE key (no card):**
        1. Go to **console.groq.com** -> Sign up
        2. Create API Key -> Copy `gsk_...`
        3. Streamlit App -> Manage app -> Settings -> Secrets -> Paste: