import pymysql

def connection():
    return pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        db='Agenda',
    )