import tkinter as tk


def show_issue_report_popup(root):
    popup = tk.Toplevel(root)
    popup.grab_set()
    popup.title("Report Issue")
    popup.geometry("600x500")
    popup.configure(bg="#ffffff")
    popup.transient(root)
    popup.resizable(False, False)

    # Center the window on screen
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() - popup.winfo_reqwidth()) // 3
    y = (popup.winfo_screenheight() - popup.winfo_reqheight()) // 3
    popup.geometry(f"+{x}+{y}")

    # Container
    container = tk.Frame(popup, bg="white", padx=20, pady=20)
    container.pack(expand=True, fill="both")


    # Title
    tk.Label(container, text="REPORT EQUIPMENT PROBLEM", font=("Arial", 12, "bold"), bg="white").pack(pady=(10, 5))

    # Description
    tk.Label(container, text="Use this form to report any issues with laboratory equipment",
             font=("Arial", 9), bg="white").pack()

    # Text box
    issue_entry = tk.Text(container, width=60, height=8, font=("Arial", 10))
    issue_entry.pack(pady=10)

    # Submit button
    def submit_issue():
     issue_text = issue_entry.get("1.0", "end").strip()
     if issue_text:
        # Confirmation dialog
        confirm = tk.Toplevel(popup)
        confirm.grab_set()
        confirm.title("Success")
        confirm.geometry("400x200")
        confirm.configure(bg="white")
        confirm.transient(popup)
        confirm.resizable(False, False)

        # Center the confirmation popup
        confirm.update_idletasks()
        x = (confirm.winfo_screenwidth() - confirm.winfo_reqwidth()) // 2
        y = (confirm.winfo_screenheight() - confirm.winfo_reqheight()) // 2
        confirm.geometry(f"+{x}+{y}")

        # Content
        frame = tk.Frame(confirm, bg="white")
        frame.pack(expand=True)

        tk.Label(frame, text="REPORT", font=("Arial", 11, "bold"), bg="white").pack(pady=(20, 5))
        tk.Label(frame, text="Successfully Submitted!", font=("Arial", 10), bg="white").pack()

        def close_all():
            confirm.destroy()
            popup.destroy()

        tk.Button(frame, text="OK", font=("Arial", 10, "bold"), bg="#007b3c", fg="white",
                  width=8, pady=2, command=close_all).pack(pady=(15, 10))


    submit_btn = tk.Button(container, text="SUBMIT", bg="#007b3c", fg="white", font=("Arial", 10, "bold"),
                           padx=20, pady=5, command=submit_issue)
    submit_btn.pack(pady=(10, 0))
   
