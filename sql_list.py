import sqlite3
import jdatetime
import click


sql_filename = 'hesab.sql'
connection = sqlite3.connect(sql_filename)
sql_cursor = connection.cursor()
tablename = 'standard'

def list_entries():
    entries = sql_cursor.execute(f'SELECT * FROM {tablename}')
    for entry in entries:
        name = entry[0]
        date = jdatetime.datetime.fromtimestamp(int(entry[1])).date()
        value = entry[2]
        print(name, date, value)
