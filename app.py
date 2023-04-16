from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import mysql.connector
from mysql.connector import errorcode

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')

app = Flask(__name__, template_folder=template_path)


def insert_user_data(name, pdf):

    cnx = mysql.connector.connect(user='root', password='dontforgetmysql14@#',
                                  host='127.0.0.1',
                                  database='resumes')
    cur = cnx.cursor()
    query = """
        INSERT INTO resume_table (user_name, pdf) VALUES (&s, &S);
    """
    cur.execute(query, [name, pdf])
    print(cur.column_names)
    cnx.commit()


@app.route("/")
def home():
    if request.method == "POST":
        pdf = request.files["pdf"].read()
        name = request.form["name"]
        insert_user_data(name, pdf)
        return redirect(url_for("home"))

    return render_template("index.html")
