import sqlite3
from tkinter import *
import tkinter.ttk as ttk

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   note TEXT, priority INTEGER)''')

def show_notes():
    cursor.execute("SELECT * FROM notes")
    rows = cursor.fetchall()

    # Очищаем таблицу перед обновлением
    for i in tree.get_children():
        tree.delete(i)

    # Заполняем таблицу данными из базы
    for row in rows:
        tree.insert("", "end", values=row)


def add_note():
    def add():
        cursor.execute("INSERT INTO notes (note, priority) VALUES (?, ?)", (note.get(), priority.get()))
        conn.commit()
        show_notes() # Обновляем таблицу после добавления
        add_window.destroy()
    add_window = Toplevel(window)
    note = Entry(add_window)
    note.grid()
    priority = Entry(add_window)
    priority.grid()
    Button(add_window, text="Добавить", command=add).grid()

def update_note():
    def update():
        cursor.execute("UPDATE notes SET note=?, priority=? WHERE id=?", (note.get(), priority.get(), id_.get()))
        conn.commit()
        show_notes() # Обновляем таблицу после обновления
        update_window.destroy()
    update_window = Toplevel(window)
    id_ = Entry(update_window)
    id_.grid()
    note = Entry(update_window)
    note.grid()
    priority = Entry(update_window)
    priority.grid()
    Button(update_window, text="Обновить", command=update).grid()

def delete_note():
    def delete():
        cursor.execute("DELETE FROM notes WHERE id=?", (id_.get(),))
        conn.commit()
        show_notes()
        delete_window.destroy()
    delete_window = Toplevel(window)
    id_ = Entry(delete_window)
    id_.grid()
    Button(delete_window, text="Удалить", command=delete).grid()


window = Tk()
window.title("Заметки")
window.geometry('600x400')



tree = ttk.Treeview(window, columns=("ID", "Заметка", "Приоритет"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Заметка", text="Заметка")
tree.heading("Приоритет", text="Приоритет")
tree.grid(row=5, column=0, columnspan=4, pady=(10, 0))


Button(window, text="Добавить", command=add_note).grid(row=0, column=0, pady=5)
Button(window, text="Обновить", command=update_note).grid(row=1, column=0, pady=5)
Button(window, text="Удалить", command=delete_note).grid(row=2, column=0, pady=5)
Button(window, text="Показать", command=show_notes).grid(row=3, column=0, pady=5)




window.mainloop()
conn.close()
