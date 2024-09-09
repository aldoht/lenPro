from flask import Flask, render_template, request, redirect
from pymysql import MySQLError

from mysql import connection

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/update")
def update():
    return render_template("update.html")

@app.route("/remove")
def remove():
    return render_template("remove.html")

@app.route("/out")
def show():
    conn = connection()
    cur = conn.cursor()
    contacts = []

    try:
        cur.execute("SELECT * FROM People;")
        contacts = cur.fetchall()
    except MySQLError as e:
        print(e)
    finally:
        cur.close()
        conn.close()

    return render_template("out.html", contacts=contacts)

@app.route("/add", methods=["POST"])
def form():
    name = request.form["firstname"]
    lastName = request.form["lastname"]

    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO People (Name, Surname) VALUES (%s, %s)", (name, lastName))
        conn.commit()
    except MySQLError as e:
        print(e)
        return "Error", 400
    finally:
        cursor.close()
        conn.close()

    return redirect("out")

@app.route("/removepost", methods=["POST"])
def removepost():
    id = request.form["id"]

    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM People where ID = %s;", id)
        conn.commit()
    except MySQLError as e:
        print(e)
        return "Error", 400
    finally:
        cursor.close()
        conn.close()

    return redirect("out")
@app.route("/updatepost", methods=["POST"])
def updatepost():
    id = request.form["id"]
    name = request.form["firstname"]
    lastName = request.form["lastname"]

    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE People SET Name = %s, Surname = %s where ID = %s;", (name, lastName, id))
        conn.commit()
    except MySQLError as e:
        print(e)
        return "Error", 400
    finally:
        cursor.close()
        conn.close()

    return redirect("out")

if __name__ == "__main__":
    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS People(ID INT AUTO_INCREMENT PRIMARY KEY, Name TEXT, Surname TEXT);")
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

    app.run()
