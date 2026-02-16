import streamlit as st
import time

st.set_page_config(page_title="GramVikas Mitra", page_icon="🤖")

# --- APP STYLING ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatFloatingInputContainer { bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 GramVikas Mitra")
st.caption("Your Personal Financial Mentor & Data Analyst Assistant")

# --- INITIAL DATA (Your Context) ---
if "salary" not in st.session_state:
    st.session_state.salary = 20000
    st.session_state.debt = 50000
    st.session_state.emi = 3000
    st.session_state.messages = []

# --- CHATBOT LOGIC ---
def get_bot_response(user_input):
    user_input = user_input.lower()
    
    if "salary" in user_input or "earn" in user_input:
        return f"You currently earn ₹{st.session_state.salary} at Concentrix. Based on your MSc Math background, we should aim for a Data Analyst role paying ₹45,000+ to triple your savings."
    
    elif "debt" in user_input or "loan" in user_input:
        months = round(st.session_state.debt / st.session_state.emi)
        return f"Your current debt is ₹{st.session_state.debt}. At ₹{st.session_state.emi}/month, you'll be debt-free in about {months} months. Hang in there!"
    
    elif "village" in user_input or "home" in user_input:
        return "Building that dream home in your village is a noble goal. Every ₹1,000 you save today is a brick in that house tomorrow."
    
    elif "hi" in user_input or "hello" in user_input:
        return "Namaste! I am GramVikas Mitra. Ask me about your budget, debt, or career goals."
    
    else:
        return "That's an interesting point. As a mathematician, I'd suggest looking at how that affects your monthly net disposable income. Should we calculate that?"

# --- CHAT INTERFACE ---
# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask Mitra something..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        response = get_bot_response(prompt)
        # Simulate 'typing' feel
        message_placeholder = st.empty()
        full_response = ""
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
