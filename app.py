# -*- coding: utf-8 -*-
"""

app.py

Simple blogging application

This file is part of showcase-python-flask,
an example flask application compiled based on the instructions from
<https://www.digitalocean.com/community/tutorials/
 how-to-make-a-web-application-using-flask-in-python-3-de>

"""

import datetime
import zoneinfo
import sqlite3

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


LOCAL_TIME_ZONE = zoneinfo.ZoneInfo("Europe/Berlin")


def get_db_connection():
    """Return the database connection"""
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_post_data(post_id):
    """Return data from the post specified by post_id"""
    conn = get_db_connection()
    post_data = conn.execute(
        "SELECT * FROM posts WHERE post_id = ?", (post_id,)
    ).fetchone()
    conn.close()
    if post_data is None:
        abort(404)
    #
    return post_data


app = Flask(__name__)
app.config["SECRET_KEY"] = "random secret key ideally generated at deploy time"


@app.template_filter("local_time_display")
def local_time_display(dt_string, local_time_zone=LOCAL_TIME_ZONE):
    """Return an UTC datetime converted to local time"""
    provided_dt = datetime.datetime.fromisoformat(dt_string)
    if not provided_dt.tzinfo:
        provided_dt = provided_dt.replace(tzinfo=datetime.timezone.utc)
    #
    localized_dt = provided_dt.astimezone(local_time_zone)
    return "{0} ({1})".format(localized_dt, localized_dt.tzname())


@app.route("/")
def index():
    """Application home page showing all post headlines"""
    conn = get_db_connection()
    all_posts_reversed = conn.execute(
        "SELECT * FROM posts ORDER BY created DESC"
    ).fetchall()
    conn.close()
    return render_template("index.html", posts=all_posts_reversed)


@app.route("/<int:post_id>")
def show_post(post_id):
    """Detail page showing the post headline and content"""
    post_data = get_post_data(post_id)
    return render_template("read.html", post_data=post_data)


@app.route("/create", methods=("GET", "POST"))
def create():
    """Page for creating new posts"""
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if title:
            conn = get_db_connection()
            post_id = conn.execute(
                "INSERT INTO posts (title, content) VALUES (?, ?)"
                "RETURNING post_id",
                (title, content),
            ).fetchone()["post_id"]
            conn.commit()
            conn.close()
            return redirect(url_for("show_post", post_id=post_id))
        #
        flash("Title is required!")
    #
    return render_template("create.html")


@app.route("/<int:post_id>/edit", methods=("GET", "POST"))
def edit(post_id):
    """Page for editing existing posts"""
    post_data = get_post_data(post_id)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if title:
            conn = get_db_connection()
            conn.execute(
                "UPDATE posts SET title = ?, content = ? WHERE post_id = ?",
                (title, content, post_id),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("show_post", post_id=post_id))
        #
        flash("Title is required!")
    #
    return render_template("update.html", post_data=post_data)


@app.route("/<int:post_id>/delete", methods=("POST",))
def delete(post_id):
    """URL for deleting existing posts"""
    post_data = get_post_data(post_id)
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE post_id = ?", (post_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post_data["title"]))
    return redirect(url_for("index"))


#
