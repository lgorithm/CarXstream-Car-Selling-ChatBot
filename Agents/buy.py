from langchain_openai import ChatOpenAI
from Prompts.buy import prompt
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from tools.sql_database import toolkit
from langchain import hub
from langchain_core.tools import tool
from typing_extensions import Literal, TypedDict, Annotated
from langgraph.prebuilt import InjectedState

load_dotenv()
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=5)
tools = toolkit.get_tools()
model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
system_prompt = SystemMessage(prompt + system_message)

# Supervisor agent (master agent) creation
buy = create_react_agent(model=model, tools=tools, state_modifier=system_prompt)

