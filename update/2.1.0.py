#!/usr/bin/env python

import sqlite3

con = sqlite3.connect("../data/hades.db")


update_query = "update user set GsheetAlias=? where UserId=? and Gsheetalias is Null"
cur = con.cursor()

cur.execute("SELECT * FROM user")
for row in cur.fetchall():
    result = cur.execute(update_query, [row[2], row[0]])
    print(f"updating {row[2]} {row[0]}")
    print(f"result {result}")
con.commit()
con.close()
