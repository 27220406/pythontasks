import sqlite3
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT UNIQUE
)
''')


cursor.execute('''
INSERT INTO student (name, age, email)
VALUES (?, ?, ?)
''', ("Simmi", 19, "987@example.com"))


connection.commit()


cursor.execute('SELECT * FROM student')
rows = cursor.fetchall()

for row in rows:
    print(row)


connection.close()