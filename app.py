import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import streamlit as st
from agent.recat_agent import ReactAgent

import time

st.title("智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

user_input = st.chat_input()

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state["messages"].append({"role":"user","content":user_input})

    res_messages = []
    with st.spinner('思考中'):
        res_stream = st.session_state["agent"].execute_stream(user_input)

        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)

                for char in chunk:
                    time.sleep(0.01)
                    yield char


        st.chat_message("assistant").write_stream(capture(res_stream, res_messages))
        st.session_state["messages"].append({"role": "assistant", "content": res_messages[-1]})
        st.rerun()