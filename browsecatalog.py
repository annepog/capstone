import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
from equipment_details import show_equipment_details
from reservationform import show_reserve_form
 


#UI Setup
def show_browse_catalog(root, back_callback):
    for w in root.winfo_children():
        w.destroy()
    root.configure(bg="black")

    # Top bar
    top = tk.Frame(root, bg="#005c3c", height=60)
    top.pack(fill="x", side="top")

    tk.Button(top, text="←", font=("Arial", 16), bg="#005c3c", fg="white", border=0,
              command=back_callback).pack(side="left", padx=10)
    tk.Label(top, text="Find Equipment", font=("Arial", 16), bg="#005c3c", fg="white").pack(side="left", padx=10)

    # Search bar
    search_area = tk.Frame(root, bg="#f4f0f0")
    search_area.pack(fill="x", pady=20)
    tk.Entry(search_area, width=40).pack(side="left", padx=20)
    tk.Button(search_area, text="Search").pack(side="left")
    tk.OptionMenu(search_area, tk.StringVar(value="All Categories"), "All Categories", "Category A", "Category B").pack(side="left", padx=10)
    tk.OptionMenu(search_area, tk.StringVar(value="Any Laboratory"), "Any Laboratory", "Lab 1", "Lab 2").pack(side="left")

    # Scrollable frame setup
    catalog_frame = tk.Frame(root, bg="#f4f0f0")
    catalog_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(catalog_frame, bg="#f4f0f0", highlightthickness=0)
    scrollbar = tk.Scrollbar(catalog_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f4f0f0")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    #Mousewheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    def _on_mousewheel_mac(event):
        canvas.yview_scroll(-1 * event.delta, "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", _on_mousewheel_mac)
    canvas.bind_all("<Button-5>", _on_mousewheel_mac)

    
    # Connect and get equipment from DB
    conn = sqlite3.connect("faculty_account.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM equipment")
    equipment = cursor.fetchall()
    conn.close()

    #center the equipment grid
    wrapper = tk.Frame(scrollable_frame, bg="#f4f0f0")
    wrapper.pack(fill="both")

    center_container = tk.Frame(wrapper, bg="#f4f0f0")
    center_container.grid(row=3, column=3)
    wrapper.grid_columnconfigure(0, weight=1)

    #Create equipment cards in a 2-column layout
    for idx, (eid, name, desc) in enumerate(equipment):
        frame = tk.Frame(center_container, bg="white", bd=1, relief="solid", width=400, height=320)
        frame.grid(row=idx//2, column=idx%2, padx=40, pady=20)
        frame.grid_propagate(False)

        tk.Label(frame, bg="#eee", width=40, height=8).pack(pady=(15, 5))
        tk.Label(frame, text=name, font=("Arial", 13, "bold"), bg="white", wraplength=300).pack(pady=(0, 2))
        tk.Label(frame, text=desc, font=("Arial", 10), bg="white", wraplength=300, justify="center").pack(pady=(0, 10))
        tk.Button(
        frame,
        text="Reserve",
        bg="#f4bcbc",
        relief="flat",
        width=15,
        command=lambda eid=eid, name=name: show_reserve_form(
            root,
            equipment_name=name,
            equipment_id=eid,
            user_email="faculty@nursing.com",  # ⚠️ Replace this with the logged-in user email if available
            back_callback=lambda: show_browse_catalog(root, back_callback)
          )
         ).pack()


    