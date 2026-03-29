

#base de datos 

import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root1234',
            database='db_inventario'
        )
        return connection
    except Error as e:
        print(f"Error al conectar: {e}")
        return None