import sqlite3

con = sqlite3.connect("car_data.db")
cursor = con.cursor()

res = cursor.execute("SELECT name FROM sqlite_master")
print(res.fetchone())