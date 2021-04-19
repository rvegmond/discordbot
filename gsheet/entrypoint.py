#!/usr/bin/env python

import gspread
import sqlite3
from datetime import datetime


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return conn


def create_gsheet_table(conn, worksheet):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    cur = conn.cursor()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        query = f"alter table gsheet rename to gsheet{timestamp};"
        print("{}".format(query))
        cur.execute(query)
    except Exception as e:
        print("table doesn't exist.")
    header_list = worksheet.row_values(1)
    query = "create table gsheet ('" + "','".join(header_list) + "');"
    print("{}".format(query))
    cur.execute(query)
    conn.commit()


def insert_gsheet_into_table(conn, worksheet):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    # list_of_lists = worksheet.get_all_values()

    header_list = worksheet.row_values(1)

    # print("{}".format(type(list_of_lists)))
    list_of_lists = worksheet.get_all_values()
    list_of_lists.pop(0)
    cur = conn.cursor()
    query = "delete from gsheet"
    result = cur.execute(query)

    query = "insert into gsheet values (?"
    for i in range(len(header_list) - 1):
        query += ", ?"
    query += ")"
    print("query: {}".format(query))

    result = cur.executemany(query, list_of_lists)
    print("{}".format(result))
    conn.commit()


def main():
    conn = create_connection('/data/hades.db')

    gc = gspread.service_account()

    # Open a sheet from a spreadsheet in one go
    wks = gc.open("Hades Star Spreadsheet")
    # Update a range of cells using the top left corner address
    worksheet = wks.worksheet("Modules")

    insert_gsheet_into_table(conn, worksheet)
    conn.close()


if __name__ == '__main__':
    main()
