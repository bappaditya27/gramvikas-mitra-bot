import streamlit as st
import random

# --- 1. CRISIS & EMPATHY LOGIC ---
def get_mentor_response(user_text, stress_level):
    text = user_text.lower()
    
    # EMERGENCY / CRISIS DETECTION
    # If things are very dark, the bot must stop talking about money/career.
    crisis_keywords = ["harm", "hurt", "worst", "anger", "die", "suicide", "hate"]
    if any(word in text for word in crisis_keywords) or stress_level >= 9:
        return ("I'm stopping the 'data talk' right now because I can hear how much pain you're in. "
                "Anger and thoughts of self-harm are heavy burdens to carry after a long shift. "
                "Please, before we talk about careers or math, reach out to someone—a friend, Hia, "
                "or a professional. You are worth more than any job or any salary. "
                "Can you promise me you'll take a moment to just breathe and drink some water?")

    # FINANCIAL / CAREER LOGIC (Only if not in crisis)
    if any(word in text for word in ["salary", "money", "loan", "emi"]):
        responses = [
            f"Debt is just a math problem, but your peace of mind is not. Let's tackle one small part of it today.",
            f"I know ₹20,000 feels small for the effort you put in at Concentrix. It's temporary fuel for your journey.",
            f"Don't let the EMI define your worth. You are a mathematician building a future."
        ]
        return random.choice(responses)

    elif any(word in text for word in ["data", "analytics", "python", "google"]):
        return ("Focusing on your studies is your ticket to a new life in Gurgaon. "
                "Even 10 minutes of SQL tonight is a victory over a bad day.")

    # FALLBACKS (To avoid repetition)
    else:
        fallbacks = [
            "I'm listening. Tell me more about what happened today at work—did something specific trigger that anger?",
            "You mentioned feeling 'not good.' Is it the financial pressure, or just the exhaustion of the shift?",
            "Sometimes it helps to write it out. I'm here to hold the space for you. What's on your mind?"
        ]
        return random.choice(fallbacks)

# --- 2. THE APP INTERFACE ---
st.title("🧘 GramVikas Mentor")

# Sidebar for Context
st.sidebar.title("Your State")
current_stress = st.sidebar.slider("Stress Level", 1, 10, 5)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Chat Input
if prompt := st.chat_input("Speak your mind..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get the logic-based response
    response = get_mentor_response(prompt, current_stress)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
