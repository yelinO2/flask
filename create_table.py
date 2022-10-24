import sqlite3

connection = sqlite3.connect("mydatabase.db")

cursor = connection.cursor()

# SQL Query or SQL Command
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"

cursor.execute(create_table)

create_item_table = "CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, name text, price text)"
cursor.execute(create_item_table)

create_store_table = "CREATE TABLE IF NOT EXISTS stores(id INTEGER PRIMARY KEY, name text)"
cursor.execute(create_store_table)



connection.commit()

connection.close()

