import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT UNIQUE
    )
''')
conn.commit()

def insert_student():
    name = name_var.get()
    age = age_var.get()
    email = email_var.get()

    if name == "" or age == "" or email == "":
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        cursor.execute("INSERT INTO student (name, age, email) VALUES (?, ?, ?)", (name, age, email))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_inputs()
        display_students()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email already exists!")

def delete_student():
    try:
        selected = tree.selection()[0]
        student_id = tree.item(selected)["values"][0]
        cursor.execute("DELETE FROM student WHERE id = ?", (student_id,))
        conn.commit()
        tree.delete(selected)
        messagebox.showinfo("Deleted", "Student deleted successfully.")
    except IndexError:
        messagebox.showerror("Error", "Please select a student to delete.")

def display_students():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM student")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def clear_inputs():
    name_var.set("")
    age_var.set("")
    email_var.set("")

def exit_app():
    root.destroy()


root = tk.Tk()
root.title("🎓 Student Database Manager")
root.geometry("700x500")
root.configure(bg="#f0f4f7")


name_var = tk.StringVar()
age_var = tk.StringVar()
email_var = tk.StringVar()


tk.Label(root, text="Student Name:", bg="#f0f4f7", font=("Arial", 12)).place(x=50, y=30)
tk.Entry(root, textvariable=name_var, width=30).place(x=180, y=32)

tk.Label(root, text="Age:", bg="#f0f4f7", font=("Arial", 12)).place(x=50, y=70)
tk.Entry(root, textvariable=age_var, width=30).place(x=180, y=72)

tk.Label(root, text="Email:", bg="#f0f4f7", font=("Arial", 12)).place(x=50, y=110)
tk.Entry(root, textvariable=email_var, width=30).place(x=180, y=112)


tk.Button(root, text="Insert", width=12, bg="#4CAF50", fg="white", command=insert_student).place(x=500, y=30)
tk.Button(root, text="Delete", width=12, bg="#f44336", fg="white", command=delete_student).place(x=500, y=70)
tk.Button(root, text="Display", width=12, bg="#2196F3", fg="white", command=display_students).place(x=500, y=110)
tk.Button(root, text="Exit", width=12, bg="#9E9E9E", fg="white", command=exit_app).place(x=500, y=150)

tree = ttk.Treeview(root, columns=("ID", "Name", "Age", "Email"), show="headings")
tree.heading("ID", text="ID")
tree.column("ID", width=50)
tree.heading("Name", text="Name")
tree.column("Name", width=150)
tree.heading("Age", text="Age")
tree.column("Age", width=50)
tree.heading("Email", text="Email")
tree.column("Email", width=200)

tree.place(x=50, y=200, width=600, height=250)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
style.configure("Treeview", font=('Arial', 10), rowheight=25)

display_students()
root.mainloop()
