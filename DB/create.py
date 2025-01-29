import sqlite3
from sqlalchemy import create_engine
import pandas as pd

df = pd.read_csv('car_data.csv')
engine = create_engine('sqlite:///car_data.db')
table_name = 'cars'
# Export the DataFrame to the SQLite database
df.to_sql(table_name, engine, if_exists='replace', index=False)

