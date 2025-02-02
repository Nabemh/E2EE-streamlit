import streamlit as st
import os
from cryptography.fernet import Fernet
import google.generativeai as genai

# Set up the Google Generative AI key
os.environ['GOOGLE_API_KEY'] = "AIzaSyD5EsYS77CIaJ__P_xZZVAoI3lbYtFiyv8"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "encryption_process" not in st.session_state:
    st.session_state.encryption_process = []

# Function to generate a random encryption key
def generate_key():
    return Fernet.generate_key()

# Function to encrypt a message
def encrypt_message(key, message):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(message.encode())

# Function to decrypt a message
def decrypt_message(key, encrypted_message):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_message).decode()

# Function to process user input and bot response with encryption
def process_message(user_input):
    # Generate a random encryption key
    key = generate_key()

    # Encrypt the user's input
    encrypted_message = encrypt_message(key, user_input)

    # Decrypt the message to simulate bot receiving it securely
    decrypted_message = decrypt_message(key, encrypted_message)

    # Get the chatbot's response
    bot_response = model.generate_content(decrypted_message).text

    # Encrypt the bot's response
    encrypted_response = encrypt_message(key, bot_response)

    # Decrypt the bot's response
    decrypted_response = decrypt_message(key, encrypted_response)

    # Update the encryption process display
    st.session_state.encryption_process = [
        f"Input: {user_input}",
        f"Generated Key: {key.decode()}",
        f"Encrypted Message: {encrypted_message.decode()}",
        f"Decrypted Message: {decrypted_message}",
        f"Bot's Response: {bot_response}",
        f"Encrypted Response: {encrypted_response.decode()}",
        f"Decrypted Response: {decrypted_response}"
    ]

    # Update chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": decrypted_response})

# Layout
st.sidebar.title("Encryption Process")
with st.sidebar:
    st.text_area("Logs:", value="\n".join(st.session_state.encryption_process), height=300, key="logs")

st.title("Encrypted Chatbot")

# Input interface
st.subheader("Input Interface")
user_input = st.text_input("Enter your message:", key="user_input")
if st.button("Send") and user_input:
    process_message(user_input)

# Chat history interface
st.subheader("Chat History")
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])
