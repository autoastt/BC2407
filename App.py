import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏨",
    layout="wide",
)

dashboard = st.Page("pages/0_Dashboard.py", title="Dashboard", icon="📍")
eda = st.Page("pages/1_EDA.py", title="Exploratory Data Analysis", icon="📊")
models = st.Page("pages/2_Models.py", title="Models", icon="🤖")
pg = st.navigation([dashboard, eda, models])
pg.run()