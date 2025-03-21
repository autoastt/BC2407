import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

df = pd.read_csv("data/hotel_booking.csv")
clean_df = pd.read_csv("data/hotel_cleaned.csv")

st.markdown("### Hotel Booking Data")
st.dataframe(df)

st.markdown("### Cleaned Data")
st.dataframe(clean_df)