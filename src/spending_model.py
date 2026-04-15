import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import joblib

# Load data
df = pd.read_csv("data/processed_expenses.csv")

# Prepare monthly data
monthly = df.groupby('month')['amount'].sum().reset_index()

X = monthly[['month']]
y = monthly['amount']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
# Save model safely
import os

os.makedirs("src/models", exist_ok=True)
joblib.dump(model, "src/models/spending_model.pkl")

print("✅ Model trained and saved!")
# Predict next 3 months
future_months = np.array([[13], [14], [15]])
predictions = model.predict(future_months)

print("\n🔮 Future Predictions:")
for i, val in enumerate(predictions):
    print(f"Month {13+i}: ₹{val:.2f}")
