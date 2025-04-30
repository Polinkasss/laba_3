import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    note TEXT, 
                    priority INTEGER)''')

# Словарь для отображения приоритетов
PRIORITY_NAMES = {
    0: "отсутствует",
    1: "низкий",
    2: "средний",
    3: "высокий"
}

def show_notes():
    """Показывает заметки, отсортированные по приоритету"""
    for row in tree.get_children():
        tree.delete(row)

    # Сортируем по приоритету (от высокого к низкому), затем по ID
    cursor.execute("SELECT * FROM notes ORDER BY priority DESC, id ASC")
    rows = cursor.fetchall()

    for row in rows:
        # Заменяем числовой приоритет на текстовое представление
        modified_row = (row[0], row[1], PRIORITY_NAMES.get(row[2], "неизвестно"))
        tree.insert("", "end", values=modified_row)

def add_note():
    """Добавляет новую заметку"""
    note_text = note_entry.get()
    priority_value = priority_var.get()

    if note_text:
        try:
            cursor.execute("INSERT INTO notes (note, priority) VALUES (?, ?)",
                          (note_text, priority_value))
            conn.commit()
            show_notes()
            note_entry.delete(0, END)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"SQL Error: {e}")

def update_note():
    """Обновляет выбранную заметку"""
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        note_id = item['values'][0]

        note_text = note_entry.get()
        priority_value = priority_var.get()

        if note_text:
            cursor.execute("UPDATE notes SET note=?, priority=? WHERE id=?",
                          (note_text, priority_value, note_id))
            conn.commit()
            show_notes()
            note_entry.delete(0, END)

def delete_note():
    """Удаляет выбранную заметку"""
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        note_id = item['values'][0]

        cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
        conn.commit()
        show_notes()
        note_entry.delete(0, END)

# Создаем главное окно
window = Tk()
window.title("Заметки с приоритетами")
window.geometry('600x400')

# Фрейм для ввода данных
input_frame = Frame(window)
input_frame.pack(pady=10)

Label(input_frame, text="Текст заметки:").grid(row=0, column=0, padx=5)
note_entry = Entry(input_frame, width=30)
note_entry.grid(row=0, column=1, padx=5)

priority_var = IntVar(value=1)

Label(input_frame, text="Приоритет:").grid(row=1, column=0, padx=5)
priority_frame = Frame(input_frame)
priority_frame.grid(row=1, column=1, padx=5, sticky=W)

# Радиокнопки для выбора приоритета
Radiobutton(priority_frame, text="Отсутствует", variable=priority_var, value=0).pack(side=LEFT)
Radiobutton(priority_frame, text="Низкий", variable=priority_var, value=1).pack(side=LEFT)
Radiobutton(priority_frame, text="Средний", variable=priority_var, value=2).pack(side=LEFT)
Radiobutton(priority_frame, text="Высокий", variable=priority_var, value=3).pack(side=LEFT)

# Фрейм для кнопок
button_frame = Frame(window)
button_frame.pack(pady=5)

Button(button_frame, text="Добавить", command=add_note).pack(side=LEFT, padx=5)
Button(button_frame, text="Обновить", command=update_note).pack(side=LEFT, padx=5)
Button(button_frame, text="Удалить", command=delete_note).pack(side=LEFT, padx=5)
Button(button_frame, text="Обновить список", command=show_notes).pack(side=LEFT, padx=5)

# Фрейм для таблицы с заметками
tree_frame = Frame(window)
tree_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

scrollbar = Scrollbar(tree_frame)
scrollbar.pack(side=RIGHT, fill=Y)

# Создаем таблицу
tree = ttk.Treeview(tree_frame,
                   columns=("ID", "Note", "Priority"),
                   show="headings",
                   yscrollcommand=scrollbar.set)
tree.pack(fill=BOTH, expand=True)

scrollbar.config(command=tree.yview)

# Настраиваем колонки
tree.heading("ID", text="ID")
tree.heading("Note", text="Заметка")
tree.heading("Priority", text="Приоритет")

tree.column("ID", width=50, anchor=CENTER)
tree.column("Note", width=300)
tree.column("Priority", width=100, anchor=CENTER)

def on_tree_select(event):

    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        note_entry.delete(0, END)
        note_entry.insert(0, item['values'][1])

        for priority, name in PRIORITY_NAMES.items():
            if name == item['values'][2]:
                priority_var.set(priority)
                break

tree.bind('<<TreeviewSelect>>', on_tree_select)

show_notes()

window.mainloop()
conn.close()