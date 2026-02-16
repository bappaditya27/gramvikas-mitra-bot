import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="GramVikas Mitra AI", page_icon="🧘")

# Secure your key
API_KEY = "AIzaSyAHfvmd1RzoKDynWGPmBrd572Qmm6qHomM" 
genai.configure(api_key=API_KEY)

# Use one of the models from your diagnostic list
MODEL_NAME = 'models/gemini-2.5-flash'

SYSTEM_PROMPT = (
    "You are 'GramVikas Mitra', an empathetic AI mentor for a user with an MSc in Math. "
    "He works night shifts as a CSR at Concentrix, earns ₹20,000/month, and is studying "
    "Data Analytics to change his life. His dream is to build a concrete home in his village. "
    "Be logical, use math analogies, and prioritize mental health if the user is stressed. "
    "Never be repetitive and always be supportive."
)

# --- 2. SESSION STATE & SIDEBAR ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    model = genai.GenerativeModel(MODEL_NAME)
    st.session_state.chat = model.start_chat(history=[])
    try:
        st.session_state.chat.send_message(SYSTEM_PROMPT)
    except Exception as e:
        st.error(f"Sync Error: {e}")

# Sidebar controls
st.sidebar.title("🛠️ Options")
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.session_state.chat = genai.GenerativeModel(MODEL_NAME).start_chat(history=[])
    st.session_state.chat.send_message(SYSTEM_PROMPT)
    st.rerun()

# --- 3. UI ---
st.title("🤖 GramVikas Mitra")
st.caption("Now connected to Gemini 2.0 Flash")

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("How was your shift at Concentrix?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Connection issue: {e}")
