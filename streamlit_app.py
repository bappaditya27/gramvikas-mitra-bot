import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="GramVikas Mitra AI", page_icon="🧘")

# We will use your key directly here for now
# (Reminder: Later, move this to Streamlit Secrets for safety!)
API_KEY = "AIzaSyAHfvmd1RzoKDynWGPmBrd572Qmm6qHomM" 

genai.configure(api_key=API_KEY)

# --- 2. IDENTITY & BRAIN ---
# This "Persona" ensures the AI stays focused on your specific life needs
SYSTEM_PROMPT = (
    "You are 'GramVikas Mitra', an elite AI mentor for a user with an MSc in Mathematics. "
    "CONTEXT: The user works as a CSR at Concentrix (night shifts), earns ₹20,000/month, "
    "is studying the Google Data Analytics course, and dreams of building a load-bearing "
    "concrete house in his village. He supports an NGO. "
    "TONE: Compassionate, highly logical, and encouraging. Use mathematical analogies. "
    "If the user is stressed or angry, be a calming friend first. "
    "If the user asks about Python/Data, be a strict but helpful tutor."
)

model = genai.GenerativeModel('gemini-1.5-flash') # Using the fast, smart model

# --- 3. SESSION STATE (Memory) ---
if "chat" not in st.session_state:
    # Start a chat session with the system identity
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.chat.send_message(SYSTEM_PROMPT)
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. UI ---
st.title("🤖 GramVikas Mitra (Smart AI)")
st.caption("Connected to Gemini | Personalized for your Career & Life")

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("How was your shift? Or ask a Python question..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Smart Response
    with st.chat_message("assistant"):
        try:
            # We send the prompt to the AI
            response = st.session_state.chat.send_message(prompt)
            ai_text = response.text
            
            st.markdown(ai_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
        except Exception as e:
            st.error("I'm having trouble connecting to the brain. Check your internet or API key.")
