import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# ---------------------------------------------------
# PAGE CONFIG (Dark Mode Ready)
# ---------------------------------------------------
st.set_page_config(
    page_title="ICC Champions Trophy AI Dashboard",
    page_icon="🏏",
    layout="wide"
)

# Dark Theme Styling
st.markdown("""
<style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stApp {
        background-color: #0e1117;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.markdown(
    "<h1 style='text-align:center;color:white;'>🏆 ICC Champions Trophy AI Dashboard</h1>",
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
# AUTO TEAM LIST (20 Teams)
# ---------------------------------------------------
teams = sorted(list(set(data["Team 1"].unique()) | set(data["Team 2"].unique())))

# ---------------------------------------------------
# AUTO FLAG + LOGO SYSTEM
# ---------------------------------------------------
def get_flag(team):
    return f"https://flagcdn.com/w320/{team[:2].lower()}.png"

def get_logo(team):
    return f"https://raw.githubusercontent.com/iamshaunjp/cricket-logos/main/{team.lower().replace(' ','_')}.png"

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("🎛 Filters")

year_filter = st.sidebar.selectbox(
    "📅 Select Tournament Year",
    sorted(data["Year"].unique())
)

team_filter = st.sidebar.selectbox(
    "🏏 Select Team",
    teams
)

filtered_data = data[
    (data["Year"] == year_filter) &
    ((data["Team 1"] == team_filter) | (data["Team 2"] == team_filter))
]

# ---------------------------------------------------
# MATCHES PER YEAR GRAPH
# ---------------------------------------------------
st.subheader("📊 Matches Played Per Tournament")

matches_per_year = data["Year"].value_counts().sort_index()

fig1 = px.bar(
    x=matches_per_year.index,
    y=matches_per_year.values,
    title="Matches Per Year",
    text_auto=True
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# MOST SUCCESSFUL TEAMS
# ---------------------------------------------------
st.subheader("🏆 Most Successful Teams")

wins = data["Winner"].value_counts()

fig2 = px.bar(
    wins,
    x=wins.index,
    y=wins.values,
    title="Teams with Most Wins",
    text_auto=True
)
st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# 3D ANIMATION GRAPH
# ---------------------------------------------------
st.subheader("🌍 3D Wins + Margin Impact")

fig3 = px.scatter_3d(
    data,
    x="Year",
    y="Winner",
    z="Margin",
    color="Winner",
    height=650
)
st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# TEAM LOGOS + FLAGS (Auto)
# ---------------------------------------------------
st.subheader("🏳️ All Teams Flags + Logos")

cols = st.columns(5)

for i, team in enumerate(teams[:20]):
    with cols[i % 5]:
        st.image(get_flag(team), width=70)
        st.image(get_logo(team), width=70)
        st.caption(team)

st.write("---")

# ---------------------------------------------------
# MACHINE LEARNING WINNER PREDICTION
# ---------------------------------------------------
st.subheader("🤖 AI Winner Prediction Model")

ml_data = data[["Team 1", "Team 2", "Winner"]].dropna()

# Encode Teams
le1, le2, lew = LabelEncoder(), LabelEncoder(), LabelEncoder()

ml_data["Team1_enc"] = le1.fit_transform(ml_data["Team 1"])
ml_data["Team2_enc"] = le2.fit_transform(ml_data["Team 2"])
ml_data["Winner_enc"] = lew.fit_transform(ml_data["Winner"])

X = ml_data[["Team1_enc", "Team2_enc"]]
y = ml_data["Winner_enc"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model Training
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)

st.success(f"✅ Model Accuracy: {accuracy*100:.2f}%")

# Prediction Input
team1 = st.selectbox("Select Team 1", teams)
team2 = st.selectbox("Select Team 2", teams)

if st.button("Predict Winner 🏆"):
    t1 = le1.transform([team1])[0]
    t2 = le2.transform([team2])[0]

    pred = model.predict([[t1, t2]])
    winner = lew.inverse_transform(pred)[0]

    st.balloons()
    st.info(f"🏏 Predicted Winner: **{winner}**")

# ---------------------------------------------------
# SHOW FILTERED MATCHES TABLE
# ---------------------------------------------------
st.subheader(f"📌 Matches for {team_filter} in {year_filter}")

st.dataframe(filtered_data)

st.success("🚀 ICC Champions Trophy AI Dashboard Ready for GitHub + Deployment!")
