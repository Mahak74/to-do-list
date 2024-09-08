import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("400x600")

        self.tasks = []

        self.load_tasks()

        self.title_label = tk.Label(root, text="To-Do List", font=("Helvetica", 18))
        self.title_label.pack(pady=10)

        self.tasks_frame = tk.Frame(root)
        self.tasks_frame.pack(pady=10)

        self.new_task_button = tk.Button(root, text="Add New Task", command=self.open_add_task_window)
        self.new_task_button.pack(pady=10)

        self.update_tasks_list()

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
        else:
            self.tasks = []

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

    def open_add_task_window(self):
        self.task_window = tk.Toplevel(self.root)
        self.task_window.title("Add New Task")

        title_label = tk.Label(self.task_window, text="Task Title", font=("Helvetica", 14))
        title_label.pack(pady=10)

        self.title_entry = tk.Entry(self.task_window, font=("Helvetica", 14))
        self.title_entry.pack(pady=10)

        desc_label = tk.Label(self.task_window, text="Description", font=("Helvetica", 14))
        desc_label.pack(pady=10)

        self.desc_entry = tk.Text(self.task_window, font=("Helvetica", 14), height=4)
        self.desc_entry.pack(pady=10)

        priority_label = tk.Label(self.task_window, text="Priority (Low, Medium, High)", font=("Helvetica", 14))
        priority_label.pack(pady=10)

        self.priority_entry = tk.Entry(self.task_window, font=("Helvetica", 14))
        self.priority_entry.pack(pady=10)

        due_date_label = tk.Label(self.task_window, text="Due Date (YYYY-MM-DD)", font=("Helvetica", 14))
        due_date_label.pack(pady=10)

        self.due_date_entry = tk.Entry(self.task_window, font=("Helvetica", 14))
        self.due_date_entry.pack(pady=10)

        save_button = tk.Button(self.task_window, text="Save Task", command=self.save_task)
        save_button.pack(pady=10)

    def save_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get("1.0", "end-1c")
        priority = self.priority_entry.get()
        due_date = self.due_date_entry.get()

        if not title:
            messagebox.showwarning("Input Error", "Task title is required.")
            return

        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid date in YYYY-MM-DD format.")
                return

        task = {
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "completed": False
        }

        self.tasks.append(task)
        self.save_tasks()
        self.update_tasks_list()
        self.task_window.destroy()

    def update_tasks_list(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        for i, task in enumerate(self.tasks):
            task_text = f"{task['title']} - {'Completed' if task['completed'] else 'Pending'}"
            task_label = tk.Label(self.tasks_frame, text=task_text, font=("Helvetica", 12))
            task_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            edit_button = tk.Button(self.tasks_frame, text="Edit", command=lambda i=i: self.open_edit_task_window(i))
            edit_button.grid(row=i, column=1, padx=10)

            complete_button = tk.Button(self.tasks_frame, text="Complete", command=lambda i=i: self.complete_task(i))
            complete_button.grid(row=i, column=2, padx=10)

            delete_button = tk.Button(self.tasks_frame, text="Delete", command=lambda i=i: self.delete_task(i))
            delete_button.grid(row=i, column=3, padx=10)

    def open_edit_task_window(self, index):
        self.task_window = tk.Toplevel(self.root)
        self.task_window.title("Edit Task")

        task = self.tasks[index]

        title_label = tk.Label(self.task_window, text="Task Title", font=("Helvetica", 14))
        title_label.pack(pady=10)

        self.title_entry = tk.Entry(self.task_window, font=("Helvetica", 14))
        self.title_entry.insert(0, task['title'])
        self.title_entry.pack(pady=10)

        desc_label = tk.Label(self.task_window, text="Description", font=("Helvetica", 14))
        desc_label.pack(pady=10)

        self.desc_entry = tk.Text(self.task_window, font=("Helvetica", 14), height=4)
        self.desc_entry.insert("1.0", task['description'])
        self.desc_entry.pack(pady=10)

        priority_label = tk.Label(self.task_window, text="Priority (Low, Medium, High)", font=("Helvetica", 14))
        priority_label.pack(pady=10)

        self.priority_entry = tk.Entry(self.task_window, font=("Helvetica", 14))
        self.priority_entry.insert(0, task['priority'])
        self.priority_entry.pack(pady=10)

        due_date_label = tk.Label(self.task_window, text="Due Date (YYYY-MM-DD)", font=("Helvetica", 14))
        due_date_label.pack(pady=10)

        self.due_date_entry = tk.Entry(self.task_window, font=("Helvetica", 14))
        self.due_date_entry.insert(0, task['due_date'])
        self.due_date_entry.pack(pady=10)

        save_button = tk.Button(self.task_window, text="Save Changes", command=lambda: self.update_task(index))
        save_button.pack(pady=10)

    def update_task(self, index):
        title = self.title_entry.get()
        description = self.desc_entry.get("1.0", "end-1c")
        priority = self.priority_entry.get()
        due_date = self.due_date_entry.get()

        if not title:
            messagebox.showwarning("Input Error", "Task title is required.")
            return

        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid date in YYYY-MM-DD format.")
                return

        self.tasks[index] = {
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "completed": self.tasks[index]["completed"]
        }

        self.save_tasks()
        self.update_tasks_list()
        self.task_window.destroy()

    def complete_task(self, index):
        self.tasks[index]["completed"] = True
        self.save_tasks()
        self.update_tasks_list()

    def delete_task(self, index):
        del self.tasks[index]
        self.save_tasks()
        self.update_tasks_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
