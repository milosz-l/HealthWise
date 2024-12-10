import requests
import pandas as pd
import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import uuid
import os

# Load environment variables
from dotenv import load_dotenv

load_dotenv()


def clear_chat_history():
    st.session_state.messages = [SESSION_STATE]
    st.session_state.conversation_id = str(uuid.uuid4())


def authenticate_chatbot():
    """Authenticates the user for the Chatbot page."""
    password = os.getenv("CHATBOT_PASSWORD")

    if "is_chatbot_authenticated" not in st.session_state:
        st.session_state.is_chatbot_authenticated = False

    if not st.session_state.is_chatbot_authenticated:
        entered_password = st.text_input("Enter password for Chatbot:", type="password")
        if entered_password == password:
            st.session_state.is_chatbot_authenticated = True
        elif entered_password:
            st.error("Incorrect password.")

    return st.session_state.is_chatbot_authenticated


st.set_page_config(page_title="HealthWise - Chatbot", page_icon="💬")

if authenticate_chatbot():
    SESSION_STATE = {"role": "medical assistant", "content": "How can I help you?"}
    USER_INFO = {"latitude": "LAT", "longitude": "LON"}
    SHARE_LOCATION = False

    BACKEND_URL = "http://localhost:8000"

    with st.sidebar:
        with st.expander("Share location"):
            location = streamlit_geolocation()

            if location["latitude"] and location["longitude"]:
                cords = pd.DataFrame(
                    {"LAT": [location["latitude"]], "LON": [location["longitude"]]}
                )
                st.map(cords, zoom=10)
            else:
                location = {"latitude": None, "longitude": None}

    st.title("💬 HealthWise Chatbot")
    st.caption("Your medical assistant, ready to help!")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [SESSION_STATE]

    if "conversation_id" not in st.session_state:
        st.session_state["conversation_id"] = str(uuid.uuid4())

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        payload = {
            "user_request": prompt,
            "location": (
                f"{location['latitude']},{location['longitude']}"
                if location["latitude"]
                else ""
            ),
            "conversation_id": st.session_state["conversation_id"],
        }

        try:
            response = requests.post(f"{BACKEND_URL}/", json=payload, stream=True)
            response.raise_for_status()

            msg = ""
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    msg += chunk
            st.session_state.messages.append(
                {"role": "medical assistant", "content": msg}
            )
            st.chat_message("assistant").write(msg)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
else:
    st.warning("Please enter the password to access the chatbot.")
