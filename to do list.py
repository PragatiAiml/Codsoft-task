import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 My To-Do List")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.tasks = []

        # Title
        tk.Label(root, text="To-Do List", font=("Arial", 20, "bold")).pack(pady=10)

        # Task Entry
        self.task_entry = tk.Entry(root, font=("Arial", 14))
        self.task_entry.pack(pady=10, padx=20, fill=tk.X)
        self.task_entry.bind('<Return>', lambda event: self.add_task())

        # Add Button
        tk.Button(root, text="Add Task", command=self.add_task, bg="#28a745", fg="white", font=("Arial", 12)).pack(pady=5)

        # Task Listbox
        self.task_listbox = tk.Listbox(root, font=("Arial", 12), selectmode=tk.SINGLE)
        self.task_listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Control Buttons
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Mark Done", command=self.mark_done, bg="#007bff", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Delete", command=self.delete_task, bg="#dc3545", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Save", command=self.save_tasks, bg="#6c757d", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="Load", command=self.load_tasks, bg="#ffc107", fg="black").grid(row=0, column=3, padx=5)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append({"task": task, "done": False})
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty!")

    def mark_done(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            self.tasks[index]['done'] = not self.tasks[index]['done']
            self.update_listbox()
        else:
            messagebox.showinfo("No Selection", "Please select a task to mark as done.")

    def delete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            del self.tasks[selection[0]]
            self.update_listbox()
        else:
            messagebox.showinfo("No Selection", "Please select a task to delete.")

    def save_tasks(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file:
            with open(file, "w") as f:
                for t in self.tasks:
                    line = f"{t['task']}||{t['done']}\n"
                    f.write(line)
            messagebox.showinfo("Saved", "Tasks saved successfully!")

    def load_tasks(self):
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file and os.path.exists(file):
            with open(file, "r") as f:
                self.tasks.clear()
                for line in f:
                    parts = line.strip().split("||")
                    if len(parts) == 2:
                        self.tasks.append({"task": parts[0], "done": parts[1] == 'True'})
                self.update_listbox()

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for t in self.tasks:
            text = f"[✔] {t['task']}" if t['done'] else f"[ ] {t['task']}"
            self.task_listbox.insert(tk.END, text)

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()