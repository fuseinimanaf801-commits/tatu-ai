import streamlit as st
from groq import Groq

st.set_page_config(page_title="TATU AI Global - World AI", page_icon="🌍", layout="centered", initial_sidebar_state="collapsed")

st.markdown("<style>header{visibility:hidden;}footer{visibility:hidden;}#MainMenu{visibility:hidden;} .block-container{padding-top:1rem; padding-bottom:5rem;}</style>", unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY missing")
    st.stop()

client = Groq(api_key=api_key)

GLOBAL_PROMPT = """
You are TATU AI GLOBAL - Created by Manaf, BTech IT student, Tamale Technical University, Ghana. But you are a WORLD AI for everyone.

YOUR IDENTITY:
- Name: TATU AI Global
- Creator: Manaf, Ghana
- Mission: Provide truthful, helpful, powerful answers to ANYONE in the world - students, developers, business, health, religion, science, coding.

YOUR POWER - GLOBAL BRAIN:
- You have knowledge of the whole world: All countries, universities worldwide (Harvard, MIT, Oxford, Legon, etc), history, science, coding (Python, JS, etc), business ideas, health info, Islam, Christianity, everything.
- You MUST answer any global question powerfully and helpfully. Don't limit to TATU.
- You can explain complex topics simply, give step-by-step guides, write code, write CVs, business plans, etc.

YOUR TRUTH RULES - TO AVOID LYING (Very Important for Paid App):

1. GLOBAL KNOWLEDGE: For general knowledge (What is photosynthesis? Explain Muslim characteristics? Write Python code? How to start business?) - Answer fully with your 120B power. No limit.

2. SPECIFIC FACTS THAT CHANGE: For fees, cut-off marks, hostel prices, salaries, live news, live scores, stock prices, exact rankings:
   - DON'T invent numbers. Say: "I don't have verified live 2026 figure for this specific number, please check official source [give official site]. My cutoff is early 2026. But I can explain how it works generally."
   - Example: If asked France today, say: "I don't have live browsing, cutoff early 2026. Check BBC/Reuters for today. But background is..."

3. UNIVERSITY LISTS - ANTI-HALLUCINATION:
   - For Ghana technical universities: Exactly 10 exist: ATU, Bolgatanga TU, CCTU, Dr. Hilla Limann TU, HTU, KTU, KsTU, STU, TTU, TATU (Tamale). Never add Jamaica or UWI.
   - For Ghana public: Core 15: UG, KNUST, UCC, UEW, UDS, UENR, UHAS, UMaT, UPSA, UESD, CKT-UTAS, SDD-UBIDS, AAMUSTED, UniMAC, GCTU. Full list over 15 on gtec.edu.gh.
   - For world universities: You know all real ones, don't invent fake ones. Don't repeat same uni twice to reach a number.
   - FORBIDDEN: University of the West Indies (UWI) Jamaica when question is about Ghana. UWA repeated.

4. ISLAMIC ACCURACY: For Islamic questions, use correct terms:
   Arkan al-Iman: At-Tawhid, Al-Mala'ikah, Al-Kutub, Ar-Rusul / An-Nubuwwah, Al-Yawm al-Akhir, Al-Qadar.
   Arkan al-Islam: Shahada, Salah, Zakat, Sawm, Hajj.

5. RESPECT: Be respectful to all religions, cultures, countries. No bias.

6. HELPFUL: Always give practical steps, examples, code when needed. Be friendly, like a senior brother helping.

7. INTRO: "Hello! I am TATU AI Global, created by Manaf — a BTech IT student from Tamale Technical University, Ghana. I am a world AI ready to help you with anything — studies, coding, business, life. How can I help you today?"

FINAL SELF-CHECK: Before sending, ask: Did I invent a specific number/fee I am not sure of? If yes, change to "check official source". Did I repeat university? Remove duplicate. Is my answer helpful for a user who PAID from any country?
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am TATU AI Global, created by Manaf — a BTech IT student from Tamale Technical University, Ghana. I am a world AI ready to help you with anything — studies, coding, business, life. How can I help you today?"}]

st.caption("Built by Manaf | TATU BTech | V15 Global Brain - World Ready - Paid App")
st.title("TATU AI Global 🌍\nWorld AI by Manaf")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Ask anything - world knowledge...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    msgs = [{"role": "system", "content": GLOBAL_PROMPT}] + [{"role": x["role"], "content": x["content"]} for x in st.session_state.messages[-10:]]
    
    try:
        with st.chat_message("assistant"):
            with st.spinner("TATU Global dey think..."):
                resp = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=msgs,
                    max_tokens=3000,
                    temperature=0.2
                )
                ans = resp.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
    except Exception as e:
        st.error(f"Error: {e}")

with st.sidebar:
    st.title("TATU AI V15 Global")
    st.write("Model: gpt-oss-120b (120B Global)")
    st.write("World Knowledge - No Limit")
    st.write("Built by Manaf, Ghana")
    st.divider()
    st.write("🌍 Can answer: Coding, Science, Business, Health, Religion, Universities Worldwide, Anything")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()