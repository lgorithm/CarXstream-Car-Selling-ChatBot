import sqlite3
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
import requests
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def get_engine():

    connection = sqlite3.connect("DB/car_data.db", check_same_thread=False)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )


engine = get_engine()

db = SQLDatabase(engine)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

