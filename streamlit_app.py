import streamlit as st
import time
import pandas as pd

st.set_page_config(page_title="GramVikas Mitra v2", page_icon="🧘", layout="wide")

# --- CUSTOM CSS FOR EMPATHETIC UI ---
st.markdown("""
    <style>
    .stChatMessage { background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.02); }
    .stProgress > div > div > div > div { background-color: #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "salary" not in st.session_state:
    st.session_state.update({
        "salary": 20000,
        "debt": 50000,
        "emi": 3000,
        "savings": 2000,
        "messages": [{"role": "assistant", "content": "Namaste. I know today was a long day at the office. How can I help you plan your future today?"}]
    })

# --- BRAIN: LOGICAL THINKING ENGINE ---
def analyze_intent(query):
    query = query.lower()
    
    # CASE 1: Financial Stress/Anxiety
    if any(word in query for word in ["stressed", "hard", "money", "tight", "expensive"]):
        disposable = st.session_state.salary - (st.session_state.emi + 9000) # Assuming 9k basic living
        if disposable < 2000:
            return (f"I hear you. With ₹{disposable} left after essentials, things are objectively tight. "
                    "But remember: this 20k salary is just your starting point. Your MSc in Math is an asset "
                    "most people don't have. Every module you finish in your Data course increases your 'Market Value'. "
                    "Should we look at your 'Debt-Free' date to keep the focus on the finish line?")
        return "It's a grind, but you're managing better than most. You have a surplus. Shall we allocate it to the Village Home fund?"

    # CASE 2: The "Opportunity Cost" Logic (Decision Making)
    elif "buy" in query or "spend" in query:
        # Extract potential cost from string if possible, or assume 1000
        cost = 1000 
        impact_on_debt = cost / st.session_state.emi
        return (f"If you spend ₹{cost} now, logically, it's equivalent to delaying your 'Debt-Free' goal by "
                f"approximately {impact_on_debt:.1f} weeks. Does this item bring you more joy than "
                "the peace of being debt-free?")

    # CASE 3: Career Growth Projection
    elif any(word in query for word in ["career", "future", "data", "job", "salary"]):
        new_salary = 45000
        potential_savings = new_salary - (st.session_state.emi + 12000) # Adjusted living for better role
        increase_factor = potential_savings / (st.session_state.salary - 12000)
        return (f"As a Mathematician, look at this ratio: A jump to a Data Analyst role at ₹{new_salary} "
                f"increases your saving power by **{increase_factor:.1f}x**. That’s not just a job; "
                "that's the key to your village house. Which Python chapter are we tackling tonight?")

    return "I'm processing that. Let's relate it back: Does this help your village society, your home, or your career transition?"

# --- UI LAYOUT ---
st.title("🤖 GramVikas Mitra: Your Growth Mentor")

col1, col2 = st.columns([2, 1])

with col1:
    # Chat Display
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Talk to me..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response = analyze_intent(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    st.subheader("📈 Growth Metrics")
    st.write("Current Financial Health")
    health = (st.session_state.salary - st.session_state.emi) / st.session_state.salary
    st.progress(health)
    
    st.info(f"**Debt Recovery Status:** {round((1 - (st.session_state.debt/200000))*100)}%")
    st.success("**Next Milestone:** Finish SQL Module (Data Foundations)")
