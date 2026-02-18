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
# DARK PROFESSIONAL THEME
# =====================================================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
h1,h2,h3,h4 {
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
# LOAD DATA (NO ERROR VERSION)
# =====================================================
@st.cache_data
def load_data():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        "all_champions_trophy_matches_results.csv"
    )

    if not os.path.exists(file_path):
        st.error("❌ CSV File Missing! Upload it inside data folder.")
        st.stop()

    df = pd.read_csv(file_path)
    df["Year"] = pd.to_datetime(df["Match Date"]).dt.year

    # Toss Split
    df[['Toss_Winner', 'Toss_Decision']] = df['Toss'].str.split(',', expand=True)
    df['Toss_Decision'] = df['Toss_Decision'].str.extract(r'(bat|field)')

    return df

data = load_data()

# =====================================================
# TEAM LIST AUTO
# =====================================================
teams = sorted(list(set(data["Team 1"]) | set(data["Team 2"])))

# =====================================================
# LOGO + FLAG AUTO SYSTEM
# =====================================================
def flag(team):
    return f"https://flagcdn.com/w320/{team[:2].lower()}.png"

def logo(team):
    return f"https://raw.githubusercontent.com/ajaykumar0999/cricket-team-logos/main/logos/{team.lower().replace(' ','_')}.png"

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

# Filter Data
filtered = data[
    (data["Year"] == year_filter) &
    ((data["Team 1"] == team_filter) | (data["Team 2"] == team_filter))
]

# =====================================================
# KPI SECTION
# =====================================================
st.subheader("📌 Tournament Quick Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Matches", len(filtered))
col2.metric("Total Wins", len(filtered[filtered["Winner"] == team_filter]))
col3.metric("Total Losses", len(filtered) - len(filtered[filtered["Winner"] == team_filter]))

st.write("---")

# =====================================================
# MATCHES PER YEAR (3D BAR)
# =====================================================
st.subheader("📊 Matches Played Per Tournament")

matches_per_year = data["Year"].value_counts().sort_index()

fig1 = px.bar(
    x=matches_per_year.index,
    y=matches_per_year.values,
    title="Matches Per Tournament Year",
    text_auto=True
)
st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# WIN + LOSS ANALYSIS
# =====================================================
st.subheader("🏆 Win vs Loss Analysis")

win_loss = filtered["Winner"].value_counts()

fig2 = px.pie(
    names=win_loss.index,
    values=win_loss.values,
    title="Winning Distribution"
)
st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# 3D TEAM PERFORMANCE ANIMATION
# =====================================================
st.subheader("🌍 3D Match Margin Impact Animation")

fig3 = px.scatter_3d(
    data,
    x="Year",
    y="Winner",
    z="Margin",
    color="Winner",
    title="3D Animated Wins + Margin Impact",
    height=700
)
st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# TOSS BAT vs FIELD IMPACT
# =====================================================
st.subheader("🎲 Toss Decision Impact (Bat vs Field)")

toss_fig = px.histogram(
    data,
    x="Toss_Decision",
    color="Winner",
    barmode="group",
    title="Bat or Field After Toss - Winning Impact"
)
st.plotly_chart(toss_fig, use_container_width=True)

# =====================================================
# GROUNDS ANALYSIS + STADIUM GALLERY
# =====================================================
st.subheader("🏟 Top Grounds + Stadium Gallery")

top_grounds = data["Ground"].value_counts().head(6)

fig4 = px.bar(
    x=top_grounds.index,
    y=top_grounds.values,
    title="Top Cricket Grounds (Most Matches Hosted)",
    text_auto=True
)
st.plotly_chart(fig4, use_container_width=True)

# Stadium Images (Auto)
st.markdown("### 🌍 Famous Grounds Preview")

ground_images = {
    "Lahore": "https://upload.wikimedia.org/wikipedia/commons/6/6c/Gaddafi_Stadium.jpg",
    "London": "https://upload.wikimedia.org/wikipedia/commons/1/1e/Lords_Cricket_Ground.jpg",
    "Dubai": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Dubai_International_Cricket_Stadium.jpg",
    "Cardiff": "https://upload.wikimedia.org/wikipedia/commons/3/36/Sophia_Gardens_Cardiff.jpg",
    "Johannesburg": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Wanderers_Stadium.jpg",
    "Mumbai": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Wankhede_Stadium.jpg"
}

cols = st.columns(3)
i = 0
for g, img in ground_images.items():
    with cols[i % 3]:
        st.image(img, caption=g, use_column_width=True)
    i += 1

# =====================================================
# TEAM LOGOS + FLAGS DISPLAY
# =====================================================
st.subheader("🏳️ All Teams Flags + Logos (Auto)")

cols = st.columns(5)

for i, t in enumerate(teams[:20]):
    with cols[i % 5]:
        st.image(flag(t), width=70)
        st.image(logo(t), width=70)
        st.caption(t)

# =====================================================
# FINAL TABLE
# =====================================================
st.subheader(f"📅 Match Records for {team_filter} ({year_filter})")
st.dataframe(filtered)

st.success("✅ Professional ICC Champions Trophy Dashboard Ready for GitHub + Streamlit Cloud 🚀")
