#!/usr/bin/env python

import sqlite3
from datetime import datetime

old_conn = sqlite3.connect("hades_old.db")
new_conn = sqlite3.connect("data/hades.db")

old_cur = old_conn.cursor()
new_cur = new_conn.cursor()


def migrate_users():
    query = "select Id, DiscordAlias, last_active, last_channel from UserMap"
    old_cur.execute(query)
    old_users = old_cur.fetchall()

    ins_query = "insert into user (UserId, DiscordAlias, LastActive, LastChannel) values (?, ?, ?, ?)"
    for row in old_users:
        print(f"row: {row}")
        if row[2] is None:
            new_cur.execute(ins_query, [row[0], row[1], None, row[3]])
        else:
            new_cur.execute(
                ins_query,
                [
                    row[0],
                    row[1],
                    datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f"),
                    row[3],
                ],
            )

        new_conn.commit()


def migrate_status():
    query = "select Id, LastUpdate, StatusText from Status"
    old_cur.execute(query)
    old_status = old_cur.fetchall()

    ins_query = "insert into Status (UserId, LastUpdate, StatusText) values (?, ?, ?)"
    for row in old_status:
        print(f"row: {row}")
        if row[1] is None:
            new_cur.execute(ins_query, [row[0], None, row[2]])
        else:
            new_cur.execute(
                ins_query,
                [row[0], datetime.strptime(row[1], "%d-%m-%Y %H:%M:%S"), row[2]],
            )

    new_conn.commit()


def migrate_wsentry():
    query = "select Id, Inschrijving, Opmerkingen, Inschrijftijd, actueel from WSinschrijvingen"
    old_cur.execute(query)
    old_status = old_cur.fetchall()

    ins_query = "insert into wsentry (UserId, EntryType, Remark, EntryTime, Active) values (?, ?, ?, ?, ?)"
    for row in old_status:
        print(f"row: {row}")
        if row[4] == "ja":
            active = True
        else:
            active = False
        if row[1] is None:
            new_cur.execute(ins_query, [row[0], row[1], row[2], row[3], active])
        else:
            new_cur.execute(
                ins_query,
                [
                    row[0],
                    row[1],
                    row[2],
                    datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
                    active,
                ],
            )

    new_conn.commit()


migrate_users()
migrate_status()
migrate_wsentry()
