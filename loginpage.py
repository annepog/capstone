# main.py
import tkinter as tk
from PIL import Image, ImageTk
from loginform import show_login_form

#window, wndw title, size, color
root = tk.Tk()
root.title("Institute of Nursing Laboratory Equipment Management System")
root.geometry("1920x1080")
root.configure(bg="#fbb3bb")

#frame para center lhat
main_frame = tk.Frame(root, bg="#fbb3bb")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

#logo
logo_image = Image.open("ion_logo.png").resize((400, 350))
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(main_frame, image=logo_photo, bg="#fbb3bb")
logo_label.pack(pady=(0, 10), padx=(20, 50))

#text below logo
tk.Label(main_frame, text="Institute of Nursing", font=("Helvetica", 16, "bold"), bg="#fbb3bb").pack()
tk.Label(main_frame, text="Laboratory Equipment Management System", font=("Helvetica", 20, "bold"), bg="#fbb3bb").pack(pady=(0, 20))

#buton
login_button = tk.Button(
    main_frame,
    text="LOGIN",
    font=("Helvetica", 14, "bold"),
    bg="#006544",
    fg="white",
    padx=30,
    pady=10,
    relief="flat",
    command=lambda: show_login_form(root)
)
login_button.pack()

root.mainloop()
