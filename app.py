from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import mysql.connector
from mysql.connector import errorcode

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')

app = Flask(__name__, template_folder=template_path)


def insert_user_data(name, pdf):
    try:
        cnx = mysql.connector.connect(user='scott',
                                      database='employ')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()
    cnx = mysql.connector.connect.MySQLConnection(user='root', password='root',
                                                  host='127.0.0.1',
                                                  database='pdf upload')
    # con = sqlite3.connect("pdf upload.sqlite")
    cur = cnx.cursor()
    query = """
        INSERT INTO resume_table (user_name, pdf) VALUES (?, ?);
    """
    cur.execute(query, [name, pdf])
    cnx.commit()


@app.route("/")
def home():
    if request.method == "POST":
        pdf = request.files["pdf"].read()
        name = request.form["name"]
        insert_user_data(name, pdf)
        return redirect(url_for("home"))

    return render_template("index.html")
