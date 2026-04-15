import sqlite3

# Connect to database
conn = sqlite3.connect("database/expenses.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    type TEXT,
    payment_method TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database and table created successfully!")