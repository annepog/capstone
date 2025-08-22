import tkinter as tk
from tkinter import messagebox, Spinbox
from tkcalendar import DateEntry
import sqlite3

def show_reserve_form(root, equipment_name, equipment_id, user_email, back_callback):
    for w in root.winfo_children():
        w.destroy()
    root.configure(bg="#f4f0f0")

    # Top bar
    top = tk.Frame(root, bg="#005c3c", height=60)
    top.pack(fill="x")
    tk.Button(top, text="←", font=("Arial", 16), bg="#005c3c", fg="white", border=0,
              command=back_callback).pack(side="left", padx=10)
    tk.Label(top, text="RESERVE Equipment", font=("Arial", 14), bg="#005c3c", fg="white").pack(side="left")

    tk.Label(root, text="Reserve Equipment", font=("Arial", 14, "bold"), bg="#f4f0f0").pack(pady=10)

    form = tk.Frame(root, bg="#dedede", padx=20, pady=20)
    form.pack()

    def add_field(label, row, widget):
        tk.Label(form, text=label, bg="#dedede", anchor="w").grid(row=row, column=0, sticky="w", pady=5)
        widget.grid(row=row, column=1, pady=5)
        return widget

    # Equipment Name (readonly)
    equipment_entry = tk.Entry(form, width=25)
    equipment_entry.insert(0, equipment_name)
    equipment_entry.config(state="readonly")
    add_field("Equipment Name", 0, equipment_entry)

    # Quantity (Spinbox)
    quantity_entry = Spinbox(form, from_=1, to=20, width=23)
    add_field("Quantity", 1, quantity_entry)

    # Date Needed (Calendar)
    date_entry = DateEntry(form, width=21, background="darkgreen", foreground="white", borderwidth=2)
    add_field("Date Needed", 2, date_entry)

    # Purpose of Use
    purpose_entry = tk.Entry(form, width=25)
    add_field("Purpose of Use", 3, purpose_entry)

    # Duration of Use
    duration_entry = tk.Entry(form, width=25)
    add_field("Duration of Use", 4, duration_entry)

    # Additional Notes
    notes_entry = tk.Entry(form, width=25)
    add_field("Additional Notes (optional)", 5, notes_entry)

    # Buttons
    button_frame = tk.Frame(form, bg="#dedede")
    button_frame.grid(row=6, columnspan=2, pady=15)

    tk.Button(button_frame, text="Cancel", bg="#aaa", fg="white", width=12,
              command=back_callback).pack(side="left", padx=10)

    def confirm():
        quantity = quantity_entry.get()
        date_needed = date_entry.get()
        purpose = purpose_entry.get()
        duration = duration_entry.get()
        notes = notes_entry.get()

        if not quantity or not date_needed or not purpose or not duration:
            messagebox.showwarning("Incomplete", "Please fill out all required fields.")
            return

        conn = sqlite3.connect("faculty_account.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO reservations (equipment_id, user_email, quantity, date_needed, purpose, duration, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (equipment_id, user_email, quantity, date_needed, purpose, duration, notes))
        conn.commit()
        conn.close()

        messagebox.showinfo("Reservation Submitted",
                            f"Your reservation for {equipment_name} has been submitted!\nWait for custodian approval.")
        back_callback()

    tk.Button(button_frame, text="Confirm Reservation", bg="#3498db", fg="white",
              width=20, command=confirm).pack(side="left")
