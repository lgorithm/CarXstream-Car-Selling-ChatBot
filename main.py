from typing import Any
from dotenv import load_dotenv
from langchain import hub
from langchain_core.tools import Tool, StructuredTool
from langchain_openai import ChatOpenAI
from tools.comparison_tool import comparison
from tools.recommend_tool import recommend, Graph_BytesIO
import streamlit as st
from streamlit_chat import message
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from fuzzywuzzy import fuzz, process
from langgraph.checkpoint.postgres import PostgresSaver

from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)

load_dotenv()
history = StreamlitChatMessageHistory(key="chat_history")

if len(history.messages) == 0:
    history.add_ai_message("Hi, I'm Tina. How can I help you?")
st_callback = StreamlitCallbackHandler(st.container())
llm=ChatOpenAI(temperature=0, model="gpt-4-turbo")


def main():
    print("Start...")
    st.title("💬 Multi-Agent Chatbot")
    
    view_messages = st.expander("View the message contents in session state")
    for msg in history.messages:
        st.chat_message(msg.type).write(msg.content)

    prompt = "Your name is Tina and You are a helpful agent. You help user to sell their used cars. \
    Your task is to take this car information from the user: company, model, variant, year, odometer reading, \
    price, vehicle number, color. Once you completed taking those eight information then give company, model, \
    variant and price to your Tool called, 'Comparison Tool' as a parameter. User might give price input as a string \
    like this, Examples of input: 'Rs. 6.09 Lakh', '₹5.82L', '7L', '700000', etc. Please convert that price into int \
    like this: 700000, 1200000. Comparison Tool will check if the price of the car model is more than the actual car \
    price. If comparison tool return true that means user given price of the car model is more than the actual car. \
    In that case, inform the user regading that, and ask the user if they need price recommendation. If user say yes, then \
    send company name, model name odometer reading, price and vehicle number to Recommend tool. Recommend tool will return filepath string or boolean False. \
    If recommend tool return False, that means we don't have any previously sold information of that car model. If it return filepath string then \
    you should also return that same filepath string directly to user as content. Please Do Not Share Any Other Information To The User Except This Context"  
    # company: Maruti, model: baleno, variant: ZETA CVT PETROL 1.2, year: 2021, odometer reading: 1,12,062 km, price: 6 lakh, vehicle number: 7654982311, color: red
    # company: Hyundai , model: Xcent, variant: E Plus CRDi, year: 2021, odometer reading: 73,142 km, price: 34L, vehicle number: 9876123499, and color: red.

    @st.cache_resource
    def agent():  
        memory = MemorySaver()
        grand_agent_executor = create_react_agent(
            llm,
            tools=[comparison, recommend],
            state_modifier=prompt,
            checkpointer=memory
        )
        return grand_agent_executor
    config = {"configurable": {"thread_id": "test-thread"}}
    grand_agent_executor = agent()

    if prompt := st.chat_input():
        st.chat_message("user").write(prompt)
        st_callback = StreamlitCallbackHandler(st.container())
        response = grand_agent_executor.invoke(
            {
                "messages": [("human", prompt)]
            },
            config,
        )
        history.add_user_message(prompt)
        history.add_ai_message(response["messages"][-1].content)
        st.chat_message("ai").write(response["messages"][-1].content)
        print(response["messages"][-2].content)
        if 'graphs' in response["messages"][-2].content:
            with st.chat_message("ai"):
                st.image(response["messages"][-2].content, caption="Saved Graph", use_column_width=True)
        print(response)


if __name__ == "__main__":
    main()
