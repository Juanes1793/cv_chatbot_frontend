import streamlit as st
import random
import time
import httpx
import json


# Streamed response emulator
def response_generator(url:str, input_data:dict):
    with httpx.Client(timeout=None) as client:
        try:
            # Envío de la solicitud POST
            with client.stream("POST", url, json=input_data) as response:
                if response.status_code == 200:
                    print("Recibiendo datos de streaming...")
                    # Itera sobre las partes de la respuesta conforme llegan
                    for line in response.iter_text():
                        if line:
                            yield line
                            
                else:
                    print(f"Error en la solicitud: {response.status_code}")
        except Exception as e:
            print(f"Se produjo un error: {str(e)}")
            # send request


st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(url="http://localhost:8000/chat_stream", input_data={"history": st.session_state.messages}))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})