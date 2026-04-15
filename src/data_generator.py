import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("database/expenses.db")
cursor = conn.cursor()

categories = ['Food', 'Travel', 'Rent', 'Shopping', 'Bills', 'Entertainment']
payment_methods = ['UPI', 'Card', 'Cash', 'Net Banking']
types = ['Expense', 'Income']

def random_date():
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d")

for _ in range(500):
    cursor.execute("""
    INSERT INTO transactions (date, category, amount, type, payment_method)
    VALUES (?, ?, ?, ?, ?)
    """, (
        random_date(),
        random.choice(categories),
        round(random.uniform(100, 5000), 2),
        random.choices(types, weights=[80, 20])[0],
        random.choice(payment_methods)
    ))

conn.commit()
conn.close()

print("✅ Data inserted successfully!")