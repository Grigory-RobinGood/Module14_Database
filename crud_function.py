import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()


#cursor.execute("DROP TABLE IF EXISTS Users")


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY NOT NULL,
    title TEXT,
    description TEXT NOT NULL,
    price INT)
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL)
    ''')
    connection.commit()


def add_user(username, email, age):
    cursor.execute(f"INSERT INTO Users (username, email, age, balance) VALUES('{username}', '{email}', '{age}', 1000)")
    connection.commit()
    return


def is_included(username):
    check_user = cursor.execute(f"SELECT * FROM Users WHERE username=?", (username,))
    if check_user.fetchall() is None:
        return False
    else:
        return True


def get_all_products():
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.commit()
    connection.close()
    return products









