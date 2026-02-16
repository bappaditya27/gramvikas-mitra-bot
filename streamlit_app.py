import streamlit as st
import google.generativeai as genai
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="GramVikas Mitra AI", page_icon="🧘")

API_KEY = "AIzaSyAHfvmd1RzoKDynWGPmBrd572Qmm6qHomM" 
genai.configure(api_key=API_KEY)

# Using the first model from your verified list
MODEL_NAME = 'models/gemini-2.5-flash'

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
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        st.session_state.chat = model.start_chat(history=[])
        # Using a safer way to send the initial prompt
        st.session_state.chat.send_message(SYSTEM_PROMPT)
    except Exception as e:
        st.error(f"Setup Error: {e}. Please check if the model name is correct.")

# --- 3. AUTO-RETRY LOGIC ---
def send_message_with_retry(prompt, max_retries=3, delay=25):
    for i in range(max_retries):
        try:
            response = st.session_state.chat.send_message(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                st.warning(f"Quota reached. Waiting {delay}s... (Attempt {i+1}/{max_retries})")
                time.sleep(delay)
            elif "404" in error_msg:
                return f"Model Error: The name '{MODEL_NAME}' was not recognized by the API."
            else:
                raise e
    return "Still hitting limits. Let's try again in a few minutes."

# --- 4. UI ---
st.title("🤖 GramVikas Mitra")
st.caption(f"Powered by {MODEL_NAME}")

# Sidebar
st.sidebar.title("🛠️ Tools")
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat = genai.GenerativeModel(MODEL_NAME).start_chat(history=[])
    try: st.session_state.chat.send_message(SYSTEM_PROMPT)
    except: pass
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
        with st.spinner("Analyzing..."):
            try:
                ai_response = send_message_with_retry(prompt)
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Critical System Error: {e}")
