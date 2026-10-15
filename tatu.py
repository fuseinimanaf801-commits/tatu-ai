import streamlit as st
from groq import Groq

# --- PAGE SETUP ---
st.set_page_config(page_title="TATU AI v6.0", page_icon="🧠", layout="centered")

st.title("TATU AI v6.0 🧠")

# --- CHECK BRAIN ---
has_brain = False
client = None

if "OPENAI_API_KEY" in st.secrets:
    try:
        client = Groq(api_key=st.secrets["OPENAI_API_KEY"])
        has_brain = True
    except Exception as e:
        has_brain = False

# --- SHOW STATUS ---
if has_brain:
    st.success("🧠🔥 CHATGPT BRAIN ACTIVE! Ask ANYTHING!")
else:
    st.warning("⚠️ Add Groq API Key in Secrets to activate ChatGPT Brain")
    st.info("Go to Manage app > Settings > Secrets > Add OPENAI_API_KEY")

# --- CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Ask TATU anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if has_brain:
        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": "system", "content": "You are TATU AI v6.0 created by Manaf aka Popcaan de Unruly Boss. You are TATU AI, not ChatGPT. Always say you were created by Manaf aka Popcaan de Unruly Boss."}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Brain Error: {e}")
    else:
        with st.chat_message("assistant"):
            st.error("Brain not active. Add API Key in Secrets!")