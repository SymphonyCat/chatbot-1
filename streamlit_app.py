import streamlit as st
import requests

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses the LLaMA model to generate responses. "
    "To use this app, ensure you have a running LLaMA API server."
)

# Ask user for the LLaMA API endpoint.
llama_api_url = st.text_input("LLaMA API URL", placeholder="http://localhost:5000/chat")
if not llama_api_url:
    st.info("Please provide your LLaMA API URL to continue.", icon="🗝️")
else:
    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the LLaMA API.
        response = requests.post(llama_api_url, json={"messages": st.session_state.messages})

        if response.status_code == 200:
            assistant_message = response.json().get("response")
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})

            # Display the assistant's response.
            with st.chat_message("assistant"):
                st.markdown(assistant_message)
        else:
            st.error("Error while communicating with the LLaMA API.")
