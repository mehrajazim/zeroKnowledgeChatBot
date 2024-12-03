from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini Pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    """Send user input to the chatbot and return its response."""
    response = chat.send_message(question, stream=True)
    return response

# Streamlit app setup
st.set_page_config(page_title="Gemini Chatbot")
st.header("Gemini LLM Chatbot")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("Enter your question:")
if st.button("Ask"):
    if user_input:
        response = get_gemini_response(user_input)
        st.session_state['chat_history'].append(("You", user_input))
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
