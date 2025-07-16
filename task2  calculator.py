import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        operation = operation_var.get()

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                messagebox.showerror("Error", "Division by zero is not allowed")
                return
            result = num1 / num2
        else:
            messagebox.showerror("Error", "Please select a valid operation")
            return

        result_label.config(text=f"Result: {result}")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

# Create main window
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x300")

# Input fields
tk.Label(root, text="Enter first number:").pack()
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="Enter second number:").pack()
entry2 = tk.Entry(root)
entry2.pack()

# Operation selection
tk.Label(root, text="Select Operation:").pack()
operation_var = tk.StringVar()
operation_var.set('+')  # default value

tk.OptionMenu(root, operation_var, '+', '-', '*', '/').pack()

# Calculate button