import sqlite3
import pandas as pd

# Load data
conn = sqlite3.connect("database/expenses.db")
df = pd.read_sql("SELECT * FROM transactions", conn)
conn.close()

print("✅ Data Loaded Successfully")
print(df.head())

# Clean data
df['date'] = pd.to_datetime(df['date'])
df['category'] = df['category'].str.title()
df['type'] = df['type'].str.title()

df = df[df['amount'] > 0]

print("\n✅ Data Cleaned")

# Feature Engineering
df['month'] = df['date'].dt.month
df['month_name'] = df['date'].dt.month_name()
df['day'] = df['date'].dt.day
df['weekday'] = df['date'].dt.day_name()

df['is_expense'] = df['type'].apply(lambda x: 1 if x == "Expense" else 0)

print("\n✅ Features Created")
print(df.head())

# Save processed data
df.to_csv("data/processed_expenses.csv", index=False)

print("\n💾 Processed data saved!")