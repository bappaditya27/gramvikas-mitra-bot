import streamlit as st
import pandas as pd

st.set_page_config(page_title="GramVikas Mentor", page_icon="🧘")

# --- CUSTOM THEME ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 10px; padding: 15px; }
    .stChatFloatingInputContainer { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZING USER DATA ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste. I am your GramVikas Mentor. I am here to help you manage your journey from Concentrix to a Data Analyst role, and finally to building your dream village home. How are you feeling about your finances or career today?"}
    ]

# --- THE MENTOR'S BRAIN (LOGIC) ---
def generate_mentor_response(user_text):
    text = user_text.lower()
    
    # 1. EMPATHY FOR WORK STRESS
    if any(word in text for word in ["tired", "stressed", "work", "hard", "late", "concentrix"]):
        return ("I understand that the late shifts at Concentrix are exhausting. It is not easy to manage "
                "customer support while dreaming of a larger career. But remember, this role is funding your "
                "education. You are earning ₹20,000 today so that you can earn ₹60,000 tomorrow. "
                "Take a deep breath. Have you spent even 15 minutes on your Data Analytics course today?")

    # 2. FINANCIAL GUIDANCE (MATH-BASED)
    elif any(word in text for word in ["money", "salary", "buy", "spend", "expensive"]):
        return ("As a Mathematician, you know that every rupee has an opportunity cost. If you spend "
                "unnecessarily now, it takes away a brick from your village home. Let's look at the numbers: "
                "Your current ₹20,000 salary is tight, but if we optimize your EMI payments, we can find a "
                "path to peace. Shall we calculate your savings potential for this month?")

    # 3. CAREER MOTIVATION
    elif any(word in text for word in ["data", "python", "analytics", "career", "future", "msc"]):
        return ("Your MSc in Mathematics is your superpower. Most Data Analysts have the tools but not the "
                "logic—you have the logic. Once you finish the 'Foundations' course, your profile will be "
                "much stronger for jobs in Gurgaon and NCR. Keep pushing. You are close to a breakthrough.")

    # 4. VILLAGE & NGO FOCUS
    elif any(word in text for word in ["village", "ngo", "home", "society"]):
        return ("Your commitment to your village is what defines you. Building a load-bearing structure for "
                "your home is a beautiful goal. Don't let the daily grind make you forget the soil you come from. "
                "How is the progress with the Village Society project?")

    # DEFAULT RESPONSE
    else:
        return ("I am listening. Whether it is about your EMI stress, your Python practice, or your "
                "village dreams, tell me more. I want to help you structure your thoughts logically.")

# --- DISPLAY CHAT ---
st
