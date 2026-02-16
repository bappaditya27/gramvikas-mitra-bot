import streamlit as st
import google.generativeai as genai

# Secure your key
API_KEY = "AIzaSyAHfvmd1RzoKDynWGPmBrd572Qmm6qHomM" 
genai.configure(api_key=API_KEY)

# --- NEW: DIAGNOSTIC SIDEBAR ---
st.sidebar.title("🛠️ System Diagnostics")
if st.sidebar.button("List Available Models"):
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        st.sidebar.write("Your key supports these models:")
        st.sidebar.json(models)
    except Exception as e:
        st.sidebar.error(f"Could not fetch models: {e}")

# --- UPDATED MODEL SELECTION ---
# Try 'gemini-1.5-flash-latest' or 'gemini-pro' if 'gemini-1.5-flash' fails
MODEL_NAME = 'gemini-1.5-flash-latest' 

# ... (rest of your chat code remains the same)
