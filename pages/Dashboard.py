import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

st.markdown(f"# BC2407 Project Dashboard")

df = pd.read_csv('data/hotel_cleaned.csv')
df['is_canceled_tmp'] = df['is_canceled']
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


st.markdown("## Important Findings")

# important finding 1
st.markdown("### Cancellation Rate by Lead Time and Year")
bins = [0, 30, 60, 90, 180, 365, df['lead_time'].max()]
labels = ['0–30', '31–60', '61–90', '91–180', '181–365', '366+']
df['lead_time_cat'] = pd.cut(df['lead_time'], bins=bins, labels=labels, right=True)

grouped = df.groupby(['lead_time_cat', 'arrival_date_year'])['is_canceled_tmp'].mean().reset_index()
grouped.rename(columns={'is_canceled_tmp': 'cancellation_rate'}, inplace=True)

if1 = px.line(grouped, 
    x='lead_time_cat', 
    y='cancellation_rate', 
    color='arrival_date_year', 
    markers=True, 
    color_discrete_sequence=[catppuccin_mocha[0], catppuccin_mocha[3], catppuccin_mocha[5]])
if1.update_layout(
    xaxis_title="Lead Time",
    yaxis_title="Cancellation Rate",
    legend_title_text='Year'
)
st.plotly_chart(if1)
st.markdown("Across all the years analysed, there is a consistent trend: The longer the lead time, the higher the cancellation rate.")
st.markdown("Booking made within the 0-30 day before check in showcase the lowest cancellation rates, while those made over a year in advance have the highest.")
st.markdown("This indicates that longer lead times may indicate lower commitment from the customers, possibly due to low-risk bookings made under more flexible cancellation policies.")

# important finding 2
st.markdown("### Market Segments: Who Cancels & When do they Book?")
df_bubble = df.groupby('market_segment').agg(
    avg_lead_time=('lead_time', 'mean'),
    cancellation_rate=('is_canceled_tmp', 'mean'),
    booking_count=('is_canceled_tmp', 'count')
).reset_index()
if2 = px.scatter(df_bubble,
    x='avg_lead_time',
    y='cancellation_rate',
    size='booking_count',
    color='cancellation_rate',
    text='market_segment',
    color_continuous_scale='Reds',
    size_max=60)
if2.update_layout(
    xaxis_title="Average Lead Time (days)",
    yaxis_title="Cancellation Rate",
    coloraxis_colorbar=dict(title="Cancellation Rate")
)
if2.update_traces(textposition='middle center')
st.plotly_chart(if2)
st.markdown("Group bookings are usually made well in advance and cancel more often. This could be due to high uncertainty because of shifting group plans, tentative reservations, or reliance on event confirmations.")
st.markdown("Online TA bookings also see high cancellation rates, despite lower lead times, likely because they are easy to cancel and often made on flexible terms determined by the travel agent.")
st.markdown("Corporate, Direct, and Complimentary bookings tend to be more reliable. These guests book closer to the stay, and their plans are often more fixed, like for business trips or hotel-assigned stays.")

st.markdown("### Imbalanced Cancellation")
st.plotly_chart(px.histogram(df, x='is_canceled', color='is_canceled', color_discrete_sequence=[catppuccin_mocha[4], catppuccin_mocha[0]]))
st.markdown("As our target variable has an imbalanced distribution that could lead to model bias, we will apply the Synthetic Minority Over-sampling Technique (SMOTE), which creates synthetic data points for the minority class with the same features' distribution of the original dataset. This helps the model to learn from a more balanced dataset.")
st.markdown("## Detailed Cleaned Data")
df