# loginform.py 
import subprocess
import sqlite3
import tkinter as tk
from tkinter import Entry, Label, Frame, Button, Checkbutton, IntVar, messagebox
from PIL import Image, ImageTk
from home import show_homepage

def show_login_form(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#fbb3bb")

    # Load and display logo
    logo_img = Image.open("ion_logo.png").resize((150, 130))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = Label(root, image=logo_photo, bg="#fbb3bb")
    logo_label.image = logo_photo
    logo_label.pack(pady=(80, 10), padx=(0, 10))

    Label(root, text="Institute of Nursing", font=("Helvetica", 12, "bold"), bg="#fbb3bb").pack()
    Label(root, text="Laboratory Equipment Management System", font=("Helvetica", 16, "bold"), bg="#fbb3bb").pack(pady=(0, 20))

    form_frame = Frame(root, bg="white", bd=0, relief="raised")
    form_frame.pack(pady=10)
    form_frame.configure(highlightthickness=0, padx=50, pady=30)

    Label(form_frame, text="Login", font=("Helvetica", 20, "bold"), bg="white", fg="#333").pack(pady=(0, 20))

    Label(form_frame, text="Email", font=("Helvetica", 12, "bold"), bg="white", anchor="w").pack(fill="x")
    email_entry = Entry(form_frame, font=("Helvetica", 12), width=30, relief="ridge", bd=3)
    email_entry.pack(pady=(0, 15))

    Label(form_frame, text="Password", font=("Helvetica", 12, "bold"), bg="white", anchor="w").pack(fill="x")
    password_entry = Entry(form_frame, font=("Helvetica", 12), width=30, relief="ridge", bd=3, show="*")
    password_entry.pack(pady=(0, 5))

   # Show password 
    show_pass_var = IntVar()
    def toggle_password():
        if show_pass_var.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    Checkbutton(form_frame, text="Show Password", variable=show_pass_var,
                bg="white", command=toggle_password).pack(anchor="w", pady=(0, 10))

    Label(form_frame, text="Forgot Password?", font=("Helvetica", 9), bg="white", fg="black").pack(anchor="e")
    def attempt_login():
        email = email_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect("faculty_account.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            show_homepage(root)
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

    login_btn = Button(
        root,
        text="LOGIN",
        font=("Helvetica", 14, "bold"),
        bg="white",
        fg="#e84e89",
        padx=30,
        pady=10,
        relief="flat",
        command=attempt_login
    )
    login_btn.pack(pady=(20, 0))
