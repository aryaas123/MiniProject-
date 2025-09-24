import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
#Data collection
gold_dataset=pd.read_excel("miniproject/dataset.xlsx")
#clean and preprocess,identifying numeric columns
numeric_cols=['USD_INR','Open','Open','High','Low','Goldrate']
for c in numeric_cols:
    gold_dataset[c]=pd.to_numeric(gold_dataset[c].astype(str).str.replace(',',''),errors='coerce')
    # Step 3: Extract date features (assuming Date is already datetime64)
gold_dataset['Year'] = gold_dataset['Date'].dt.year
gold_dataset['Month'] = gold_dataset['Date'].dt.month
gold_dataset['Day'] = gold_dataset['Date'].dt.day
# Select only the required features
features = ['USD_INR', 'Year', 'Month', 'Day']
target = 'Goldrate'
X = gold_dataset[features]
y = gold_dataset[target]
# Assuming you have your features (X) and target (y)
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,         # 20% test, 80% train
    random_state=42        # Ensures same split every time
)
# Step 6: Train the Random Forest Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
# Step 7: Save model as .pkl file
with open("gold_price_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("✅ Model saved successfully as gold_price_model.pkl")

