import tkinter as tk
from datetime import datetime
from issuereport import show_issue_report_popup



def show_return_screen(root, back_callback):
    for w in root.winfo_children():
        w.destroy()
    root.configure(bg="#f4f0f0")

    # Top bar
    top = tk.Frame(root, bg="#005c3c", height=60)
    top.pack(fill="x", side="top")

    tk.Label(top, text=" ", bg="#005c3c", width=2).pack(side="left")  # spacing
    tk.Button(top, text="←", font=("Arial", 18), fg="white", bg="#005c3c", border=0,
              command=back_callback).pack(side="left", padx=10)
    tk.Label(top, text="Return Equipment", font=("Arial", 16, "bold"), fg="white", bg="#005c3c").pack(side="left", padx=10)

    # Main content
    main = tk.Frame(root, bg="#f4f0f0")
    main.pack(fill="both", expand=True, padx=50, pady=30)

    tk.Label(main, text="Scan barcode to return", font=("Arial", 11)).pack(pady=(20, 5))

    scan_box = tk.Entry(main, font=("Arial", 16), width=50, justify="center", bd=2, relief="groove")
    scan_box.pack(pady=5, ipady=10)

    tk.Label(main, text="Or enter barcode manually", font=("Arial", 10)).pack(pady=(20, 5))

    manual_frame = tk.Frame(main, bg="#f4f0f0")
    manual_frame.pack(pady=5)
    manual_input = tk.Entry(manual_frame, width=40, font=("Arial", 12), relief="groove", bd=2)
    manual_input.pack(side="left", ipady=5, padx=(0, 10))
    submit_btn = tk.Button(manual_frame, text="Submit", width=10, bg="#f4bcbc")
    submit_btn.pack(side="left")

    # Simulated data
    scanned_code = "0900101001"
    item_name = "Microscope #1"
    timestamp = datetime.now().strftime("%m/%d/%y %I:%M:%S %p")

    # Display scanned info
    tk.Label(main, text=f"Scanned:  {scanned_code}  ({item_name})  Date and Time: {timestamp}",
             font=("Arial", 9)).pack(pady=(30, 5))
    tk.Label(main, text="Status: Successfully borrowed/recorded", font=("Arial", 9)).pack()

    # Report link
    def report_issue():
     show_issue_report_popup(root)

    report = tk.Label(main, text="Report an Issue", fg="blue", cursor="hand2", font=("Arial", 9, "underline"))
    report.pack(pady=(5, 20))
    report.bind("<Button-1>", lambda e: report_issue())
