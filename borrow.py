import tkinter as tk
from datetime import datetime
import sqlite3
from issuereport import show_issue_report_popup

def show_borrow_screen(root, back_callback):
    # --- Function to record borrow ---
    def record_borrow(barcode):
        conn = sqlite3.connect("faculty_account.db")
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT id, name FROM equipment WHERE barcode = ?", (barcode,))
            result = cursor.fetchone()
            if result:
                equipment_id, item_name = result
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                borrower_email = "faculty@nursing.com"   # TODO: replace with logged-in user
                borrower_name = borrower_email           # ✅ use email as borrower_name

                # Insert into borrow table
                cursor.execute("""
                    INSERT INTO borrow (equipment_id, barcode, borrow_time)
                    VALUES (?, ?, ?)
                """, (equipment_id, barcode, timestamp))

                # Insert into transactions table
                cursor.execute("""
                    INSERT INTO transactions (
                        datetime,
                        borrower_name,
                        borrower_email,
                        equipment_name,
                        barcode,
                        action,
                        status,
                        handled_by,
                        remarks
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    timestamp,
                    borrower_name,
                    borrower_email,
                    item_name,
                    barcode,
                    "Borrowed",
                    "Ongoing",
                    "Custodian 1",
                    "N/A"
                ))

                conn.commit()
                status_label.config(
                    text=f"Scanned: {barcode} ({item_name})\nTime: {timestamp}\nStatus: Borrow recorded ✅",
                    fg="green"
                )
            else:
                status_label.config(text="Error: Equipment ID not found ❌", fg="red")
        except Exception as e:
            status_label.config(text=f"Database error: {e}", fg="red")
        finally:
            conn.close()

    # --- UI Setup ---
    for w in root.winfo_children():
        w.destroy()
    root.configure(bg="#f4f0f0")

    # Top bar
    top = tk.Frame(root, bg="#005c3c", height=60)
    top.pack(fill="x", side="top")
    tk.Button(top, text="←", font=("Arial", 18), fg="white", bg="#005c3c",
              border=0, command=back_callback).pack(side="left", padx=10)
    tk.Label(top, text="Borrow Equipment", font=("Arial", 16, "bold"),
             fg="white", bg="#005c3c").pack(side="left", padx=10)

    # Main content
    main = tk.Frame(root, bg="#f4f0f0")
    main.pack(fill="both", expand=True, padx=50, pady=30)

    tk.Label(main, text="Scan barcode to borrow", font=("Arial", 11)).pack(pady=(20, 5))

    scan_box = tk.Entry(main, font=("Arial", 16), width=50, justify="center", bd=2, relief="groove")
    scan_box.pack(pady=5, ipady=10)

    # When pressing Enter
    def on_enter(event):
        barcode = scan_box.get()
        if barcode:
            record_borrow(barcode)
            scan_box.delete(0, tk.END)

    scan_box.bind("<Return>", on_enter)

    # Status label (must exist before record_borrow is used)
    global status_label
    status_label = tk.Label(main, text="", font=("Arial", 10), bg="#f4f0f0")
    status_label.pack(pady=(20, 10))

    # Report link
    def report_issue():
        show_issue_report_popup(root)

    report = tk.Label(main, text="Report an Issue", fg="blue", cursor="hand2", font=("Arial", 9, "underline"))
    report.pack(pady=(5, 20))
    report.bind("<Button-1>", lambda e: report_issue())
