# -*- coding: utf-8 -*-
"""

init_db.py

Initialize the database from schema.sql
and add a "Welcome" blog post

This file is part of showcase-python-flask,
an example flask application compiled based on the instructions from
<https://www.digitalocean.com/community/tutorials/
 how-to-make-a-web-application-using-flask-in-python-3-de>

"""

import sqlite3


connection = sqlite3.connect("database.db")


with open("schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO posts (title, content) VALUES (?, ?)",
    (
        "Welcome to your new example blog application!",
        "You can create, read, update (“edit”) or delete blog posts.",
    ),
)

connection.commit()
connection.close()

print("Initialized database schema.")
