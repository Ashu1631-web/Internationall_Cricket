import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="ICC Champions Trophy Pro Dashboard",
    page_icon="🏏",
    layout="wide"
)

# =====================================================
# DARK MODE UI
# =====================================================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
h1,h2,h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.markdown(
    "<h1 style='text-align:center;'>🏆 ICC Champions Trophy Professional Dashboard</h1>",
    unsafe_allow_html=True
)
st.write("---")

# =====================================================
# LOAD DATA SAFELY
# =====================================================
@st.cache_data
def load_data():

    file_path = "all_champions_trophy_matches_results.csv"

    if os.path.exists("data/all_champions_trophy_matches_results.csv"):
        file_path = "data/all_champions_trophy_matches_results.csv"

    if not os.path.exists(file_path):
        st.error("❌ CSV file missing! Upload it in repo root OR inside data folder.")
        st.stop()

    df = pd.read_csv(file_path)

    # Year Column
    df["Year"] = pd.to_datetime(df["Match Date"]).dt.year

    # Toss Split
    df[['Toss_Winner', 'Toss_Decision']] = df['Toss'].str.split(',', expand=True)
    df['Toss_Decision'] = df['Toss_Decision'].str.extract(r'(bat|field)')

    return df


data = load_data()

# =====================================================
# TEAMS LIST
# =====================================================
teams = sorted(list(set(data["Team1"]) | set(data["Team2"])))

# =====================================================
# FLAG AUTO SYSTEM
# =====================================================
def flag(team):
    return f"https://flagcdn.com/w320/{team[:2].lower()}.png"


# =====================================================
# SIDEBAR FILTERS
# =====================================================
st.sidebar.title("🎛 Dashboard Filters")

year_filter = st.sidebar.selectbox(
    "📅 Select Year",
    sorted(data["Year"].unique())
)

team_filter = st.sidebar.selectbox(
    "🏏 Select Team",
    teams
)

filtered = data[
    (data["Year"] == year_filter) &
    ((data["Team1"] == team_filter) | (data["Team2"] == team_filter))
]

# =====================================================
# KPI SUMMARY
# =====================================================
st.subheader("📌 Team Performance Summary")

wins = len(filtered[filtered["Winner"] == team_filter])
losses = len(filtered) - wins

col1, col2, col3 = st.columns(3)
col1.metric("Total Matches", len(filtered))
col2.metric("Wins 🏆", wins)
col3.metric("Losses ❌", losses)

st.write("---")

# =====================================================
# MATCHES PER YEAR
# =====================================================
st.subheader("📊 Matches Played Per Tournament")

matches_per_year = data["Year"].value_counts().sort_index()

fig1 = px.bar(
    x=matches_per_year.index,
    y=matches_per_year.values,
    title="Matches Played Each Year",
    text_auto=True
)
st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# MOST SUCCESSFUL TEAMS
# =====================================================
st.subheader("🏆 Most Successful Teams")

team_wins = data["Winner"].value_counts()

fig2 = px.bar(
    team_wins,
    x=team_wins.index,
    y=team_wins.values,
    title="Teams with Most Wins",
    text_auto=True
)
st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# 3D WIN MARGIN ANIMATION
# =====================================================
st.subheader("🌍 3D Match Margin Impact")

fig3 = px.scatter_3d(
    data,
    x="Year",
    y="Winner",
    z="Margin",
    color="Winner",
    title="3D Wins + Margin Impact",
    height=650
)
st.plotly_chart(fig3, use_container_width=True)

# ===================================
