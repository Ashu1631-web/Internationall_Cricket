import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="ICC Champions Trophy Dashboard",
    page_icon="🏏",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.markdown(
    "<h1 style='text-align:center;'>🏆 ICC Champions Trophy Analysis Dashboard</h1>",
    unsafe_allow_html=True
)

st.write("---")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/all_champions_trophy_matches_results.csv")
    df["Year"] = pd.to_datetime(df["Match Date"]).dt.year
    return df

data = load_data()

# ---------------------------------------------------
# TEAM LOGOS + FLAGS (REAL LINKS)
# ---------------------------------------------------
team_assets = {
    "India": {
        "flag": "https://flagcdn.com/w320/in.png",
        "logo": "https://upload.wikimedia.org/wikipedia/en/4/4b/India_national_cricket_team_logo.png"
    },
    "Pakistan": {
        "flag": "https://flagcdn.com/w320/pk.png",
        "logo": "https://upload.wikimedia.org/wikipedia/en/3/36/Pakistan_cricket_team_logo.png"
    },
    "Australia": {
        "flag": "https://flagcdn.com/w320/au.png",
        "logo": "https://upload.wikimedia.org/wikipedia/en/3/3f/Australia_national_cricket_team_logo.png"
    },
    "England": {
        "flag": "https://flagcdn.com/w320/gb.png",
        "log
