import tkinter as tk
from PIL import Image, ImageTk


def show_profile_settings(root: tk.Tk, back_callback=None, profile=None):
    """Render the Profile Settings page on the given root window.

    Args:
        root (tk.Tk | tk.Frame): the window or frame to populate.
        back_callback (callable | None): called when the user presses the back arrow.
        profile (dict | None): mapping of field label -> value. If None, demo data is used.
    """
    # ------------------------------------------------------------------
    # Demo / fallback profile data
    # ------------------------------------------------------------------
    if profile is None:
        profile = {
            "Full Name": "Professor 1",
            "Employee ID": "KLD-24-001",
            "Email Address": "prof1@kld.edu.ph",
            "Contact No.": "+63 9987654241",
            "Department": "ION",
            "Position": "Professor",
        }

    # ------------------------------------------------------------------
    # 1. Clear the window and set a base background
    # ------------------------------------------------------------------
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#fbb3bb")  # soft pink like other pages

    # ------------------------------------------------------------------
    # 2. Top bar (logo only, same style as homepage)
    # ------------------------------------------------------------------
    top_bar = tk.Frame(root, bg="#005c3c", height=80)
    top_bar.pack(fill="x", side="top")

    # Try to load the logo; fall back to text if missing
    try:
        logo_img = Image.open("ion_logo.png").resize((50, 50))
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_lbl = tk.Label(top_bar, image=logo_photo, bg="#005c3c")
        logo_lbl.image = logo_photo  # keep reference
    except Exception:
        logo_lbl = tk.Label(top_bar, text="ION", fg="white", bg="#005c3c", font=("Arial", 20, "bold"))
    logo_lbl.pack(side="left", padx=20, pady=10)

    # ------------------------------------------------------------------
    # 3. Header bar with Back, title, edit icon
    # ------------------------------------------------------------------
    header = tk.Frame(root, bg="#f4f0f0", height=60)
    header.pack(fill="x", side="top")

    def on_back(event=None):
        if callable(back_callback):
            back_callback()

    back_lbl = tk.Label(header, text="\u2190", font=("Arial", 24), bg="#f4f0f0", cursor="hand2")
    back_lbl.pack(side="left", padx=15)
    back_lbl.bind("<Button-1>", on_back)

    tk.Label(header, text="Profile Settings", font=("Arial", 16, "bold"), bg="#f4f0f0").pack(side="left")

    edit_lbl = tk.Label(header, text="\u270f", font=("Arial", 18), bg="#f4f0f0", cursor="hand2")
    edit_lbl.pack(side="left", padx=10)

    # ------------------------------------------------------------------
    # 4. Profile info panel
    # ------------------------------------------------------------------
    info_container = tk.Frame(root, bg="#f4f0f0")
    info_container.pack(expand=True, fill="both")

    info_card = tk.Frame(info_container, bg="white", bd=1, relief="solid")
    info_card.pack(padx=30, pady=20, fill="both", expand=True)

    # Build a 2‑col grid of labels and values
    for r, (label, val) in enumerate(profile.items()):
        tk.Label(info_card, text=label, anchor="w", font=("Arial", 11, "bold"), bg="white") \
            .grid(row=r, column=0, sticky="w", padx=(15, 10), pady=8)
        tk.Label(info_card, text=val, anchor="w", font=("Arial", 11), bg="white") \
            .grid(row=r, column=1, sticky="w", padx=(0, 15), pady=8)

    # Vertical separator line between label/value columns
    sep = tk.Frame(info_card, bg="#d0d0d0", width=2)
    sep.place(relx=0.35, rely=0, relheight=1)  # 35% across the card

    # ------------------------------------------------------------------
    # 5. Large circular user icon on the right (overlay)
    # ------------------------------------------------------------------
    #circle_diam = 120  # px
    #circle = tk.Canvas(info_container, width=circle_diam, height=circle_diam, highlightthickness=0, bg="white")
    #circle.create_oval(2, 2, circle_diam-2, circle_diam-2, width=2, outline="#000000")
    #circle.create_text(circle_diam/2, circle_diam/2 - 15, text="\u25CF", font=("Arial", 26))  # head
    #circle.create_arc(20, circle_diam/2 - 5, circle_diam-20, circle_diam-20, start=0, extent=-180, style="arc", width=2)

    # Place it to the right, overlapping the info card a little (like screenshot)
    #circle.place(relx=1, x=-circle_diam-20, rely=0.05)


# ------------------------------------------------------------------------------
# Simple manual test when running this file directly
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Profile Settings – demo")
    root.geometry("800x600")
    show_profile_settings(root)
    root.mainloop()
