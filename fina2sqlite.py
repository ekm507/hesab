import sqlite3
import json
import datetime

sql_filename = 'hesab.sql'
connection = sqlite3.connect(sql_filename)
sql_cursor = connection.cursor()
tablename = 'standard'
sql_cursor.execute(f'''CREATE TABLE IF NOT EXISTS {tablename} (
    date DATETIME,
    name TEXT,
    value REAL
    )''')
connection.commit()

json_filename = 'main.json'
json_data = json.load(open(json_filename))['standard']

for entryindex in json_data.keys():
    entry = json_data[entryindex]
    date = datetime.datetime.fromisoformat(entry['date']).toordinal()
    name = entry['name']
    value = entry['value']

    sql_cursor.execute(f'''INSERT INTO {tablename} VALUES(?,?,?)''', [date, name, value])

connection.commit()