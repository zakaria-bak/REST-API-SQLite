import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query = "CREATE TABLE if not exists users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(query)

query = "CREATE TABLE if not exists items(name text, price real)"
cursor.execute(query)

#cursor.execute("INSERT INTO items VALUES ('test', 10.18)")


connection.commit()
connection.close()

