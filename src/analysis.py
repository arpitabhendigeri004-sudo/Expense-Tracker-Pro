import pandas as pd
import matplotlib.pyplot as plt

# Load processed data
df = pd.read_csv("data/processed_expenses.csv")

print("✅ Data Loaded for Analysis")

# -----------------------------
# 1. CATEGORY ANALYSIS
# -----------------------------
category_spending = df.groupby('category')['amount'].sum().sort_values(ascending=False)

print("\n📊 Category-wise Spending:")
print(category_spending)

# Bar Chart
plt.figure(figsize=(10,5))
category_spending.plot(kind='bar')
plt.title("Category-wise Spending")
plt.xlabel("Category")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.savefig("outputs/category_spending.png")
plt.show()

# -----------------------------
# 2. MONTHLY TREND
# -----------------------------
monthly_spending = df.groupby('month')['amount'].sum()

plt.figure(figsize=(10,5))
monthly_spending.plot(marker='o')
plt.title("Monthly Spending Trend")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.savefig("outputs/monthly_trend.png")
plt.show()

# -----------------------------
# 3. OVESPENDING DETECTION
# -----------------------------
threshold = df['amount'].mean() * 1.5

high_spending = df[df['amount'] > threshold]

print("\n🚨 High Spending Transactions:")
print(high_spending.head())

# -----------------------------
# 4. SMART INSIGHTS
# -----------------------------
top_category = category_spending.idxmax()
total_spent = df['amount'].sum()
avg_spent = df['amount'].mean()

print("\n💡 INSIGHTS:")
print(f"👉 Highest spending category: {top_category}")
print(f"👉 Total spending: ₹{total_spent:.2f}")
print(f"👉 Average transaction: ₹{avg_spent:.2f}")

if avg_spent > 3000:
    print("⚠️ You are spending heavily!")
else:
    print("✅ Spending is under control")
    