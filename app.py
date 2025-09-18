import streamlit as st
import pandas as pd
import joblib

# Load model and expected columns
model = joblib.load("random_forest_model.pkl")
model_columns = joblib.load("model_columns.pkl")

# Page Config
st.set_page_config(page_title="Flight Price Predictor", layout="centered")

# Title
st.markdown("<h1 style='text-align:center;'>✈️ Flight Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Fill in the details to get an estimated flight price.</p>", unsafe_allow_html=True)
st.markdown("---")

# Grouped Inputs in 2 columns
col1, col2 = st.columns(2)

with col1:
    airline = st.selectbox("🛫 Airline", ['Air_India', 'GO_FIRST', 'Indigo', 'SpiceJet', 'Vistara'])
    source_city = st.selectbox("🌆 Source City", ['Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai'])
    departure_time = st.selectbox("🕒 Departure Time", ['Early_Morning', 'Evening', 'Late_Night', 'Morning', 'Night'])
    duration = st.number_input("⏱️ Flight Duration (hours)", min_value=0.0, value=2.0)

with col2:
    destination_city = st.selectbox("🏙️ Destination City", ['Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai'])
    arrival_time = st.selectbox("🕓 Arrival Time", ['Early_Morning', 'Evening', 'Late_Night', 'Morning', 'Night'])
    stops = st.selectbox("🛑 Number of Stops", ['zero', 'two_or_more'])
    days_left = st.slider("📅 Days Until Departure", 0, 60, 30)

travel_class = st.selectbox("🎟️ Class", ['Economy', 'Business'])

# Convert inputs to encoded format
input_dict = {
    'duration': duration,
    'days_left': days_left,
    f'airline_{airline}': 1,
    f'source_city_{source_city}': 1,
    f'destination_city_{destination_city}': 1,
    f'departure_time_{departure_time}': 1,
    f'arrival_time_{arrival_time}': 1,
    f'stops_{stops}': 1,
    'class_Economy': 1 if travel_class == 'Economy' else 0
}

# Fill missing columns with 0
input_data = {col: input_dict.get(col, 0) for col in model_columns}
input_df = pd.DataFrame([input_data])

# Predict Button
if st.button("🔍 Predict Price"):

    # Input validation
    if source_city == destination_city:
        st.warning("⚠️ Source and destination cities cannot be the same.")
    elif duration <= 0:
        st.warning("⚠️ Flight duration must be greater than 0.")
    else:
        try:
            predicted_price = model.predict(input_df)[0]
            st.success(f"🎯 Estimated Flight Price: ₹{int(predicted_price):,}")
        except Exception as e:
            st.error("⚠️ Error in prediction!")
            st.code(str(e))
