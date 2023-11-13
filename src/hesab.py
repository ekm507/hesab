#!/usr/bin/python3
# Released under GPLv3+ License
# Erfan Kheyrollahi Qaroğlu <ekm507@gmail.com>, 2023.

"""
Hesab - A CLI personal accounting app with Persian calendar
"""

import os
import sqlite3
import jdatetime
import click
from rich.table import Table, box
from rich import print as rprint


# defaults. should change later
SQL_FILENAME = "hesab.sql"
TABLE_NAME = "standard"


def create_database():
    connection = sqlite3.connect(SQL_FILENAME)
    sql_cursor = connection.cursor()
    sql_cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        date INT,
        name TEXT,
        value REAL
        )"""
    )
    connection.commit()


def fetch_entries_today():
    connection = sqlite3.connect(SQL_FILENAME)
    sql_cursor = connection.cursor()
    today_date = jdatetime.datetime.now().toordinal()
    entries = sql_cursor.execute(
        f"SELECT * FROM {TABLE_NAME} where date={today_date}"
    )
    return entries


def fetch_entries_all():
    connection = sqlite3.connect(SQL_FILENAME)
    sql_cursor = connection.cursor()
    entries = sql_cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    return entries


def get_entries_list():
    entries = fetch_entries_all()
    # entries = fetch_entries_today()
    entries_list = []
    for i, entry in enumerate(entries):
        # date = jdatetime.datetime.fromtimestamp(int(entry[0])).date()
        date = entry[0]
        name = entry[1]
        value = entry[2]
        entries_list.append((i + 1, date, name, value))
    return entries_list


# def flatten_entries_date(entries):
#    output = map(
#        lambda entry: (
#            entry[0],
#            jdatetime.datetime.fromtimestamp(int(entry[1])).date(),
#            entry[2],
#            entry[3],
#        ),
#        entries,
#    )
#    return list(output)


def filter_entries_today(entries):
    # entries = flatten_entries_date(entries)
    today_date = jdatetime.datetime.now().toordinal()
    # today_date = jdatetime.datetime.fromtimestamp(time.time()).date()
    output = filter(lambda entry: entry[1] == today_date, entries)
    return list(output)


def print_entries_list(entries):
    # entries = filter_entries_today(entries)
    # entries = flatten_entries_date(entries)

    egg_price = 5  # how much is an egg today?

    table_earn = Table(title="دخل", box=box.SIMPLE_HEAVY, expand=True)
    table_earn.add_column("اندیس", justify="right", style="cyan", no_wrap=True)
    table_earn.add_column("تاریخ", justify="right", style="cyan", no_wrap=True)
    table_earn.add_column("عنوان", style="magenta", justify="right")
    table_earn.add_column("مبلغ", justify="right", style="green")
    table_earn.add_column(f"🥚={egg_price}", justify="right", style="green")

    table_expense = Table(title="خرج", box=box.SIMPLE_HEAVY, expand=True)
    table_expense.add_column(
        "اندیس", justify="right", style="cyan", no_wrap=True
    )
    table_expense.add_column(
        "تاریخ", justify="right", style="cyan", no_wrap=True
    )
    table_expense.add_column("عنوان", style="magenta", justify="right")
    table_expense.add_column("مبلغ", justify="right", style="green")
    table_expense.add_column(f"🥚={egg_price}", justify="right", style="green")

    for entry in entries:
        index = str(entry[0])
        date = jdatetime.datetime.fromordinal(entry[1]).strftime("%y-%m-%d")
        name = entry[2]
        value = entry[3]
        value_str = str(value)
        value_egg = str((value / egg_price * 100) // 1 / 100)
        # table.add_row(index, date, name, value, value_egg)
        if value > 0:
            table_earn.add_row(value_egg, value_str, name, date, index)
        else:
            table_expense.add_row(value_egg, value_str, name, date, index)
        # table.border_style='red'

    grid = Table(expand=True, title="دخل‌وخرج‌ها", show_header=False)
    grid.add_column("دخل", ratio=1)
    grid.add_column("خرج", ratio=1)
    grid.add_row(table_earn, table_expense)
    rprint(grid)
    # print(f'{index}:   {date}    {name}   \t {value}')


def add_entry(date, name, value):
    connection = sqlite3.connect(SQL_FILENAME)
    sql_cursor = connection.cursor()
    sql_cursor.execute(
        f"""INSERT INTO {TABLE_NAME} VALUES(?,?,?)""", [date, name, value]
    )
    connection.commit()


def add_entry_with_date(name, value):
    date = jdatetime.datetime.now().toordinal()
    add_entry(date, name, value)


def remove_entry(entry_id):
    connection = sqlite3.connect(SQL_FILENAME)
    sql_cursor = connection.cursor()
    sql_cursor.execute(f"""DELETE FROM {TABLE_NAME} LIMIT {entry_id-1},{1};""")
    connection.commit()


def database_exists():
    if os.path.exists(SQL_FILENAME):
        return True
    else:
        return False


def check_database():
    if not database_exists():
        create_database()


@click.group()
def cli():
    pass


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("name", nargs=1)
@click.argument("value", nargs=1)
def add(name, value):
    add_entry_with_date(name, value)
    click.echo(f"added {name} with {value}")


@cli.command("list")
def list_entries():
    entries = get_entries_list()
    print_entries_list(entries)


@cli.command("remove")
@click.argument("number", nargs=1, type=int)
def list_entries(number):
    remove_entry(number)
    print(f"record {number} removed.")


def main():
    check_database()
    try:
        cli()
    except sqlite3.OperationalError:
        print("there is an Error in database file")


if __name__ == "__main__":
    main()
