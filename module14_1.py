import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

#cursor.execute("DROP TABLE IF EXISTS Users")
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

for i in range(10):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)",
                   (f"User{i+1}", f"example{i+1}@gmail.com", (i+1)*10, 1000))

cursor.execute("UPDATE Users SET balance = ? WHERE id % 2 != 0", (500,))

for a in range(1, 11, 3):
    cursor.execute("DELETE FROM Users WHERE id = ?", (f"{a}", ))


cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60")
users = cursor.fetchall()
for username, email, age, balance in users:
    print(f"Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}")

connection.commit()
connection.close()
