import pymysql

def getDBConnection():
    connection = pymysql.connect(
        host='127.0.0.1',         
        user='root',    
        password='root', 
        database='Agenda'  
    )
    return connection