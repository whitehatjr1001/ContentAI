import streamlit as st
import requests

# Title for the conversational bot
st.title("  ----Content AI----")

# Initialize the session state to maintain message history
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "state" not in st.session_state:
        st.session_state.state = "awaiting_message_type"
    if "eta" not in st.session_state:
        st.session_state.eta = None

# Initialize session state if not already initialized
initialize_session_state()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field to accept user input
if user_input := st.chat_input("Ask anything..."):
    # Add the user's message to the session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display the user's message in the chat interface
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call Flask API to get the response from the backend LLM
    flask_url = "http://localhost:5001/query"  
    response = requests.post(flask_url, json={"query": user_input})

    if response.status_code == 200:
        # Extract the LLM response from the Flask API
        llm_response = response.json().get('answer', "No response generated.")
    else:
        llm_response = f"Error: {response.status_code}"

    # Add the assistant's message to the session state
    st.session_state.messages.append({"role": "assistant", "content": llm_response})

    # Display the assistant's message in the chat interface
    with st.chat_message("assistant"):
        st.markdown(llm_response)

# Reset the ETA in session state after response
st.session_state.eta = None

