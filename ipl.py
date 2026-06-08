import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    /* Dark cricket-themed background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Main title */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #f5a623, #e74c3c, #f5a623);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 20px 0 5px 0;
        letter-spacing: 2px;
    }
    
    .subtitle {
        text-align: center;
        color: #aaaaaa;
        font-size: 1rem;
        margin-bottom: 30px;
        letter-spacing: 1px;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e1e3f, #16213e);
        border: 1px solid #f5a623;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(245, 166, 35, 0.2);
    }

    div[data-testid="metric-container"] label {
        color: #f5a623 !important;
        font-weight: 600;
    }

    div[data-testid="metric-container"] div[data-testid="metric-value"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 800;
    }

    /* Section headers */
    h2, h3 {
        color: #f5a623 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d1a, #1a1a2e);
        border-right: 1px solid #f5a623;
    }
    
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Divider */
    hr {
        border-color: #f5a623 !important;
        opacity: 0.3;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# STEP 1: LOAD DATA
# ============================================
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
    return matches, deliveries

try:
    matches, deliveries = load_data()
except FileNotFoundError:
    st.error("❌ Could not find 'matches.csv' or 'deliveries.csv'. Make sure they are in the same folder as ipl.py")
    st.stop()

# ============================================
# STEP 2: SIDEBAR FILTER
# ============================================
st.sidebar.markdown("## 🏏 IPL Dashboard")
st.sidebar.markdown("---")

seasons = sorted(matches["season"].unique())
selected_season = st.sidebar.selectbox("📅 Select Season", ["All Seasons"] + [str(s) for s in seasons])

if selected_season != "All Seasons":
    filtered_matches = matches[matches["season"] == int(selected_season)]
else:
    filtered_matches = matches.copy()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Showing:** {len(filtered_matches)} matches")

# ============================================
# STEP 3: TITLE
# ============================================
st.markdown('<div class="main-title">🏏 IPL ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Indian Premier League • Data Analysis & Visualization</div>', unsafe_allow_html=True)
st.markdown("---")

# ============================================
# STEP 4: TOP METRICS
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏟️ Total Matches", len(filtered_matches))
with col2:
    total_teams = filtered_matches["team1"].nunique()
    st.metric("🤝 Total Teams", total_teams)
with col3:
    total_seasons = filtered_matches["season"].nunique()
    st.metric("📅 Seasons", total_seasons)
with col4:
    if "winner" in filtered_matches.columns:
        top_team = filtered_matches["winner"].value_counts().idxmax()
        st.metric("🏆 Most Wins", top_team)

st.markdown("---")

# ============================================
# STEP 5: TEAM WIN PERCENTAGE CHART
# ============================================
st.subheader("🏆 Team Win Count")

win_counts = filtered_matches["winner"].value_counts().reset_index()
win_counts.columns = ["Team", "Wins"]

fig1 = px.bar(
    win_counts,
    x="Team",
    y="Wins",
    color="Wins",
    color_continuous_scale=["#e74c3c", "#f5a623", "#f9ca24"],
    title="Number of Wins by Team"
)
fig1.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#ffffff",
    title_font_color="#f5a623",
    xaxis=dict(tickangle=-30, gridcolor="#333"),
    yaxis=dict(gridcolor="#333"),
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ============================================
# STEP 6: TOSS DECISION ANALYSIS
# ============================================
st.subheader("🎯 Toss Decision Analysis")

col_a, col_b = st.columns(2)

with col_a:
    toss = filtered_matches["toss_decision"].value_counts().reset_index()
    toss.columns = ["Decision", "Count"]

    fig2 = px.pie(
        toss,
        names="Decision",
        values="Count",
        title="Toss Decision: Bat vs Field",
        color_discrete_sequence=["#f5a623", "#e74c3c"]
    )
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff",
        title_font_color="#f5a623",
    )
    st.plotly_chart(fig2, use_container_width=True)

