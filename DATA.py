import sqlite3

def create_table():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                email TEXT UNIQUE
            )
        ''')

def insert_student():
    name = input("Enter name: ")
    age = input("Enter age: ")
    email = input("Enter email: ")
    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO student (name, age, email) VALUES (?, ?, ?)",
                           (name, age, email))
            conn.commit()
            print("✅ Student inserted successfully.\n")
    except sqlite3.IntegrityError:
        print("⚠️ Email already exists! Try a different one.\n")

def remove_student():
    student_id = input("Enter student ID to remove: ")
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE id = ?", (student_id,))
        if cursor.rowcount > 0:
            print("🗑️ Student removed successfully.\n")
        else:
            print("❌ No student found with that ID.\n")

def display_students():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student")
        rows = cursor.fetchall()
        if rows:
            print("\n📋 Student Records:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Email: {row[3]}")
            print()
        else:
            print("📭 No student records found.\n")

def menu():
    create_table()
    while True:
        print("====== Student Database Menu ======")
        print("1. Insert Student")
        print("2. Remove Student")
        print("3. Display Students")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            insert_student()
        elif choice == '2':
            remove_student()
        elif choice == '3':
            display_students()
        elif choice == '4':
            print("👋 Exiting program. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Try again!\n")

menu()
