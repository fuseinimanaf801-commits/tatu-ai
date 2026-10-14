import streamlit as st
import os

st.set_page_config(page_title="TATU AI - ChatGPT Brain", page_icon="🧠", layout="wide")

# --- API KEY ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = os.getenv("OPENAI_API_KEY", "")

# --- CHECK BRAIN ---
has_brain = False
client = None
if api_key and api_key.startswith("gsk_"):
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        has_brain = True
    except:
        has_brain = False

# --- SESSION STATE FIX ---
if "db" not in st.session_state:
    st.session_state.db = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Fix old bad data automatically
try:
    for k in list(st.session_state.db.keys()):
        cleaned = []
        for item in st.session_state.db[k]:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                cleaned.append(item)
        st.session_state.db[k] = cleaned
except:
    st.session_state.db = {}

# --- HEADER ---
st.title("🇬🇭 TATU AI v6.0")

if has_brain:
    st.success("🧠🔥 CHATGPT BRAIN ACTIVE! Ask ANYTHING!")
else:
    st.warning("⚠️ Add Groq API Key in Secrets to activate ChatGPT Brain")

# --- CHAT DISPLAY - FIXED LINE 84 BUG ---
# This replaces the old buggy line
chat_container = st.container()
with chat_container:
    # Show chat history
    if "chat_history" in st.session_state:
        for item in reversed(st.session_state.chat_history[-20:]):
            try:
                # FIXED: Safe unpacking - handles 2, 3 or more values
                if isinstance(item, (list, tuple)):
                    role = item[0] if len(item) > 0 else "user"
                    content = item[1] if len(item) > 1 else ""
                else:
                    role = "user"
                    content = str(item)

                if role == "user":
                    st.chat_message("user").write(content)
                else:
                    st.chat_message("assistant").write(content)
            except:
                continue

# Also fix db display if you use db
if "db" in st.session_state and st.session_state.db:
    for n in list(st.session_state.db.keys())[:1]: # show first
        try:
            for item in reversed(st.session_state.db[n][-20:]):
                try:
                    a = item[0] if len(item) > 0 else ""
                    b = item[1] if len(item) > 1 else ""
                    # your old logic here if needed
                except:
                    continue
        except:
            pass

# --- CHAT INPUT ---
prompt = st.chat_input("Ask TATU anything...")

if prompt:
    # Save user message
    st.session_state.chat_history.append(("user", prompt))
    if "general" not in st.session_state.db:
        st.session_state.db["general"] = []
    st.session_state.db["general"].append(("user", prompt))

    st.chat_message("user").write(prompt)

    # Get AI response
    if has_brain and client:
        with st.chat_message("assistant"):
            with st.spinner("TATU dey think..."):
                try:
                    # Build messages for Groq
                    messages = [{"role": "system", "content": "You are TATU AI, created by Fuseini Manaf in Ghana. You are helpful, smart, and friendly like ChatGPT. Answer everything."}]
                    for r, c in st.session_state.chat_history[-10:]:
                        role = "user" if r == "user" else "assistant"
                        messages.append({"role": role, "content": c})
                    messages.append({"role": "user", "content": prompt})

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=messages,
                        temperature=0.7,
                        max_tokens=1000
                    )
                    answer = response.choices[0].message.content

                    st.write(answer)
                    st.session_state.chat_history.append(("assistant", answer))
                    st.session_state.db["general"].append(("assistant", answer))
                except Exception as e:
                    st.error(f"Brain error: {e}")
                    st.write("I be TATU, but my brain need small rest. Try again!")
    else:
        with st.chat_message("assistant"):
            st.write("Add your Groq API key for ChatGPT brain! I'm TATU, built by Manaf in Ghana 🇬🇭")
            st.session_state.chat_history.append(("assistant", "Add API key to activate me!"))

st.sidebar.title("TATU Controls")
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.db = {}
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("Built by **Fuseini Manaf** 🇬🇭")
st.sidebar.markdown("v6.0 - ChatGPT Brain Active")
