import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

st.markdown(f"# BC2407 Project Dashboard")

df = pd.read_csv('data/hotel_cleaned.csv')
df['is_canceled'] = df['is_canceled'].map({0: "Didn't Cancel", 1: 'Cancel'})
numerical = ['lead_time', 'stays_in_weekend_nights', 'stays_in_week_nights', 'adults', 'children', 'babies', 'previous_cancellations', 'previous_bookings_not_canceled', 'booking_changes', 'days_in_waiting_list', 'adr', 'required_car_parking_spaces', 'total_of_special_requests']
categorical = ['hotel', 'arrival_date_year', 'arrival_date_month', 'arrival_date_week_number', 'meal', 'country', 'market_segment', 'distribution_channel', 'is_repeated_guest', 'reserved_room_type', 'assigned_room_type', 'deposit_type', 'customer_type']

st.markdown('## Univariate Analysis')
color = st.selectbox('Display Cancellation?', ['Yes', 'No'])
dcolor = ['#94e2d5', '#f38ba8']
mauve = ['#cba6f7']
catppuccin_mocha = [
    "#f38ba8", 
    "#fab387", 
    "#f9e2af", 
    "#a6e3a1", 
    "#94e2d5", 
    "#89b4fa", 
    "#b4befe", 
    "#cba6f7", 
    "#f5c2e7", 
    "#eba0ac", 
]

col1, col2 = st.columns(2)
with col1:
    var1 = st.selectbox("Please select first column", df.columns, index=None, key='s1')
    if (var1):
        if color == 'No':
            fig1 = px.histogram(df, x=var1, color_discrete_sequence=mauve)
        else:
            fig1 = px.histogram(df, x=var1, color='is_canceled', color_discrete_sequence=dcolor) 
        st.plotly_chart(fig1, key='p1')

with col2:
    var2 = st.selectbox("Please select second column", df.columns, index=None, key='s2')
    if (var2):
        if color == 'No':
            fig2 = px.histogram(df, x=var2, color_discrete_sequence=mauve) 
        else:
            fig2 = px.histogram(df, x=var2, color='is_canceled', color_discrete_sequence=dcolor) 
        st.plotly_chart(fig2, key='p2')

st.markdown('## Bivariate Analysis')
if (var1 and var2):
    if (var1 in numerical and var2 in numerical):
        if color == 'No':
            cmp = px.scatter(df, x=var1, y=var2, color_discrete_sequence=mauve)
        else:
            cmp = px.scatter(df, x=var1, y=var2, color='is_canceled', color_discrete_sequence=dcolor)
        st.plotly_chart(cmp)
    elif (var1 in numerical and var2 in categorical):
        if color == 'No':
            cmp = px.box(df, x=var2, y=var1, color_discrete_sequence=mauve)
        else:    
            cmp = px.box(df, x=var2, y=var1, color='is_canceled', color_discrete_sequence=dcolor)
        st.plotly_chart(cmp)
    elif (var1 in categorical and var2 in numerical):
        if color == 'No':
            cmp = px.box(df, x=var1, y=var2, color_discrete_sequence=mauve)
        else:    
            cmp = px.box(df, x=var1, y=var2, color='is_canceled', color_discrete_sequence=dcolor)
        st.plotly_chart(cmp)
    else:
        cmp = px.histogram(df, x=var1, color=var2, barmode='group', color_discrete_sequence=catppuccin_mocha)
        st.plotly_chart(cmp)
else:
    st.status('Please Select 2 Columns')


st.markdown("## Detailed Cleaned Data")
df