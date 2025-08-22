import sqlite3
from datetime import datetime   # ✅ for timestamp

#create connection
conn = sqlite3.connect("faculty_account.db")
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'faculty'))
)
""")
#sample account
cursor.execute("INSERT OR IGNORE INTO users (email, password, role) VALUES (?, ?, ?)",
               ("admin@nursing.com", "admin123", "admin"))
cursor.execute("INSERT OR IGNORE INTO users (email, password, role) VALUES (?, ?, ?)",
               ("faculty@nursing.com", "faculty123", "faculty"))

# Drop and recreate the equipment table
cursor.execute("DROP TABLE IF EXISTS equipment")
cursor.execute("""
CREATE TABLE equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    image_path TEXT,
    availability_status TEXT NOT NULL DEFAULT 'Available',
    category TEXT NOT NULL,
    usage_instruction TEXT NOT NULL
)
""")

# Drop and recreate the reservations table
cursor.execute("DROP TABLE IF EXISTS reservations")
cursor.execute("""
CREATE TABLE reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER NOT NULL,
    user_email TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    date_needed TEXT NOT NULL,
    purpose TEXT NOT NULL,
    duration TEXT NOT NULL,
    notes TEXT,
    status TEXT NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (equipment_id) REFERENCES equipment(id),
    FOREIGN KEY (user_email) REFERENCES users(email)
)
""") 

# Drop and recreate borrow table
cursor.execute("DROP TABLE IF EXISTS borrow")
cursor.execute("""
CREATE TABLE borrow (
    borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER NOT NULL,
    barcode TEXT NOT NULL,
    borrow_time TEXT NOT NULL,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id)
)
""")

# ✅ Drop and recreate transactions table properly
cursor.execute("DROP TABLE IF EXISTS transactions")
cursor.execute("""
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime TEXT NOT NULL,
    borrower_name TEXT NOT NULL,
    borrower_email TEXT NOT NULL,
    equipment_name TEXT NOT NULL,
    barcode TEXT NOT NULL,
    action TEXT NOT NULL CHECK(action IN ('Borrowed','Returned')),
    status TEXT NOT NULL,
    handled_by TEXT NOT NULL,
    remarks TEXT
)
""")

# Sample data
sample_equipment = [
    ("4801002457825", "Microscopes", "Capture and display specimen images.", "capstone/microscope.jpg", "Available", "Laboratory Equipment", "Place the slide and adjust the focus knobs."),
    ("4801002457824","Test tubes", "Small glass containers for mixing chemicals.", "capstone/testtube.jpeg", "Available", "Laboratory Equipment", "Mix or heat chemicals with care."),
    ("4801002457823","Medical apparatus", "Used to diagnose or treat.", "capstone/apparatus.jpeg", "Available", "Medical Equipment", "Follow standard procedures for use."),
    ("4801002457822","Funnels", "Pour liquids into small openings.", "capstone/funnel.jpeg", "Available", "Laboratory Equipment", "Pour liquids slowly to avoid spills."),
    ("4801002457821","Wire gauzes", "Heat-resistant mesh for experiments.", "capstone/gauze.jpeg", "Available", "Laboratory Equipment", "Place under beakers when heating."),
    ("6970122841710","Test tube holders", "Hold test tubes over flames.", "capstone/holder.jpeg", "Available", "Laboratory Equipment", "Grip test tubes firmly over heat.")
]

for barcode, name, desc, img, status, cat, usage in sample_equipment:
    cursor.execute("""
        INSERT INTO equipment (barcode, name, description, image_path, availability_status, category, usage_instruction)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (barcode, name, desc, img, status, cat, usage))

# ✅ Example: insert a transaction using email as borrower_name
borrower_email = "faculty@nursing.com"
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
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    borrower_email,   # borrower_name = email
    borrower_email,   # borrower_email
    "Microscopes",    # example equipment
    "4801002457825",  # example barcode
    "Borrowed",
    "Ongoing",
    "Custodian 1",
    
    None
))

conn.commit()
conn.close()
print("Database created, equipment inserted, and sample transaction added.")
