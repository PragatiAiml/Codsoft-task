import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import os


class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TODO LIST")
        self.root.geometry("700x600")
        self.root.configure(bg="#f6f6fd")

        self.tasks = []
        self.filter = tk.StringVar(value="All")

        self.build_ui()
        self.render_tasks()

    def build_ui(self):
        title = tk.Label(self.root, text="TODO LIST", font=("Segoe UI Black", 24), bg="#f6f6fd", fg="#444")
        title.pack(pady=20)

        top_frame = tk.Frame(self.root, bg="#f6f6fd")
        top_frame.pack(pady=10, padx=20, fill="x")

        self.task_entry = tk.Entry(top_frame, font=("Segoe UI", 12), bd=0, relief="flat")
        self.task_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))

        add_btn = tk.Button(top_frame, text="Add Task", bg="#6C63FF", fg="white",
                            font=("Segoe UI Semibold", 10), padx=15, pady=5, bd=0,
                            activebackground="#5848e5", command=self.add_task)
        add_btn.pack(side="left")

        right_frame = tk.Frame(self.root, bg="#f6f6fd")
        right_frame.pack(pady=5, padx=20, fill="x")

        options = ["All", "Pending", "Completed"]
        self.filter_dropdown = ttk.Combobox(right_frame, textvariable=self.filter, values=options,
                                            state="readonly", width=10)
        self.filter_dropdown.pack(side="right")
        self.filter_dropdown.bind("<<ComboboxSelected>>", lambda e: self.render_tasks())

        self.task_container = tk.Frame(self.root, bg="#f6f6fd")
        self.task_container.pack(fill="both", expand=True, padx=20, pady=10)

        bottom = tk.Frame(self.root, bg="#f6f6fd")
        bottom.pack(pady=10)

        tk.Button(bottom, text="💾 Save", command=self.save_tasks, font=("Segoe UI", 10)).pack(side="left", padx=5)
        tk.Button(bottom, text="📂 Load", command=self.load_tasks, font=("Segoe UI", 10)).pack(side="left", padx=5)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Task cannot be empty.")
            return
        timestamp = datetime.now().strftime("%I:%M %p, %d/%m/%Y")
        self.tasks.append({"text": task_text, "done": False, "time": timestamp})
        self.task_entry.delete(0, tk.END)
        self.render_tasks()

    def render_tasks(self):
        for widget in self.task_container.winfo_children():
            widget.destroy()

        show_tasks = self.get_filtered_tasks()

        for i, task in enumerate(show_tasks):
            self.render_single_task(task, i)


    def render_single_task(self, task, index):
        frame = tk.Frame(self.task_container, bg="#E0F2F7", bd=0, highlightthickness=1,
                        highlightbackground="#B3E0F2", relief="flat")  # Pastel blue with border
        frame.pack(fill="x", pady=7, ipady=10, padx=15)

        var = tk.BooleanVar(value=task["done"])

        check_btn = tk.Checkbutton(frame, variable=var, command=lambda: self.toggle_done(task),
                                bg="#E0F2F7", activebackground="#D5EDF3", bd=0, relief="flat")
        check_btn.pack(side="left", padx=(15, 10))

        # Task Label
        text_style = ("Segoe UI Semibold", 11)
        task_lbl = tk.Label(frame, text=task["text"], font=text_style, bg="#E0F2F7")
        if task["done"]:
            task_lbl.config(fg="#888888", font=(text_style[0], text_style[1], "overstrike"))
        else:
            task_lbl.config(fg="#333333")
        task_lbl.pack(side="left", anchor="w", padx=(0, 10), expand=True, fill="x")

        # Timestamp
        time_lbl = tk.Label(frame, text=task["time"], font=("Segoe UI", 9), fg="#999999", bg="#E0F2F7")
        time_lbl.pack(side="left", anchor="e", padx=(0, 15))

        # Button frame
        btn_frame = tk.Frame(frame, bg="#E0F2F7")
        btn_frame.pack(side="right", padx=(0, 10))

        # Delete Button
        del_btn = tk.Button(btn_frame, text="🗑", command=lambda: self.delete_task(task),
                            bd=1, bg="#D45454", activebackground="#D5EDF3", font=("Segoe UI", 10), fg="white")
        del_btn.pack(side="left", padx=(5, 2))

        # Edit Button
        edit_btn = tk.Button(btn_frame, text="🖉", command=lambda: self.edit_task(task),
                            bd=1, bg="#377485", activebackground="#D5EDF3", font=("Segoe UI", 10, "bold"), fg="white")
        edit_btn.pack(side="left", padx=(5, 2))

    def get_filtered_tasks(self):
        if self.filter.get() == "All":
            return self.tasks
        elif self.filter.get() == "Completed":
            return [t for t in self.tasks if t["done"]]
        else:
            return [t for t in self.tasks if not t["done"]]

    def toggle_done(self, task):
        task["done"] = not task["done"]
        self.render_tasks()

    def delete_task(self, task):
        self.tasks.remove(task)
        self.render_tasks()

    def edit_task(self, task):
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Task")
        edit_win.geometry("300x100")
        edit_win.resizable(False, False)

        entry = tk.Entry(edit_win, font=("Segoe UI", 11))
        entry.insert(0, task["text"])
        entry.pack(pady=10, padx=10, fill="x")

        def save_edit():
            new_text = entry.get().strip()
            if new_text:
                task["text"] = new_text
                self.render_tasks()
                edit_win.destroy()
            else:
                messagebox.showwarning("Error", "Task cannot be empty.")

        tk.Button(edit_win, text="Save", command=save_edit).pack()

    def save_tasks(self):
        file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file:
            try:
                with open(file, "w") as f:
                    json.dump(self.tasks, f, indent=4)
                messagebox.showinfo("Saved", "Tasks saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def load_tasks(self):
        file = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file:
            try:
                with open(file, "r") as f:
                    self.tasks = json.load(f)
                self.render_tasks()
            except Exception as e:
                messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
