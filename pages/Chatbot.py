import requests
import pandas as pd
import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import uuid
import os
import json

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
    SESSION_STATE = {"bot": "How can I help you?"}
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
        for role, content in msg.items():
            if role == "bot":
                role = "assistant"
            st.chat_message(role).write(content)

    if prompt := st.chat_input():
        st.session_state.messages.append({"user": prompt})
        st.chat_message("user").write(prompt)
        payload = {
            "conversation_history": st.session_state.messages,
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

            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                response_text = ""
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        chunk_key, chunk_content = list(json.loads(chunk).items())[0]
                        if chunk_key == "processing_state" and chunk_content:
                            response_placeholder.write(chunk_content)
                        elif chunk_content == "":
                            pass
                        elif chunk_key == "answer":
                            response_text += chunk_content
                            response_placeholder.write(response_text)
                        elif chunk_key == "final_answer":
                            response_text += chunk_content
                            response_placeholder.write(response_text)

            st.session_state.messages.append(
                {"bot": response_text}
            )
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
else:
    st.warning("Please enter the password to access the chatbot.")
