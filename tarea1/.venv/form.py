from flask import Flask, render_template, request, redirect, url_for
from main import app
from dbconfig import getDBConnection
import pymysql


@app.route('/', methods=["GET"])
def index():
    connection = getDBConnection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT * FROM People")
        contactos = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        contactos = []
    finally:
        cursor.close()
        connection.close()

    return render_template('form.html', contactos=contactos)

@app.route('/', methods=['POST'])
def submit():
    name = request.form['name']
    surname = request.form['surname']
    
    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO People (nombre, apellido) VALUES (%s,%s)", (name, surname))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_contact(id):
    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM People WHERE ID = %s", (id,))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    connection = getDBConnection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']

        try:
            cursor.execute("UPDATE People SET Name = %s, Surname = %s WHERE ID = %s", (name, surname, id,))
            connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('index'))
    
    else:
        try:
            cursor.execute("SELECT * FROM People WHERE ID = %s", (id,))
            contacto = cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            contacto = None
        finally:
            cursor.close()
            connection.close()

        return render_template('edit.html', contacts=contacto)


if __name__ == "__main__":
    app.run()