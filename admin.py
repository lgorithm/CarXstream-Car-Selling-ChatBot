import streamlit as st
import pandas as pd
import sqlite3
from sqlalchemy import create_engine

query = "SELECT * FROM cars"
engine = create_engine('sqlite:///DB/car_data.db')
df = pd.read_sql(query, engine)

st.dataframe(df, use_container_width=True)