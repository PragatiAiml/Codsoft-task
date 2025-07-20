import tkinter as tk
from tkinter import messagebox
import string
import random

class PasswordGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("400x460")
        self.root.configure(bg="#2d2e35")
        self.root.resizable(False, False)

        self.length_var = tk.IntVar(value=10)
        self.password_var = tk.StringVar()
        self.strength_var = tk.StringVar()

        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_numbers = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)

        self.create_widgets()
        self.generate_password()

    def create_widgets(self):
        
        # Outer frame simulating a single input field
        password_frame = tk.Frame(self.root, bg="#171717", bd=0)
        password_frame.pack(pady=10)

        # Entry widget inside the frame
        self.output_entry = tk.Entry(password_frame, textvariable=self.password_var,
                                    font=("Consolas", 12), bg="#151515",
                                    fg="#8aff80", relief="flat", justify="center", bd=0, width=30)
        self.output_entry.pack(side=tk.LEFT, ipady=10, padx=(10, 5))

        # Copy button styled to match inside the entry field
        copy_icon = "📋"
        copy_btn = tk.Button(password_frame, text=copy_icon, command=self.copy_to_clipboard,
                            bg="#171717", fg="#8aff80", activebackground="#171717",
                            relief="flat", bd=0, font=("Arial", 14), cursor="hand2")
        copy_btn.pack(side=tk.LEFT, ipady=6, padx=(0, 10))

        # Create a body frame to wrap the entire UI section
        body_frame = tk.Frame(self.root, bg="#171717", bd=0)
        body_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Character Length
        tk.Label(body_frame, text="Character Length", bg="#171717",
                fg="#ffffff", font=("Arial", 12)).pack(pady=(30, 5))

        # slider_frame = tk.Frame(body_frame, bg="#1b1c22")
        slider_frame = tk.Frame(body_frame, bg="#171717")
        slider_frame.pack(pady=(0, 20))

        self.length_slider = tk.Scale(slider_frame, from_=4, to=32,
                                    variable=self.length_var,
                                    orient=tk.HORIZONTAL, length=220,
                                    bg="#171717", fg="#8aff80",
                                    highlightthickness=0,
                                    troughcolor="#cfd4d1", sliderrelief="flat")
        self.length_slider.pack(side=tk.LEFT)

        self.length_label = tk.Label(slider_frame, textvariable=self.length_var,
                                    bg="#171717", fg="#8aff80", font=("Consolas", 12, "bold"))
        self.length_label.pack(side=tk.LEFT, padx=10, pady=(14, 0))

        # Checkboxes
        options = [
            ("Include Uppercase Letters", self.use_upper),
            ("Include Lowercase Letters", self.use_lower),
            ("Include Numbers", self.use_numbers),
            ("Include Symbols", self.use_symbols),
        ]

        for text, var in options:
            tk.Checkbutton(body_frame, text=text, variable=var,
                        bg="#1b1c22", fg="white", activebackground="#1b1c22",
                        selectcolor="#1b1c22", font=("Arial", 11), anchor="w").pack(padx=30, fill="x", pady=2)

        # Strength Label
        self.strength_label = tk.Label(body_frame, text="", font=("Arial", 11, "bold"),
                                    bg="#171717", fg="#ffcc00")
        self.strength_label.pack(pady=(20, 5))

        # Generate Button
        tk.Button(body_frame, text="GENERATE ➜", font=("Arial", 12, "bold"),
                command=self.generate_password, bg="#8aff80", fg="#1b1c22",
                relief="flat", cursor="hand2").pack(padx=30, fill="x", pady=(20, 0))

    def generate_password(self):
        length = self.length_var.get()
        chars = ""
        if self.use_upper.get():
            chars += string.ascii_uppercase
        if self.use_lower.get():
            chars += string.ascii_lowercase
        if self.use_numbers.get():
            chars += string.digits
        if self.use_symbols.get():
            chars += string.punctuation

        if not chars:
            messagebox.showerror("Error", "Please select at least one character set.")
            self.password_var.set("")
            return

        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)
        self.evaluate_strength(password)

    def evaluate_strength(self, password):
        length = len(password)
        score = 0
        if any(c.islower() for c in password): score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in string.punctuation for c in password): score += 1
        if length >= 12: score += 1

        levels = ["VERY WEAK", "WEAK", "MEDIUM", "STRONG", "VERY STRONG"]
        bars = ["▯▯▯▯▯", "▮▯▯▯▯", "▮▮▯▯▯", "▮▮▮▯▯", "▮▮▮▮▯", "▮▮▮▮▮"]
        self.strength_label.config(text=f"STRENGTH: {levels[min(score, 4)]}  {bars[score]}")

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()
            messagebox.showinfo("Copied", "Password copied to clipboard!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorUI(root)
    root.mainloop()
