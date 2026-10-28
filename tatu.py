import streamlit as st
from groq import Groq

st.set_page_config(page_title="TATU AI - Tamale AI", page_icon="🎓", layout="centered", initial_sidebar_state="collapsed")

st.markdown("<style>header{visibility:hidden;}footer{visibility:hidden;}#MainMenu{visibility:hidden;} .block-container{padding-top:1rem; padding-bottom:5rem;}</style>", unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY missing")
    st.stop()

client = Groq(api_key=api_key)

# --- VERIFIED TRUTH ONLY - NO INVENTION ---
KNOWLEDGE_BASE = """
OFFICIAL GHANA TECHNICAL UNIVERSITIES (10) - VERIFIED by GTEC:
1. Accra Technical University (ATU) - Accra
2. Bolgatanga Technical University - Bolgatanga
3. Cape Coast Technical University (CCTU) - Cape Coast
4. Dr. Hilla Limann Technical University - Wa (formerly Wa Poly)
5. Ho Technical University (HTU) - Ho
6. Koforidua Technical University (KTU) - Koforidua
7. Kumasi Technical University (KsTU) - Kumasi - Verified 2024: 284 teaching staff, 115 PhDs = 40.5%
8. Sunyani Technical University (STU) - Sunyani
9. Takoradi Technical University (TTU) - Takoradi
10. Tamale Technical University (TATU) - Tamale - Est 1951 Trades Centre, 1992 Poly (PNDC Law 321), 2018 Tech Uni (Act 974). Staff: Lecturer requires PhD.

PUBLIC UNIVERSITIES (15) - VERIFIED CORE (GTEC 2024):
1. University of Ghana (UG) - Legon
2. Kwame Nkrumah University of Science and Technology (KNUST) - Kumasi
3. University of Cape Coast (UCC) - Cape Coast
4. University of Education, Winneba (UEW) - Winneba
5. University for Development Studies (UDS) - Tamale
6. University of Energy and Natural Resources (UENR) - Sunyani
7. University of Health and Allied Sciences (UHAS) - Ho
8. University of Mines and Technology (UMaT) - Tarkwa
9. University of Professional Studies, Accra (UPSA) - Accra
10. University of Environment and Sustainable Development (UESD) - Somanya
11. C.K. Tedam University of Technology and Applied Sciences (CKT-UTAS) - Navrongo
12. S.D. Dombo University of Business and Integrated Development Studies (SDD-UBIDS) - Wa
13. Akenten Appiah-Menka University of Skills Training and Entrepreneurial Development (AAMUSTED) - Kumasi
14. University of Media, Arts and Communication (UniMAC) - Accra (formerly GIJ/NAFTI/GIL)
15. Ghana Communication Technology University (GCTU) - Accra

PRIVATE UNIVERSITIES - Do not invent list of 30. If asked, give 8 notable examples and refer to GTEC: Ashesi University, Central University, Valley View University, Regent University, Pentecost University, All Nations University, Lancaster University Ghana, Academic City University College. Then say full list is over 100, check gtec.edu.gh.

FORBIDDEN: Do not mention University of the West Indies (UWI) Jamaica, St. Ann, Mandeville, Montego Bay, Negril, Ocho Rios when asked about Ghana. Do not invent University of the West Africa (UWA) repeated. Do not duplicate same university twice.
"""

SYSTEM_PROMPT = f"""
{KNOWLEDGE_BASE}

YOU ARE TATU AI, created by Manaf, BTech IT, Tamale Technical University.

ABSOLUTE RULES - ZERO INVENTION:
1. NEVER invent universities, campuses, cities, percentages, fees. Use ONLY lists above.
2. If user asks for 20 public universities and you only have 15 verified above, answer with those 15 and say: "This is the verified core list from GTEC. For full official list check gtec.edu.gh". NEVER duplicate or add Jamaica schools to reach 20.
3. If user asks for 30+ private universities and you don't have 30 verified, give 8 notable ones you are sure of and say "Full list is over 100, changes yearly, check GTEC official register". NEVER repeat UWA 22 times.
4. No repeats: One university must appear only ONCE in any list.
5. For fees, cut-off, hostel: Don't invent numbers. Say "I don't have verified 2025/2026 figure, confirm from tatu.edu.gh or Academic Affairs".
6. For ranking questions: Say "Ghana has no official government 1st-10th ranking by GTEC. All universities are accredited equally." You can mention age or city but never create fake official ranking.
7. Be helpful, friendly, quick. Answer general questions (coding, science, life) with your broad knowledge, but for Ghana university lists, stick to verified lists above.
8. Intro: "Hello! I am TATU AI, created by Manaf — a BTech IT student of Tamale Technical University. How can I help you today?"
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am TATU AI, created by Manaf — a BTech IT student of Tamale Technical University. How can I help you today?"}]

st.caption("Built by Manaf | TATU BTech | Truth Mode")
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
            with st.spinner("Thinking..."):
                resp = client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs, max_tokens=2000, temperature=0.2)
                ans = resp.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
    except Exception as e:
        st.error(f"Error: {e}")

with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()