import streamlit as st
import google.generativeai as genai
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="GramVikas Mitra AI", page_icon="🧘")

API_KEY = "AIzaSyAHfvmd1RzoKDynWGPmBrd572Qmm6qHomM" 
genai.configure(api_key=API_KEY)

# Using 1.5-Flash for better free-tier stability
MODEL_NAME = 'models/gemini-1.5-flash-latest'

SYSTEM_PROMPT = (
    "You are 'GramVikas Mitra', an empathetic AI mentor for a user with an MSc in Math. "
    "He works night shifts as a CSR at Concentrix, earns ₹20,000/month, and is studying "
    "Data Analytics. Goal: Build a concrete home in his village. "
    "Be logical, use math analogies, and prioritize mental health if the user is stressed."
)

# --- 2. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    model = genai.GenerativeModel(MODEL_NAME)
    st.session_state.chat = model.start_chat(history=[])
    # The system prompt usually doesn't hit quota, but we wrap it just in case
    try:
        st.session_state.chat.send_message(SYSTEM_PROMPT)
    except:
        pass

# --- 3. AUTO-RETRY LOGIC ---
def send_message_with_retry(prompt, max_retries=3, delay=25):
    """Attempts to send a message and retries if a quota error occurs."""
    for i in range(max_retries):
        try:
            response = st.session_state.chat.send_message(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                st.warning(f"Quota exceeded. Retrying in {delay} seconds... (Attempt {i+1}/{max_retries})")
                time.sleep(delay)
            else:
                raise e # Raise other errors (like connection issues) normally
    return "I'm still hitting a quota limit. Let's try again in a minute."

# --- 4. UI ---
st.title("🤖 GramVikas Mitra")
st.caption("AI Mentor with Auto-Retry Protection")

# Sidebar
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat = genai.GenerativeModel(MODEL_NAME).start_chat(history=[])
    st.session_state.chat.send_message(SYSTEM_PROMPT)
    st.rerun()

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Talk to me..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                ai_response = send_message_with_retry(prompt)
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Error: {e}")