with col_b:
    # Toss winner = match winner?
    toss_win = filtered_matches[filtered_matches["toss_winner"] == filtered_matches["winner"]]
    toss_lose = filtered_matches[filtered_matches["toss_winner"] != filtered_matches["winner"]]

    toss_impact = pd.DataFrame({
        "Result": ["Won Toss & Match", "Won Toss, Lost Match"],
        "Count": [len(toss_win), len(toss_lose)]
    })

    fig3 = px.pie(
        toss_impact,
        names="Result",
        values="Count",
        title="Does Winning Toss Help Win Match?",
        color_discrete_sequence=["#27ae60", "#e74c3c"]
    )
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff",
        title_font_color="#f5a623",
    )
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ============================================
# STEP 7: TOP BATSMEN
# ============================================
st.subheader("🏏 Top 10 Run Scorers (All Time)")

# Use batsman column name (varies by dataset version)
batsman_col = "batsman" if "batsman" in deliveries.columns else "batter"
runs_col = "batsman_runs" if "batsman_runs" in deliveries.columns else "runs_off_bat"

top_batsmen = (
    deliveries.groupby(batsman_col)[runs_col]
    .sum()
    .reset_index()
    .sort_values(runs_col, ascending=False)
    .head(10)
)
top_batsmen.columns = ["Batsman", "Runs"]

fig4 = px.bar(
    top_batsmen,
    x="Runs",
    y="Batsman",
    orientation="h",
    color="Runs",
    color_continuous_scale=["#e74c3c", "#f5a623", "#f9ca24"],
    title="Top 10 Batsmen by Total Runs"
)
fig4.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#ffffff",
    title_font_color="#f5a623",
    yaxis=dict(categoryorder="total ascending", gridcolor="#333"),
    xaxis=dict(gridcolor="#333"),
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ============================================
# STEP 8: SEASON-WISE MATCH COUNT
# ============================================
st.subheader("📅 Matches Played Per Season")

season_matches = matches.groupby("season").size().reset_index(name="Matches")

fig5 = px.line(
    season_matches,
    x="season",
    y="Matches",
    markers=True,
    title="Number of Matches Per Season",
    color_discrete_sequence=["#f5a623"]
)
fig5.update_traces(line_width=3, marker_size=8)
fig5.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#ffffff",
    title_font_color="#f5a623",
    xaxis=dict(gridcolor="#333"),
    yaxis=dict(gridcolor="#333"),
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ============================================
# STEP 9: WIN BY RUNS vs WIN BY WICKETS
# ============================================
st.subheader("⚡ How Teams Win — By Runs vs By Wickets")

col_c, col_d = st.columns(2)

with col_c:
    runs_col = "win_by_runs" if "win_by_runs" in filtered_matches.columns else "WinByRuns"
    win_by_runs = filtered_matches[filtered_matches[runs_col] > 0][runs_col]
    fig6 = px.histogram(
        win_by_runs,
        nbins=20,
        title="Distribution of Win by Runs",
        color_discrete_sequence=["#e74c3c"]
    )
    fig6.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff",
        title_font_color="#f5a623",
        xaxis=dict(gridcolor="#333"),
        yaxis=dict(gridcolor="#333"),
    )
    st.plotly_chart(fig6, use_container_width=True)

with col_d:
    wickets_col = "win_by_wickets" if "win_by_wickets" in filtered_matches.columns else "WinByWickets"
    win_by_wickets = filtered_matches[filtered_matches[wickets_col] > 0][wickets_col]
    fig7 = px.histogram(
        win_by_wickets,
        nbins=10,
        title="Distribution of Win by Wickets",
        color_discrete_sequence=["#f5a623"]
    )
    fig7.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff",
        title_font_color="#f5a623",
        xaxis=dict(gridcolor="#333"),
        yaxis=dict(gridcolor="#333"),
    )
    st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div style="text-align:center; color:#666; font-size:0.85rem; padding:20px 0;">
    Built with ❤️ using Python • Pandas • Plotly • Streamlit<br>
    Data Science Project | Techno India University
</div>
""", unsafe_allow_html=True)
z\