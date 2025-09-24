import streamlit as st
import pickle
import pandas as pd

st.title("💰 Gold Price Prediction💰")


# Load model
with open("gold_price_model.pkl", "rb") as f:
    model = pickle.load(f)

st.write("### Enter details for prediction")

# User input
usd_inr = st.number_input("USD_INR Value", min_value=50.0, max_value=100.0, value=82.0, step=0.1)
year = st.number_input("Year", min_value=2023, max_value=2026, value=2023, step=1)
month = st.number_input("Month", min_value=1, max_value=12, value=1, step=1)
day = st.number_input("Day", min_value=1, max_value=31, value=21, step=1)


# Predict gold price
if st.button("Predict Gold Rate"):
    prediction = model.predict([[usd_inr, year, month, day]])
    st.success(f"💡 Predicted Gold Rate: {prediction[0]:.2f}")
