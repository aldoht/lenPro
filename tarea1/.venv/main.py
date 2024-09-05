from flask import Flask, render_template, request, redirect, url_for
import pymysql
from db import getDBConnection

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    connection = getDBConnection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT ID, Name, Surname FROM People")
        contacts = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        contacts = []
    finally:
        cursor.close()
        connection.close()

    return render_template('form.html', contacts=contacts)

@app.route('/', methods=['POST'])
def submit():
    name = request.form['name']
    surname = request.form['surname']
    
    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO People (Name, Surname) VALUES (%s,%s)", (name, surname))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
