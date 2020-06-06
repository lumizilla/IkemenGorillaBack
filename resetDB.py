# resetDB.py
import sqlite3
import sys

## YOU CAN USE THIS FILE TO RESET THE DB

DATABASE = 'ikemengori.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    return db


file = open("databaseCode.txt", "r")
dbCode = file.read()

print("Resetting database...")
cursor = get_db().executescript(dbCode)
get_db().commit()
cursor.close()
print("Done!")
