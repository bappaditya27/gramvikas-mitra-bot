import streamlit as st
import pandas as pd
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GramVikas Mentor", 
    page_icon="🧘", 
    layout="centered"
)

# --- 2. LOGIC ENGINE ---
def get_response(user_text):
    text = user_text.lower()
    
    if any(word in text for word in ["salary", "money", "emi", "loan", "debt"]):
        return ("With your MSc in Mathematics, you know that debt is just a variable we can solve for. "
                "Even on a ₹20,000 salary, focus on small 'micro-payments' toward your principal. "
                "Every bit of interest saved is a rupee earned for your village home.")
    
    elif any(word in text for word in ["data", "python", "analytics", "course", "google"]):
        return ("This is the 'pivot point' of your life. The Google Data Analytics course is more than a certificate; "
                "it's your ticket out of the late-night shift. Keep your focus on SQL and Python today.")
    
    elif any(word in text for word in ["tired", "exhausted", "hard", "stressed", "concentrix"]):
        return ("I hear you. The grind at Concentrix is tough, but it's temporary. You are working hard now "
                "so your future self can work smart. Take 5 minutes to breathe, then look at your goal again.")
    
    elif any(word in text for word in ["village", "ngo", "home", "construction"]):
        return ("Your dream of a load-bearing concrete home in your village is a powerful anchor. "
                "Don't lose sight of it. Your village society project is proof that you are a leader.")
    
    return "I am with you. Tell me more about your day, your studies, or your financial goals."

# --- 3. UI & CHAT INTERFACE ---
st.title("🧘 GramVikas Mentor")
st.markdown("---")

# Sidebar for Mood Tracking
st.sidebar.header("How is your mind today?")
mood_score = st.sidebar.select_slider(
    "Your Stress Level (1 = Calm, 10 = High Stress)",
    options=range(1, 11),
    value=5
)
if mood_score > 7:
    st.sidebar.warning("Stress is high. Maybe focus on a light Python task tonight instead of heavy math?")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste. I am your mentor. How can I support your growth today?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
if prompt := st.chat_input("Message your mentor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
