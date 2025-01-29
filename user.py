from typing import Any
from langchain import hub
from langchain_core.tools import Tool, StructuredTool
import streamlit as st
from streamlit_chat import message
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
import json
from langchain_core.messages.tool import ToolMessage
import os
from Agents.buy import buy

from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)

history = StreamlitChatMessageHistory(key="chat_history")

if len(history.messages) == 0:
    history.add_ai_message("Hi, I'm Tina. How can I help you?")
st_callback = StreamlitCallbackHandler(st.container())

print("Start...")
st.title("💬 Car selling Agent")
view_messages = st.expander("View the message contents in session state")
for msg in history.messages:
    st.chat_message(msg.type).write(msg.content)

config = {"configurable": {"thread_id": "test-thread"}}
if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st_callback = StreamlitCallbackHandler(st.container())
    response = buy.invoke(
        {
            "messages": [("human", prompt)]
        },
        config,
    )
    
    print(response)
    history.add_user_message(prompt)
    history.add_ai_message(response["messages"][-1].content)
    st.chat_message("ai").write(response["messages"][-1].content)