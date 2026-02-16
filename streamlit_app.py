import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="GramVikas Mitra AI", page_icon="🧘")

# Your API Key
API_KEY = "AIzaSyAHfvmd1RzoKDynWGPmBrd572Qmm6qHomM" 
genai.configure(api_key=API_KEY)

# Using a standard model name that usually works everywhere
MODEL_NAME = 'gemini-1.5-flash'

SYSTEM_PROMPT = (
    "You are 'GramVikas Mitra', an empathetic AI mentor. The user has an MSc in Math, "
    "works night shifts at Concentrix, and is studying Data Analytics. "
    "Goal: Build a concrete house in his village. "
    "Be logical, use math analogies, and prioritize mental health if the user is stressed."
)

# --- 2. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "chat" not in st.session_state:
    model = genai.GenerativeModel(MODEL_NAME)
    st.session_state.chat = model.start_chat(history=[])
    # Send system instructions
    try:
        st.session_state.chat.send_message(SYSTEM_PROMPT)
    except Exception as e:
        st.error(f"Brain Sync Error: {e}")

# --- 3. UI ---
st.title("🤖 GramVikas Mitra")
st.caption("AI Mentor for Career & Life")

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("How was your shift?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"I'm having trouble thinking right now: {e}")
