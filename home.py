import tkinter as tk
from PIL import Image, ImageTk  #for images
from profsettings import show_profile_settings
from browsecatalog import show_browse_catalog  
from borrow import show_borrow_screen
from returnequipment import show_return_screen
from facultyhistory import show_faculty_history  

def show_homepage(root: tk.Tk):
    
    #clear window first
    for w in root.winfo_children():
        w.destroy()
    root.configure(bg="#fbb3bb")  

    #top bar
    top = tk.Frame(root, bg="#005c3c", height=80)
    top.pack(fill="x", side="top")

    #try to load logo, if d nagload show text
    try:
        logo_img = Image.open("ion_logo.png").resize((50, 50))
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo = tk.Label(top, image=logo_photo, bg="#005c3c")
        logo.image = logo_photo 
    except Exception:
        logo = tk.Label(top, text="ION", bg="#005c3c", fg="white", font=("Arial", 20, "bold"))
    logo.pack(side="left", padx=(20, 0), pady=10)

    #computer icon
    tk.Label(top, text="🖥️", bg="#005c3c", font=("Arial", 20)).pack(side="right", padx=10, pady=10)

    #for menu
    menu_shown = tk.BooleanVar(value=False)

    #user menu(pop up if clicked)
    user_menu = tk.Toplevel(root)
    user_menu.withdraw()  #hide
    user_menu.overrideredirect(True)  #remove window border
    user_menu.transient(root)
    user_menu.configure(bg="white", bd=1, relief="solid")
    user_menu.lift()

    #menu buttons, Settings and Logout
    tk.Button(user_menu, text="Settings", relief="flat", bg="white",
              command=lambda: [user_menu.withdraw(), show_profile_settings(root, back_callback=lambda: show_homepage(root))]).pack(fill="x", padx=5, pady=(5, 2))
    tk.Button(user_menu, text="Logout", relief="flat", bg="white",
              command=lambda: print("Logged out")).pack(fill="x", padx=5, pady=(2, 5))

    #function to show or hide the user menu
    def toggle_menu(event=None):
        if menu_shown.get():
            user_menu.withdraw()
            menu_shown.set(False)
        else:
            root.update_idletasks()
            x = user_icon.winfo_rootx()
            y = user_icon.winfo_rooty() + user_icon.winfo_height()
            user_menu.geometry(f"+{x}+{y}")
            user_menu.deiconify()
            menu_shown.set(True)

    #user icon to open menu
    user_icon = tk.Label(top, text="👤", bg="#005c3c", font=("Arial", 24), cursor="hand2")
    user_icon.pack(side="right", padx=(10, 20), pady=10)
    user_icon.bind("<Button-1>", toggle_menu)  # Click to open menu

    #hide the menu if clicked outside
    def hide_on_click_outside(event):
        if menu_shown.get() and not user_menu.winfo_containing(event.x_root, event.y_root):
            toggle_menu()
    root.bind_all("<Button-1>", hide_on_click_outside, "+")

    #main content area
    main = tk.Frame(root, bg="#f4f0f0")
    main.pack(expand=True, fill="both")

    #heading texts
    tk.Label(main, text="Faculty Equipment Portal",
             font=("Arial", 20, "bold"), bg="#f4f0f0").pack(pady=(30, 5))
    tk.Label(main,
             text="Browse, borrow, and manage laboratory equipment for your research and classes",
             font=("Arial", 12), bg="#f4f0f0").pack()

    #function to create a card (box with icon, title, desc, button)
    def card(parent, title, desc, btn_text, r, c):
        frame = tk.Frame(parent, bg="white", width=200, height=150,
                         bd=1, relief="raised")
        frame.grid(row=r, column=c, padx=20, pady=20)
        frame.grid_propagate(False)  

        #emojis
        icons = {"Browse Equipment": "🔍", "Borrow Equipment": "➡️",
                 "Return Equipment": "↩️", "View History": "📋"}
        tk.Label(frame, text=icons.get(title, ""), bg="#f4bcbc",
                 font=("Arial", 20), width=22).pack(fill="x")
        tk.Label(frame, text=title, font=("Arial", 12, "bold"),
                 bg="white").pack(pady=(5, 0))
        tk.Label(frame, text=desc, wraplength=180, font=("Arial", 10),
                 bg="white").pack(pady=(0, 5))

        #button actions
        action = lambda: None
        if title == "Browse Equipment":
            action = lambda: show_browse_catalog(root, back_callback=lambda: show_homepage(root))
        if title == "Borrow Equipment":
            action = lambda: show_borrow_screen(root, back_callback=lambda: show_homepage(root))
        if title == "Return Equipment":
            action = lambda: show_return_screen(root, back_callback=lambda: show_homepage(root))
        if title == "View History":
            action = lambda: show_faculty_history(root, back_callback=lambda: show_homepage(root))

        tk.Button(frame, text=btn_text, bg="#f4bcbc", relief="flat",
                  width=10, command=action).pack(pady=(0, 10))

    #place cards in a grid layout
    grid = tk.Frame(main, bg="#f4f0f0")
    grid.pack()
    card(grid, "Browse Equipment", "Search and filter available laboratory equipment.", "Browse", 0, 0)
    card(grid, "Borrow Equipment", "Submit request to borrow laboratory equipment.", "Request", 0, 1)
    card(grid, "Return Equipment", "Process returns for items you’ve borrowed", "Return", 1, 0)
    card(grid, "View History", "View your equipment borrowing history", "View", 1, 1)
    
     # --- Notification Section ---
    notif_section = tk.Frame(main, bg="white", bd=1, relief="solid", width=300, height=300)
    notif_section.pack(side="right", padx=40, pady=40, anchor="n")
    notif_section.pack_propagate(False)

    tk.Label(notif_section, text="🔔 Notifications", font=("Arial", 12, "bold"),
             bg="white").pack(pady=(10, 5))
    tk.Label(notif_section, text="No new notifications.", font=("Arial", 10), 
             bg="white", fg="gray").pack(pady=(5, 10))

#run file
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Home - Demo")
    root.geometry("1920x1080")  #full screen window size
    show_homepage(root)
    root.mainloop()
