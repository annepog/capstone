import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
from borrow import show_borrow_screen


def show_equipment_details(root, equipment_name, back_callback):
    for w in root.winfo_children():
        w.destroy()
    root.configure(bg="#f4f0f0")

    #fetch from db
    conn = sqlite3.connect("faculty_account.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, description, image_path, availability_status, category, usage_instruction
        FROM equipment
        WHERE name = ?
    """, (equipment_name,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        tk.Label(root, text="Equipment not found", fg="red", bg="white", font=("Arial", 16)).pack()
        return

    equipment_id, name, description, image_path, status, category, usage = result

    # Try loading image
    try:
        img = Image.open(image_path)
        img = img.resize((200, 200))
        photo = ImageTk.PhotoImage(img)
    except:
        photo = None
        
    
    #UI setup
    #Top Bar 
    top = tk.Frame(root, bg="#005c3c", height=60)
    top.pack(fill="x", side="top")
    tk.Label(top, text="Equipment Details", font=("Arial", 16, "bold"), bg="#005c3c", fg="white").pack(side="left", padx=20)

    #Card Container
    card = tk.Frame(root, bg="white", bd=1, relief="solid", highlightbackground="#ccc", highlightthickness=1)
    card.place(relx=0.5, rely=0.5, anchor="c", width=720, height=520)

    #Left: Image
    left = tk.Frame(card, bg="white", padx=30, pady=30)
    left.pack(side="left", fill="y")

    if photo:
        img_label = tk.Label(left, image=photo, bg="white")
        img_label.image = photo
        img_label.pack()
    else:
        tk.Label(left, text="No Image", bg="gray", fg="white", width=25, height=13).pack()

    #Right: Info
    right = tk.Frame(card, bg="white", padx=20, pady=30)
    right.pack(side="right", fill="both", expand=True)

    def make_label(master, text, bold=False, size=11, pady=0):
        font = ("Arial", size, "bold" if bold else "normal")
        return tk.Label(master, text=text, font=font, bg="white", anchor="w", justify="left")

    # Fields
    make_label(right, f"Equipment ID: {equipment_id:04}", bold=True).pack(anchor="w", pady=(0, 5))
    make_label(right, f"Name: {name}").pack(anchor="w", pady=(0, 5))
    make_label(right, f"Availability Status: {status}").pack(anchor="w", pady=(0, 5))
    make_label(right, f"Category: {category}").pack(anchor="w", pady=(0, 10))

    # Description
    make_label(right, "Description:", bold=True).pack(anchor="w", pady=(10, 0))
    make_label(right, description, size=10).pack(anchor="w", pady=(0, 10))

    # Usage
    make_label(right, "Usage Instruction:", bold=True).pack(anchor="w", pady=(5, 0))
    make_label(right, usage, size=10).pack(anchor="w")

    # Buttons
    btn_frame = tk.Frame(right, bg="white")
    btn_frame.pack(anchor="center", pady=20)

    btn_style = {"width": 12, "font": ("Arial", 10), "padx": 5, "pady": 5}
    tk.Button(btn_frame, text="Back", bg="#888", fg="white", command=back_callback, **btn_style).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Borrow", bg="#3baeff", fg="white",command=lambda: show_borrow_screen(root, lambda: show_equipment_details(root, equipment_name, back_callback)),
    **btn_style).pack(side="left", padx=10)

