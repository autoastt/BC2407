import streamlit as st
import numpy as np
import pandas as pd
import joblib

st.markdown("## Hotel Booking Cancellation Prediction")

# Load trained models
rf = joblib.load("models/RandomForest.joblib")
xgb = joblib.load("models/XGBoost.joblib")
mlp = joblib.load("models/MLP.joblib")
log = joblib.load("models/Logistic.joblib")

# Layout: User input fields
col1, col2, col3 = st.columns(3)

with col1:
    arrival_date_year = st.selectbox("Arrival Year", [2015, 2016, 2017], index=0)
    arrival_date_month = st.selectbox("Arrival Month", 
                                      ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], 
                                      index=6)
    arrival_date_week_number = st.number_input("Arrival Week Number", min_value=1, max_value=52, value=27)
    arrival_date_day_of_month = st.number_input("Arrival Day of Month", min_value=1, max_value=31, value=2)
    stays_in_weekend_nights = st.number_input("Weekend Nights", min_value=0, value=1)
    stays_in_week_nights = st.number_input("Week Nights", min_value=0, value=3)
    adults = st.number_input("Number of Adults", min_value=1, value=3)
    children = st.number_input("Number of Children", min_value=0, value=0)
    babies = st.number_input("Number of Babies", min_value=0, value=0)

with col2:    
    lead_time = st.number_input("Lead Time (days before arrival)", min_value=0, value=45)
    is_repeated_guest = st.selectbox("Is Repeated Guest?", ["No", "Yes"], index=0)
    previous_cancellations = st.number_input("Previous Cancellations", min_value=0, value=0)
    previous_bookings_not_canceled = st.number_input("Previous Bookings Not Canceled", min_value=0, value=0)
    booking_changes = st.number_input("Booking Changes", min_value=0, value=0)
    days_in_waiting_list = st.number_input("Days in Waiting List", min_value=0, value=0)
    adr = st.number_input("Average Daily Rate", min_value=0.0, value=108.8)
    required_car_parking_spaces = st.number_input("Car Parking Spaces", min_value=0, value=0)
    total_of_special_requests = st.number_input("Special Requests", min_value=0, value=1)

with col3:
    hotel = st.selectbox("Hotel Type", ["Resort Hotel", "City Hotel"], index=0)
    meal = st.selectbox("Meal Type", ["BB", "FB", "HB", "SC"], index=0)
    country = st.selectbox("Country", ['PRT', 'GBR', 'USA', 'ESP', 'IRL', 'FRA', 'NOR', 'POL', 'DEU', 'BEL', 'CHE',
                                    'CN', 'ITA', 'NLD', 'RUS', 'SWE', 'BRA', 'CHN', 'AUT', 'ISR', 'Other'], index=0)
    market_segment = st.selectbox("Market Segment", ["Direct", "Corporate", "Online TA", "Offline TA/TO", 
                                                    "Complementary", "Groups", "Aviation"], index=2)
    distribution_channel = st.selectbox("Distribution Channel", ["Direct", "Corporate", "TA/TO", "GDS"], index=2)
    reserved_room_type = st.selectbox("Reserved Room Type", ['C', 'A', 'D', 'E', 'G', 'F', 'H', 'L', 'B', 'P'], index=2)
    assigned_room_type = st.selectbox("Assigned Room Type", ['C', 'A', 'D', 'E', 'G', 'F', 'I', 'B', 'H', 'L', 'K', 'P'], index=2)
    deposit_type = st.selectbox("Deposit Type", ["No Deposit", "Refundable", "Non Refund"], index=0)
    customer_type = st.selectbox("Customer Type", ["Transient", "Contract", "Transient-Party", "Group"], index=0)

# Select Model
model_name = st.selectbox("Select Model", ["Random Forest", "XGBoost", "Multi-layer Perceptron", "Logistic Regression"], index=0)


data = {
    'hotel': [hotel],
    'lead_time': [lead_time],
    'arrival_date_year': [arrival_date_year],
    'arrival_date_month': [arrival_date_month],
    'arrival_date_week_number': [arrival_date_week_number],
    'arrival_date_day_of_month': [arrival_date_day_of_month],
    'stays_in_weekend_nights': [stays_in_weekend_nights],
    'stays_in_week_nights': [stays_in_week_nights],
    'adults': [adults],
    'children': [children],
    'babies': [babies],
    'meal': [meal],
    'country': [country],
    'market_segment': [market_segment],
    'distribution_channel': [distribution_channel],
    'is_repeated_guest': [1 if is_repeated_guest == "Yes" else 0],
    'previous_cancellations': [previous_cancellations],
    'previous_bookings_not_canceled': [previous_bookings_not_canceled],
    'reserved_room_type': [reserved_room_type],
    'assigned_room_type': [assigned_room_type],
    'booking_changes': [booking_changes],
    'deposit_type': [deposit_type],
    'days_in_waiting_list': [days_in_waiting_list],
    'customer_type': [customer_type],
    'adr': [adr],
    'required_car_parking_spaces': [required_car_parking_spaces],
    'total_of_special_requests': [total_of_special_requests]
}

# Convert to DataFrame
df = pd.DataFrame(data)
one_hot_cols = ['country', 'hotel', 'arrival_date_month', 'meal', 'market_segment', 
                'distribution_channel', 'reserved_room_type', 'assigned_room_type', 
                'deposit_type', 'customer_type']
df = pd.get_dummies(df, columns=one_hot_cols, drop_first=True)
X_train = pd.read_csv('./data/train-test/train.csv').drop('is_canceled', axis=1)
X_train, df = X_train.align(df, join='left', axis=1, fill_value=0)

# Load selected model and predict
model_dict = {
    "Random Forest": rf, 
    "XGBoost": xgb, 
    "Multi-layer Perceptron": mlp, 
    "Logistic Regression": log
    }
selected_model = model_dict[model_name]

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

if selected_model != log: 
    result = selected_model.predict(df)
else:
    result = selected_model.predict(df_scaled)

# Display results
if result[0] == 1:
    st.html("<h3 style='text-align: center; background-color: rgba(210, 15, 57, 0.2); border-radius: 0.5rem; font-size: 28px; padding-top: 8px; padding-bottom: 8px;'> ‼️ This booking is likely to be canceled.</h3>")
else:
    st.html("<h3 style='text-align: center; background-color: rgba(64, 160, 43, 0.2); border-radius: 0.5rem; font-size: 28px; padding-top: 8px; padding-bottom: 8px;'> ✅ This booking is not likely to be canceled.</h3>")

st.markdown("### Model's Performace")
if selected_model == rf:
    st.markdown("#### :blue[Accuracy: 0.884]")
    st.markdown("#### :green[Confusion Matrix]")
    st.image("results/rf_cm.png")
    st.markdown("#### :red[Top Features]")
    st.image("results/rf_im.png")
elif selected_model == xgb:
    st.markdown("#### :blue[Accuracy: 0.877]")
    st.markdown("#### :green[Confusion Matrix]")
    st.image("results/xgb_cm.png")
    st.markdown("#### :red[Top Features]")
    st.image("results/xgb_im.png")
elif selected_model == mlp:
    st.markdown("#### :blue[Accuracy: 0.841]")
    st.markdown("#### :green[Confusion Matrix]")
    st.image("results/mlp_cm.png")
else:
    st.markdown("#### :blue[Accuracy: 0.813]")
    st.markdown("#### :green[Confusion Matrix]")
    st.image("results/log_cm.png")