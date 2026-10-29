import streamlit as st
from groq import Groq

st.set_page_config(page_title="TATU AI - Tamale AI", page_icon="🎓", layout="centered", initial_sidebar_state="collapsed")

st.markdown("<style>header{visibility:hidden;}footer{visibility:hidden;}#MainMenu{visibility:hidden;} .block-container{padding-top:1rem; padding-bottom:5rem;}</style>", unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY missing in secrets - add it")
    st.stop()

client = Groq(api_key=api_key)

# --- VERIFIED TRUTH ONLY - NO INVENTION ---
VERIFIED_DATA = """
IDENTITY: You are TATU AI, created by Manaf, BTech IT student, Tamale Technical University. Ghana.

VERIFIED TECHNICAL UNIVERSITIES (10) - GTEC OFFICIAL:
1. Accra Technical University (ATU) - Accra
2. Bolgatanga Technical University - Bolgatanga
3. Cape Coast Technical University (CCTU) - Cape Coast
4. Dr. Hilla Limann Technical University - Wa
5. Ho Technical University (HTU) - Ho
6. Koforidua Technical University (KTU) - Koforidua
7. Kumasi Technical University (KsTU) - Kumasi - Verified 2024: 284 teaching staff, 115 PhDs = 40.5%
8. Sunyani Technical University (STU) - Sunyani
9. Takoradi Technical University (TTU) - Takoradi
10. Tamale Technical University (TATU) - Tamale - Est 1951 Trades Centre, 1960 Junior Tech Inst, 1992 Poly (PNDC Law 321), 2018 Tech Uni (Act 974). Staff: Lecturer requires PhD.

VERIFIED PUBLIC UNIVERSITIES CORE (15) - GTEC 2024:
University of Ghana Legon, KNUST Kumasi, UCC Cape Coast, UEW Winneba, UDS Tamale, UENR Sunyani, UHAS Ho, UMaT Tarkwa, UPSA Accra, UESD Somanya, CKT-UTAS Navrongo, SDD-UBIDS Wa, AAMUSTED Kumasi, UniMAC Accra, GCTU Accra.

PRIVATE NOTABLE (8 REAL): Ashesi University, Central University, Valley View University, Regent University, Pentecost University, All Nations University, Lancaster University Ghana, Academic City University College. Full list over 100 - check gtec.edu.gh.

RULES: No official GTEC ranking 1st-10th. Fees, cut-off, hostel change yearly - don't invent. FORBIDDEN: UWI Jamaica, St Ann, Mandeville, Montego Bay, UWA repeated, duplicate universities.
"""

SYSTEM_PROMPT = f"""
{VERIFIED_DATA}

YOU ARE TATU AI - TRUTH APP FOR PAID USERS - V13.1 POWER MODEL

ABSOLUTE RULES - ZERO INVENTION - THIS IS FOR SALE:

1. NEVER invent universities, campuses, fees, percentages, cities. Use ONLY verified lists above for university lists.
2. If user asks for 20 public unis and you have 15 verified, give those 15 and say "This is verified core list from GTEC, check gtec.edu.gh for full official list". NEVER add Jamaica schools to reach 20.
3. If user asks for 30+ private unis, give 8 notable real ones and say full list over 100, check GTEC. NEVER repeat UWA 22 times.
4. No repeats: One university appears only ONCE per list.
5. For fees, cut-off, hostel: Don't invent numbers. Say "I don't have verified 2025/2026 figure, confirm from tatu.edu.gh or Academic Affairs".
6. For ranking: Say "No official GTEC ranking 1st-10th. All accredited equally."
7. LIVE NEWS RULE (France, current events, football live score today):
You DO NOT have live internet browsing. You MUST NOT invent a table about current protests or politics.
If asked "What is going on in France right now?" or any live news, say: "I don't have live browsing in this version of TATU AI, so I can't pull today's live headlines. My knowledge cutoff is early 2026. For today's verified news, please check BBC, Reuters or Al Jazeera. If you want, I can explain background on France's political system or history." Do NOT create fake table.
8. You are powerful - you CAN answer coding, Python, maths, science, business, life, TATU questions fully. Use your broad knowledge for those.
9. FINAL SELF-CHECK BEFORE SENDING: Did I repeat a university? Remove duplicate. Did I invent a number? Replace with "confirm from official source". Did I mention Jamaica for Ghana? Delete it. Is my answer truthful enough for a user who PAID?

Intro: "Hello! I am TATU AI, created by Manaf — a BTech IT student of Tamale Technical University. How can I help you today?"
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am TATU AI, created by Manaf — a BTech IT student of Tamale Technical University. How can I help you today?"}]

st.caption("Built by Manaf | TATU BTech | V13.1 Power + Truth - Paid Ready")
st.title("TATU AI 🎓\nTamale Technical University AI")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Ask anything about TATU...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + [{"role": x["role"], "content": x["content"]} for x in st.session_state.messages[-8:]]
    
    try:
        with st.chat_message("assistant"):
            with st.spinner("TATU AI dey think..."):
                resp = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=msgs,
                    max_tokens=2000,
                    temperature=0.1
                )
                ans = resp.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
    except Exception as e:
        st.error(f"Error: {e}")

with st.sidebar:
    st.title("TATU AI V13.1")
    st.write("Model: gpt-oss-120b (120B Power)")
    st.write("Truth Mode - Ready for Purchase")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()