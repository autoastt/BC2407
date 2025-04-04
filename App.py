import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏨",
    layout="wide",
)

dashboard = st.Page("pages/Dashboard.py", title="Dashboard", icon="📍")
models = st.Page("pages/Models.py", title="Models", icon="🤖")
pg = st.navigation({"Navigation": [dashboard, models]})
pg.run()