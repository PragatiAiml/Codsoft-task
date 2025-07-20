import tkinter as tk
from tkinter import messagebox

class SimpleRoundCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Basic Calculator")
        master.geometry("320x500")
        master.resizable(False, False)
        master.configure(bg="#F0F0F0")

        self.expression = ""
        self.history = []
       
        self.display_frame = tk.Frame(master, bg="#333333", bd=5, relief="ridge")
        self.display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.history_label = tk.Label(self.display_frame, text="", font=("Arial", 12), fg="#AAAAAA", bg="#333333", anchor="e")
        self.history_label.pack(fill=tk.X, padx=5, pady=(5,0))

        self.input_field = tk.Entry(self.display_frame, font=("Arial", 28, "bold"), textvariable=tk.StringVar(),
                                     bg="#333333", fg="white", bd=0, insertbackground="white", justify="right")
        self.input_field.pack(fill=tk.X, padx=5, pady=(0,5))
        self.input_field.focus_set()

        self.create_calculator_buttons(master)
        self.bind_keys()

    def create_calculator_buttons(self, parent_frame):
        button_frame = tk.Frame(parent_frame, bg="#F0F0F0")
        button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
       
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)

        buttons = [
           
            ("AC", 0, 0, self.clear_all, "clear"), ("(", 0, 1, lambda: self.append_to_expression("("), "operator"),
            (")", 0, 2, lambda: self.append_to_expression(")"), "operator"), ("/", 0, 3, lambda: self.append_to_expression("/"), "operator_last_col"),

            ("7", 1, 0, lambda: self.append_to_expression("7"), "number"), ("8", 1, 1, lambda: self.append_to_expression("8"), "number"),
            ("9", 1, 2, lambda: self.append_to_expression("9"), "number"), ("*", 1, 3, lambda: self.append_to_expression("*"), "operator_last_col"),
           
            ("4", 2, 0, lambda: self.append_to_expression("4"), "number"), ("5", 2, 1, lambda: self.append_to_expression("5"), "number"),
            ("6", 2, 2, lambda: self.append_to_expression("6"), "number"), ("-", 2, 3, lambda: self.append_to_expression("-"), "operator_last_col"),
           
            ("1", 3, 0, lambda: self.append_to_expression("1"), "number"), ("2", 3, 1, lambda: self.append_to_expression("2"), "number"),
            ("3", 3, 2, lambda: self.append_to_expression("3"), "number"), ("+", 3, 3, lambda: self.append_to_expression("+"), "operator_last_col"),
           
            ("DEL", 4, 0, self.delete_last_char, "clear"),
            ("0", 4, 1, lambda: self.append_to_expression("0"), "number"),
            (".", 4, 2, lambda: self.append_to_expression("."), "number"),
            ("=", 4, 3, self.calculate_result, "equals_last_col")
        ]

        for (text, row, col, command, btn_type) in buttons:
            btn_color = "#424242"
            text_color = "white"
            active_bg_color = "#616161"

            if btn_type == "operator":
                btn_color = "#616161"
                active_bg_color = "#757575"
            elif btn_type == "operator_last_col":
                btn_color = "#FF9800"
                active_bg_color = "#FFB74D"
            elif btn_type == "clear":
                btn_color = "#FF5722"
                active_bg_color = "#FF8A65"
            elif btn_type == "equals_last_col":
                btn_color = "#4CAF50"
                active_bg_color = "#81C784"

            button = tk.Button(button_frame, text=text, command=command,
                               font=("Arial", 18, "bold"), bg=btn_color, fg=text_color,
                               bd=0, relief="flat",
                               padx=1, pady=1,
                               activebackground=active_bg_color,
                               activeforeground=text_color,
                               highlightbackground="#F0F0F0",
                               highlightthickness=0
                               )
            button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

    def append_to_expression(self, value):
        self.expression += str(value)
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, self.expression)
        self.history_label.config(text=self.expression)

    def calculate_result(self):
        try:
            if '%' in self.expression:
                self.expression = self.expression.replace('%', '*0.01')
            result = eval(self.expression)
            self.add_to_history(f"{self.expression} = {result}")
            self.expression = str(result)
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, self.expression)
            self.history_label.config(text="")

        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero!")
            self.clear_all()
        except SyntaxError:
            messagebox.showerror("Error", "Invalid expression!")
            self.clear_all()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.clear_all()

    def clear_all(self):
        self.expression = ""
        self.input_field.delete(0, tk.END)
        self.history_label.config(text="")

    def delete_last_char(self):
        self.expression = self.expression[:-1]
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, self.expression)
        self.history_label.config(text=self.expression)

    def add_to_history(self, entry):
        self.history.append(entry)
        print(f"History: {entry}")

    def bind_keys(self):
        self.master.bind("<Key>", self.handle_key_press)
        self.master.bind("<Return>", lambda event: self.calculate_result())
        self.master.bind("<BackSpace>", lambda event: self.delete_last_char())
        self.master.bind("<Escape>", lambda event: self.clear_all())

    def handle_key_press(self, event):
        key = event.char
        if key.isdigit() or key in "+-*/.()%":
            self.append_to_expression(key)
        elif key == "=":
            self.calculate_result()
        elif key == '\x08':
            self.delete_last_char()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleRoundCalculator(root)
    root.mainloop()