import sqlite3
import tkinter as tk
from tkinter import ttk

def show_faculty_history(root, back_callback):
    # clear window
    for w in root.winfo_children():
        w.destroy()
    root.configure(bg="white")

    # top bar
    top = tk.Frame(root, bg="#005c3c", height=60)
    top.pack(fill="x", side="top")

    back_btn = tk.Button(top, text="←", font=("Arial", 16), bg="#005c3c", fg="white",
                         relief="flat", command=back_callback)
    back_btn.pack(side="left", padx=15, pady=10)

    tk.Label(top, text="Transaction History", bg="#005c3c", fg="white",
             font=("Arial", 16, "bold")).pack(side="left", padx=10)

    # search bar
    search_frame = tk.Frame(root, bg="white")
    search_frame.pack(pady=15)
    search_entry = tk.Entry(search_frame, width=40, relief="solid")
    search_entry.insert(0, "Search by borrower name, equipment, or date..")
    search_entry.pack(side="left", padx=(0,5))
    tk.Button(search_frame, text="Search", relief="solid").pack(side="left")

    # table
    columns = ("TRANSACTION ID", "DATE/TIME", "BORROWER NAME", "BORROWER EMAIL",
               "EQUIPMENT", "BARCODE ID", "ACTION", "STATUS", "HANDLED BY")
    
    tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
    tree.pack(fill="both", expand=True, padx=20, pady=10)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    # connect DB and fetch transactions
    conn = sqlite3.connect("faculty_account.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()

    # insert into table
    for row in rows:
        tree.insert("", "end", values=row)

