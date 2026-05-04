import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
from datetime import datetime

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.data = []
        self.load_data()

        # --- Поля ввода ---
        ttk.Label(root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(root)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Дата:").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # --- Кнопка добавления ---
        ttk.Button(root, text="Добавить расход", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

        # --- Таблица расходов ---
        self.tree = ttk.Treeview(root, columns=("Сумма", "Категория", "Дата"), show="headings")
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        self.tree.grid(row=4, column=0, columnspan=2, sticky="nsew")

        # --- Фильтры ---
        ttk.Label(root, text="Фильтр по категории:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_category = ttk.Combobox(root, values=self.get_categories())
        self.filter_category.grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(root, text="Фильтровать", command=self.filter_by_category).grid(row=6, column=0, columnspan=2, pady=5)

        ttk.Label(root, text="Период (с):").grid(row=7, column=0, padx=5, pady=5)
        self.start_date = DateEntry(root, date_pattern='yyyy-mm-dd')
        self.start_date.grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(root, text="Период (по):").grid(row=8, column=0, padx=5, pady=5)
        self.end_date = DateEntry(root, date_pattern='yyyy-mm-dd')
        self.end_date.grid(row=8, column=1, padx=5, pady=5)

        ttk.Button(root, text="Сумма за период", command=self.sum_for_period).grid(row=9, column=0, columnspan=2, pady=5)

        # Заполнение таблицы при запуске
        self.update_table()

    def load_data(self):
        try:
            with open("data.json", "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def save_data(self):
        with open("data.json", "w") as f:
            json.dump(self.data, f)

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get_date().strftime('%Y-%m-%d')

        if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
            return

        if not category:
            messagebox.showerror("Ошибка", "Введите категорию!")
            return

        self.data.append({"amount": float(amount), "category": category, "date": date})
        self.save_data()
        self.update_table()

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.data:
            self.tree.insert("", "end", values=(item["amount"], item["category"], item["date"]))

    def get_categories(self):
        return list(set([x["category"] for x in self.data]))

    def filter_by_category(self):
        category = self.filter_category.get()
        filtered = [x for x in self.data if x["category"] == category]
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in filtered:
            self.tree.insert("", "end", values=(item["amount"], item["category"], item["date"]))

    def sum_for_period(self):
        start = self.start_date.get_date().strftime('%Y-%m-%d')
        end = self.end_date.get_date().strftime('%Y-%m-%d')

        total = sum(
            x["amount"] for x in self.data
            if start <= x["date"] <= end
        )

        messagebox.showinfo("Сумма за период", f"Сумма расходов с {start} по {end}: {total:.2f} руб.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()