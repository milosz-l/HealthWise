import requests
import pandas as pd
import streamlit as st

from streamlit_geolocation import streamlit_geolocation


def clear_chat_history():
    st.session_state.messages = [SESSION_STATE]


def reset_location():
    st.session_state["location"] = None
    

st.set_page_config(
    page_title="HealthWise - Chatbot",
    page_icon="💬"
)

SESSION_STATE = {"role": "medical assistant", "content": "How can I help you?"}
USER_INFO = {"latitude": "LAT", "longitude": "LON"}
SHARE_LOCATION = False

LLAMA = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
GPT2 = "https://api-inference.huggingface.co/models/openai-community/gpt2"
API_URL = ""

location = {}

if "location" not in st.session_state:
    st.session_state["location"] = None

with st.sidebar:
    selected_model = st.selectbox("Choose a model", ["Llama-3-8B", "GPT2"], key="selected_model")

    with st.expander("API Key Configuration"):
        api_key = st.text_input("Hugging Face API Key", key="huggingface_api_key", type="password")
        st.markdown("[Get your Hugging Face API key here](https://huggingface.co/settings/tokens)", unsafe_allow_html=True) 

    if selected_model == "Llama-3-8B":
        API_URL = LLAMA[:]
    elif selected_model == "GPT2":
        API_URL = GPT2[:]
    
    with st.expander("Share location"):
        if not st.session_state["location"]:
            location = streamlit_geolocation()

            if location["latitude"] and location["longitude"]:
                st.session_state["location"] = location
                st.write("Are you sure?")
            
        else:
            location = st.session_state["location"]
            st.button('Reset', on_click=reset_location)
            cords = pd.DataFrame({"LAT": [location["latitude"]], "LON": [location["longitude"]]})
            st.map(cords, zoom=10)
        
st.title("💬 HealthWise Chatbot")
st.caption("Your medical assistant, ready to help!")
st.button('Clear Chat History', on_click=clear_chat_history)

if "messages" not in st.session_state:
    st.session_state["messages"] = [SESSION_STATE]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not api_key:
        st.info("Please add your Hugging Face API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    if response.status_code == 200:
        msg = response.json()[0]["generated_text"]
        st.session_state.messages.append({"role": "medical assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    else:
        st.error("Something went wrong with the API request. Please check your API key and try again.")
    