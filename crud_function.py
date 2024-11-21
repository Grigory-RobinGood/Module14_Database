import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()
#cursor.execute("DROP TABLE IF EXISTS Products")


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY NOT NULL,
    title TEXT,
    description TEXT NOT NULL,
    price INT
    )
    ''')
    connection.commit()
    connection.close()


def get_all_products():
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.commit()
    connection.close()
    return products









