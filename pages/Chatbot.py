import requests
import pandas as pd
import streamlit as st

from streamlit_geolocation import streamlit_geolocation
import uuid  # Import uuid to generate conversation_id


def clear_chat_history():
    st.session_state.messages = [SESSION_STATE]
    # Generate a new conversation_id when chat history is cleared
    st.session_state.conversation_id = str(uuid.uuid4())


st.set_page_config(page_title="HealthWise - Chatbot", page_icon="💬")

SESSION_STATE = {"role": "medical assistant", "content": "How can I help you?"}
USER_INFO = {"latitude": "LAT", "longitude": "LON"}
SHARE_LOCATION = False

BACKEND_URL = "http://localhost:8000"  # Update with your backend URL

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
# st.button("Clear Chat History", on_click=clear_chat_history)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state["messages"] = [SESSION_STATE]

if "conversation_id" not in st.session_state:
    st.session_state["conversation_id"] = str(uuid.uuid4())

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Send the user prompt to the backend
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

        # Read the streaming response from the backend
        msg = ""
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                msg += chunk
                # Optionally, you can update the message in real-time
                # st.session_state.messages.append({"role": "medical assistant", "content": msg})
                # st.chat_message("assistant").write(msg)
        # Once the full message is received, append it to the chat
        st.session_state.messages.append({"role": "medical assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
