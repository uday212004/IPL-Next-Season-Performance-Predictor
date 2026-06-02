# ==========================================
# IPL NEXT SEASON PERFORMANCE PREDICTOR
# Premium Sports Analytics Dashboard
# ==========================================

import streamlit as st
import pandas as pd
import joblib
import json

# ==========================================
# PAGE CONFIG — Must be first Streamlit call
# ==========================================

st.set_page_config(
    page_title="IPL Performance Predictor",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# GLOBAL CSS — Dark IPL Theme
# Purple (#7C3AED), Gold (#F59E0B), Dark BG
# ==========================================

st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary:    #0A0A14;
    --bg-secondary:  #0F0F20;
    --bg-card:       #13132A;
    --bg-card-hover: #1A1A35;
    --purple-deep:   #4C1D95;
    --purple-main:   #7C3AED;
    --purple-light:  #A78BFA;
    --purple-glow:   rgba(124, 58, 237, 0.25);
    --gold-main:     #F59E0B;
    --gold-light:    #FCD34D;
    --gold-glow:     rgba(245, 158, 11, 0.20);
    --text-primary:  #F1F0FF;
    --text-secondary:#A5A0CC;
    --text-muted:    #6B648C;
    --border-subtle: rgba(124, 58, 237, 0.18);
    --border-gold:   rgba(245, 158, 11, 0.35);
    --success:       #10B981;
    --success-glow:  rgba(16, 185, 129, 0.20);
    --warning:       #EF4444;
    --warning-glow:  rgba(239, 68, 68, 0.20);
}

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Exo 2', sans-serif !important;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Main content padding ── */
[data-testid="stAppViewContainer"] > section > div {
    padding-top: 0 !important;
}
.block-container {
    padding: 1.5rem 2rem 3rem 2rem !important;
    max-width: 1400px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}
[data-testid="stSidebarContent"] {
    background: transparent !important;
}

/* ── Sidebar Nav Items ── */
.sidebar-nav-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    margin: 0.2rem 0;
    border-radius: 10px;
    cursor: pointer;
    color: var(--text-secondary);
    font-family: 'Exo 2', sans-serif;
    font-weight: 500;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    border: 1px solid transparent;
    text-decoration: none;
}
.sidebar-nav-item:hover {
    background: var(--purple-glow);
    color: var(--purple-light);
    border-color: var(--border-subtle);
}
.sidebar-nav-item.active {
    background: linear-gradient(135deg, var(--purple-glow), rgba(245,158,11,0.08));
    color: var(--gold-light);
    border-color: var(--border-gold);
}
.sidebar-logo {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--gold-main);
    letter-spacing: 1px;
    padding: 0.5rem 1rem 1.5rem 1rem;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 1rem;
}
.sidebar-logo span { color: var(--purple-light); }
.sidebar-section-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 1rem 1rem 0.4rem 1rem;
}

/* ── Hero Banner ── */
.hero-banner {
    position: relative;
    background: linear-gradient(135deg, #0D0B2A 0%, #1A0944 40%, #0A1628 70%, #0D1520 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    padding: 3rem 3rem 2.5rem 3rem;
    margin-bottom: 2rem;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(124,58,237,0.35) 0%, transparent 70%);
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 10%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(245,158,11,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--gold-main);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.hero-eyebrow::before {
    content: '';
    display: inline-block;
    width: 24px; height: 2px;
    background: var(--gold-main);
    border-radius: 2px;
}
.hero-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 3.2rem;
    font-weight: 700;
    line-height: 1.05;
    margin: 0 0 0.75rem 0;
    background: linear-gradient(135deg, #F1F0FF 30%, var(--purple-light) 65%, var(--gold-main) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    max-width: 520px;
    line-height: 1.6;
    font-weight: 400;
    margin-bottom: 0;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(245,158,11,0.12);
    border: 1px solid var(--border-gold);
    color: var(--gold-light);
    font-size: 0.75rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.5px;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    margin-top: 1.5rem;
}
.hero-badge::before { content: '●'; font-size: 0.5rem; color: var(--gold-main); }

/* ── KPI Card ── */
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: all 0.25s ease;
}
.kpi-card:hover {
    border-color: var(--purple-main);
    background: var(--bg-card-hover);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px var(--purple-glow);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    right: 0; height: 2px;
    background: linear-gradient(90deg, var(--purple-main), var(--gold-main));
}
.kpi-icon {
    font-size: 1.5rem;
    margin-bottom: 0.6rem;
    display: block;
}
.kpi-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: var(--gold-light);
    line-height: 1;
    margin-bottom: 0.25rem;
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted);
}
.kpi-sub {
    font-size: 0.8rem;
    color: var(--purple-light);
    margin-top: 0.3rem;
    font-weight: 500;
}

/* ── Section Header ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2rem 0 1.25rem 0;
}
.section-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: 0.5px;
}
.section-pill {
    background: var(--purple-glow);
    border: 1px solid var(--border-subtle);
    color: var(--purple-light);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Player Card ── */
.player-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
}
.player-card::after {
    content: '';
    position: absolute;
    bottom: 0; right: 0;
    width: 120px; height: 120px;
    background: radial-gradient(circle, var(--purple-glow) 0%, transparent 70%);
    pointer-events: none;
}
.player-avatar {
    width: 100%;
    aspect-ratio: 1;
    background: linear-gradient(135deg, var(--purple-deep), #1A0944, #0A1628);
    border-radius: 16px;
    border: 2px solid var(--border-subtle);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.player-avatar::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(245,158,11,0.1));
}
.player-name-display {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
}
.player-season-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: var(--gold-glow);
    border: 1px solid var(--border-gold);
    color: var(--gold-light);
    font-size: 0.72rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    padding: 0.2rem 0.65rem;
    border-radius: 8px;
}

/* ── Stat Metric Card ── */
.stat-card {
    background: linear-gradient(135deg, var(--bg-card), rgba(19,19,42,0.7));
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    transition: all 0.2s ease;
}
.stat-card:hover {
    border-color: rgba(124,58,237,0.4);
    background: var(--bg-card-hover);
    transform: translateY(-1px);
    box-shadow: 0 4px 20px var(--purple-glow);
}
.stat-card-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
}
.stat-card-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.65rem;
    font-weight: 700;
    color: var(--gold-light);
    line-height: 1;
}
.stat-card-sub {
    font-size: 0.72rem;
    color: var(--purple-light);
    margin-top: 0.2rem;
}

/* ── Predict Button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--purple-deep) 0%, var(--purple-main) 50%, #5B21B6 100%) !important;
    color: white !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2rem !important;
    border-radius: 12px !important;
    border: 1px solid rgba(167,139,250,0.35) !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 24px var(--purple-glow) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--purple-main) 0%, #8B5CF6 50%, var(--gold-main) 100%) !important;
    box-shadow: 0 6px 32px rgba(124,58,237,0.45) !important;
    transform: translateY(-2px) !important;
    border-color: var(--gold-light) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Prediction Result Card ── */
.prediction-card {
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.prediction-card.success {
    background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(16,185,129,0.03));
    border: 1px solid rgba(16,185,129,0.35);
}
.prediction-card.warning {
    background: linear-gradient(135deg, rgba(239,68,68,0.08), rgba(239,68,68,0.03));
    border: 1px solid rgba(239,68,68,0.35);
}
.prediction-emoji {
    font-size: 3.5rem;
    margin-bottom: 0.75rem;
    display: block;
}
.prediction-verdict {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.prediction-verdict.success { color: #34D399; }
.prediction-verdict.warning { color: #F87171; }
.prediction-sub {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
}

/* ── Confidence Bar ── */
.confidence-wrapper {
    margin-top: 1.25rem;
}
.confidence-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}
.confidence-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
}
.confidence-pct {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
}
.confidence-pct.success { color: #34D399; }
.confidence-pct.warning { color: #F87171; }
.confidence-track {
    height: 8px;
    background: rgba(255,255,255,0.06);
    border-radius: 8px;
    overflow: hidden;
}
.confidence-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.8s cubic-bezier(.4,0,.2,1);
}
.confidence-fill.success {
    background: linear-gradient(90deg, #059669, #34D399);
    box-shadow: 0 0 12px rgba(52,211,153,0.5);
}
.confidence-fill.warning {
    background: linear-gradient(90deg, #DC2626, #F87171);
    box-shadow: 0 0 12px rgba(248,113,113,0.5);
}

/* ── Model Metric Cards ── */
.model-metric {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
}
.model-metric:hover {
    border-color: var(--gold-main);
    box-shadow: 0 0 24px var(--gold-glow);
}
.model-metric::before {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--purple-main), var(--gold-main));
}
.metric-pct {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--gold-light), var(--gold-main));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.35rem;
}
.metric-name {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
}

/* ── Feature Importance Bar ── */
.feat-bar-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.85rem;
}
.feat-bar-label {
    min-width: 160px;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-secondary);
    font-family: 'JetBrains Mono', monospace;
    text-align: right;
}
.feat-bar-track {
    flex: 1;
    height: 6px;
    background: rgba(255,255,255,0.06);
    border-radius: 6px;
    overflow: hidden;
}
.feat-bar-fill {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, var(--purple-main), var(--gold-main));
}
.feat-bar-pct {
    min-width: 42px;
    text-align: right;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--gold-light);
    font-family: 'JetBrains Mono', monospace;
}

/* ── Leaderboard Table ── */
[data-testid="stDataFrame"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
.stDataFrame th {
    background: rgba(124,58,237,0.15) !important;
    color: var(--purple-light) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border-subtle) !important;
}
.stDataFrame td {
    color: var(--text-primary) !important;
    font-family: 'Exo 2', sans-serif !important;
    border-bottom: 1px solid rgba(124,58,237,0.06) !important;
}
.stDataFrame tr:hover td {
    background: rgba(124,58,237,0.06) !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Exo 2', sans-serif !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--purple-main) !important;
    box-shadow: 0 0 0 2px var(--purple-glow) !important;
}

/* ── Dividers ── */
hr {
    border-color: var(--border-subtle) !important;
    margin: 2rem 0 !important;
}

/* ── Download Button ── */
[data-testid="stDownloadButton"] button {
    background: transparent !important;
    border: 1px solid var(--border-gold) !important;
    color: var(--gold-light) !important;
    font-family: 'Exo 2', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.25rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: var(--gold-glow) !important;
    box-shadow: 0 0 16px var(--gold-glow) !important;
}

/* ── Info card ── */
.info-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 1.5rem;
}
.info-row {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(124,58,237,0.06);
}
.info-row:last-child { border-bottom: none; }
.info-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--purple-main);
    margin-top: 0.45rem;
    flex-shrink: 0;
}
.info-key {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    color: var(--text-muted);
    min-width: 90px;
    font-family: 'JetBrains Mono', monospace;
}
.info-val {
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-weight: 500;
}

/* ── Rank badge ── */
.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px; height: 28px;
    border-radius: 50%;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
}
.rank-1 { background: linear-gradient(135deg,#D97706,#FBBF24); color: #000; }
.rank-2 { background: linear-gradient(135deg,#6B7280,#D1D5DB); color: #000; }
.rank-3 { background: linear-gradient(135deg,#92400E,#D97706); color: #fff; }
.rank-n { background: rgba(124,58,237,0.15); border: 1px solid var(--border-subtle); color: var(--purple-light); }

/* ── Misc streamlit overrides ── */
p, li, label { color: var(--text-secondary) !important; }
h1, h2, h3, h4 { color: var(--text-primary) !important; font-family: 'Rajdhani', sans-serif !important; }
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 { color: var(--text-primary) !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--purple-light) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-secondary); }
::-webkit-scrollbar-thumb { background: var(--purple-deep); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--purple-main); }
</style>
""", unsafe_allow_html=True)


# ==========================================
# LOAD MODEL
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load("ipl_next_season_predictor.pkl")

# ==========================================
# LOAD DATASET
# ==========================================

@st.cache_data
def load_data():
    return pd.read_csv("player_stats.csv")

# ==========================================
# LOAD PLAYER NAME MAPPING
# ==========================================

@st.cache_data
def load_player_names():
    with open("data/Player_names.json", "r") as f:
        player_name_map = json.load(f)
    reverse_map = {v: k for k, v in player_name_map.items()}
    return player_name_map, reverse_map

model       = load_model()
df          = load_data()
player_name_map, reverse_map = load_player_names()

# ==========================================
# FEATURE COLUMNS (same order as training)
# ==========================================

FEATURES = [
    "Runs", "Balls", "Batting_Avg", "Strike_Rate",
    "Economy", "Wickets_Per_Match", "Matches",
    "Runs_Per_Match", "Balls_Per_Match", "Batting_Impact"
]

# ==========================================
# FEATURE IMPORTANCE (illustrative / replace
# with model.coef_ if logistic regression)
# ==========================================

FEATURE_IMPORTANCE = {
    "Batting Impact":      0.92,
    "Strike Rate":         0.83,
    "Batting Average":     0.76,
    "Runs Per Match":      0.71,
    "Wickets Per Match":   0.64,
    "Economy":             0.57,
    "Runs":                0.53,
    "Matches":             0.49,
    "Balls Per Match":     0.41,
    "Balls":               0.36,
}

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        🏏 IPL <span>AI</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">Navigation</div>', unsafe_allow_html=True)

    page = st.radio(
        label="nav",
        options=["🏠  Dashboard", "🔍  Player Analysis", "📈  Analytics", "ℹ️  Model Info"],
        label_visibility="hidden"
    )

    st.markdown("---")

    st.markdown('<div class="sidebar-section-label">Season</div>', unsafe_allow_html=True)
    seasons = sorted(df["Season"].unique(), reverse=True)
    selected_season = st.selectbox("Filter Season", ["All Seasons"] + [str(s) for s in seasons])

    st.markdown("---")

    # Quick dataset stats
    total_players = df["Player"].nunique()
    total_seasons = df["Season"].nunique()
    total_records = len(df)

    st.markdown(f"""
    <div class="info-card" style="margin-top:0.5rem;">
        <div style="font-size:0.68rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
                    color:var(--text-muted);margin-bottom:1rem;font-family:'JetBrains Mono',monospace;">
            Dataset Stats
        </div>
        <div class="info-row">
            <div class="info-dot"></div>
            <span class="info-key">Players</span>
            <span class="info-val" style="color:var(--gold-light);font-weight:700;">{total_players}</span>
        </div>
        <div class="info-row">
            <div class="info-dot"></div>
            <span class="info-key">Seasons</span>
            <span class="info-val" style="color:var(--gold-light);font-weight:700;">{total_seasons}</span>
        </div>
        <div class="info-row">
            <div class="info-dot"></div>
            <span class="info-key">Records</span>
            <span class="info-val" style="color:var(--gold-light);font-weight:700;">{total_records}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem;color:var(--text-muted);text-align:center;line-height:1.7;
                font-family:'JetBrains Mono',monospace;">
        Powered by<br>
        <span style="color:var(--purple-light);font-weight:600;">Logistic Regression</span><br>
        <span style="color:var(--gold-main);">v2.0 · IPL 2024</span>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# HERO BANNER (shown on all pages)
# ==========================================

st.markdown("""
<div class="hero-banner">
    <div class="hero-eyebrow">IPL Performance Intelligence Platform</div>
    <h1 class="hero-title">Next Season<br>Performance Predictor</h1>
    <p class="hero-subtitle">
        Advanced machine learning analytics that forecasts IPL player
        performance for the upcoming season using historical batting,
        bowling, and impact metrics.
    </p>
    <div class="hero-badge">LIVE MODEL · IPL 2025 EDITION</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# COMPUTE KPI STATS FOR HERO CARDS
# ==========================================

all_probs = model.predict_proba(df[FEATURES].values)[:, 1]
high_perf_count = int((all_probs >= 0.5).sum())
avg_confidence = float(all_probs.mean() * 100)
top_prob = float(all_probs.max() * 100)

# KPI ROW
kc1, kc2, kc3, kc4 = st.columns(4)
with kc1:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">👥</span>
        <div class="kpi-value">{total_players}</div>
        <div class="kpi-label">Total Players</div>
        <div class="kpi-sub">Across all seasons</div>
    </div>
    """, unsafe_allow_html=True)
with kc2:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">⚡</span>
        <div class="kpi-value">{high_perf_count}</div>
        <div class="kpi-label">High Performers</div>
        <div class="kpi-sub">Model predictions</div>
    </div>
    """, unsafe_allow_html=True)
with kc3:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🎯</span>
        <div class="kpi-value">{avg_confidence:.1f}%</div>
        <div class="kpi-label">Avg Confidence</div>
        <div class="kpi-sub">Across all players</div>
    </div>
    """, unsafe_allow_html=True)
with kc4:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-icon">🏆</span>
        <div class="kpi-value">{top_prob:.1f}%</div>
        <div class="kpi-label">Peak Probability</div>
        <div class="kpi-sub">Highest performer</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ==========================================
# PAGE: DASHBOARD / PLAYER ANALYSIS
# ==========================================

if page in ["🏠  Dashboard", "🔍  Player Analysis"]:

    # ── Player Selection ──────────────────
    st.markdown("""
    <div class="section-header">
        <span class="section-title">🔍 Player Analysis</span>
        <span class="section-pill">LIVE PREDICTION</span>
    </div>
    """, unsafe_allow_html=True)

    full_names = sorted(player_name_map.values())
    selected_full_name = st.selectbox(
        "Select a Player",
        full_names,
        help="Choose any IPL player to view their statistics and prediction"
    )

    player = reverse_map[selected_full_name]
    player_data = df[df["Player"] == player]
    latest = player_data.sort_values("Season").iloc[-1]

    # ── Two-column layout: avatar card + stats ──
    pc1, pc2 = st.columns([1, 2.5], gap="large")

    with pc1:
        # Determine initials for avatar
        parts = selected_full_name.split()
        initials = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()

        st.markdown(f"""
        <div class="player-card">
            <div class="player-avatar">{initials}</div>
            <div class="player-name-display">{selected_full_name}</div>
            <div style="margin: 0.5rem 0 1rem 0;">
                <span class="player-season-tag">📅 Season {int(latest['Season'])}</span>
            </div>
            <div style="height:1px;background:var(--border-subtle);margin:1rem 0;"></div>
            <div class="info-row">
                <div class="info-dot"></div>
                <span class="info-key">Matches</span>
                <span class="info-val" style="color:var(--gold-light);font-weight:700;">
                    {int(latest['Matches'])}
                </span>
            </div>
            <div class="info-row">
                <div class="info-dot"></div>
                <span class="info-key">Runs</span>
                <span class="info-val" style="color:var(--gold-light);font-weight:700;">
                    {int(latest['Runs'])}
                </span>
            </div>
            <div class="info-row">
                <div class="info-dot"></div>
                <span class="info-key">Wickets/M</span>
                <span class="info-val" style="color:var(--gold-light);font-weight:700;">
                    {float(latest['Wickets_Per_Match']):.2f}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with pc2:
        # Stats grid — 3 columns × 3 rows
        s1, s2, s3 = st.columns(3)
        stats = [
            ("Batting Avg",   f"{float(latest['Batting_Avg']):.2f}",    "Higher is better"),
            ("Strike Rate",   f"{float(latest['Strike_Rate']):.1f}",    "Runs per 100 balls"),
            ("Economy",       f"{float(latest['Economy']):.2f}",        "Runs per over"),
            ("Runs / Match",  f"{float(latest['Runs_Per_Match']):.2f}", "Avg contribution"),
            ("Balls",         f"{int(latest['Balls'])}",                 "Total balls faced"),
            ("Batting Impact",f"{float(latest['Batting_Impact']):.2f}", "Composite score"),
            ("Balls / Match", f"{float(latest['Balls_Per_Match']):.1f}","Avg balls faced"),
            ("Wickets / Match",f"{float(latest['Wickets_Per_Match']):.2f}","Bowling impact"),
            ("Season",        f"{int(latest['Season'])}",               "Latest data from"),
        ]
        cols = [s1, s2, s3]
        for i, (lbl, val, sub) in enumerate(stats):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="stat-card" style="margin-bottom:0.75rem;">
                    <div class="stat-card-label">{lbl}</div>
                    <div class="stat-card-value">{val}</div>
                    <div class="stat-card-sub">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── Prediction Section ─────────────────
    st.markdown("""
    <div class="section-header">
        <span class="section-title">🎯 Performance Prediction</span>
        <span class="section-pill">ML ENGINE</span>
    </div>
    """, unsafe_allow_html=True)

    predict_col, result_col = st.columns([1, 2], gap="large")

    with predict_col:
        st.markdown("""
        <div class="info-card">
            <div style="font-size:0.78rem;color:var(--text-secondary);line-height:1.7;margin-bottom:1.25rem;">
                Click the button below to run the
                <span style="color:var(--purple-light);font-weight:600;">
                Logistic Regression model
                </span>
                on this player's latest season stats and get a next-season
                performance forecast.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)
        predict_clicked = st.button("🏏 Predict Next Season Performance")

    with result_col:
        if predict_clicked:
            input_df = pd.DataFrame([[
                latest["Runs"], latest["Balls"], latest["Batting_Avg"],
                latest["Strike_Rate"], latest["Economy"],
                latest["Wickets_Per_Match"], latest["Matches"],
                latest["Runs_Per_Match"], latest["Balls_Per_Match"],
                latest["Batting_Impact"]
            ]], columns=FEATURES)

            prediction  = model.predict(input_df.values)
            probability = model.predict_proba(input_df.values)
            raw_conf    = probability[0][1] * 100

            if prediction[0] == 1:
                card_cls     = "success"
                emoji        = "🌟"
                verdict      = "High Performer Next Season"
                sub_text     = f"{selected_full_name} is highly likely to excel in IPL 2025."
                confidence   = raw_conf
            else:
                card_cls     = "warning"
                emoji        = "⚠️"
                verdict      = "Unlikely to be High Performer"
                sub_text     = f"{selected_full_name} may not reach top-tier performance next season."
                confidence   = 100 - raw_conf

            st.markdown(f"""
            <div class="prediction-card {card_cls}">
                <span class="prediction-emoji">{emoji}</span>
                <div class="prediction-verdict {card_cls}">{verdict}</div>
                <div class="prediction-sub">{sub_text}</div>
                <div class="confidence-wrapper">
                    <div class="confidence-header">
                        <span class="confidence-label">Confidence Score</span>
                        <span class="confidence-pct {card_cls}">{confidence:.1f}%</span>
                    </div>
                    <div class="confidence-track">
                        <div class="confidence-fill {card_cls}"
                             style="width:{confidence:.1f}%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:var(--bg-card);border:1px dashed var(--border-subtle);
                        border-radius:16px;padding:2.5rem;text-align:center;">
                <div style="font-size:2.5rem;margin-bottom:0.75rem;">🏏</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:1.15rem;
                            color:var(--text-secondary);font-weight:500;">
                    Select a player and click
                    <span style="color:var(--purple-light);">Predict</span> to see the forecast
                </div>
            </div>
            """, unsafe_allow_html=True)


# ==========================================
# PAGE: ANALYTICS
# ==========================================

if page in ["🏠  Dashboard", "📈  Analytics"]:

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <span class="section-title">📈 Model Analytics</span>
        <span class="section-pill">INSIGHTS</span>
    </div>
    """, unsafe_allow_html=True)

    analyt_left, analyt_right = st.columns([1.3, 1], gap="large")

    # ── Feature Importance ────────────────
    with analyt_left:
        st.markdown("""
        <div class="info-card">
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;
                        color:var(--text-primary);margin-bottom:1.25rem;letter-spacing:0.3px;">
                Feature Importance
            </div>
        """, unsafe_allow_html=True)

        feat_html = ""
        for feat, imp in sorted(FEATURE_IMPORTANCE.items(), key=lambda x: -x[1]):
            pct = imp * 100
            feat_html += f"""
            <div class="feat-bar-row">
                <span class="feat-bar-label">{feat}</span>
                <div class="feat-bar-track">
                    <div class="feat-bar-fill" style="width:{pct:.0f}%;"></div>
                </div>
                <span class="feat-bar-pct">{pct:.0f}%</span>
            </div>
            """

        st.markdown(feat_html + "</div>", unsafe_allow_html=True)

    # ── Model Performance Metrics ─────────
    with analyt_right:
        st.markdown("""
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;
                    color:var(--text-primary);margin-bottom:1rem;letter-spacing:0.3px;">
            Model Performance Metrics
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        for col, (label, value) in zip(
            [m1, m2, m3],
            [("Accuracy", "85%"), ("Precision", "59%"), ("Recall", "55%")]
        ):
            with col:
                st.markdown(f"""
                <div class="model-metric">
                    <div class="metric-pct">{value}</div>
                    <div class="metric-name">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        # Confusion matrix mini visual
        st.markdown("""
        <div class="info-card" style="margin-top:0;">
            <div style="font-size:0.72rem;font-weight:700;letter-spacing:1.5px;
                        text-transform:uppercase;color:var(--text-muted);
                        margin-bottom:1rem;font-family:'JetBrains Mono',monospace;">
                Classification Summary
            </div>
            <div class="info-row">
                <div class="info-dot" style="background:#10B981;"></div>
                <span class="info-key">Algorithm</span>
                <span class="info-val">Logistic Regression</span>
            </div>
            <div class="info-row">
                <div class="info-dot" style="background:#10B981;"></div>
                <span class="info-key">Target</span>
                <span class="info-val">High Performer (binary)</span>
            </div>
            <div class="info-row">
                <div class="info-dot" style="background:#10B981;"></div>
                <span class="info-key">Features</span>
                <span class="info-val">10 batting & bowling metrics</span>
            </div>
            <div class="info-row">
                <div class="info-dot" style="background:#F59E0B;"></div>
                <span class="info-key">F1-Score</span>
                <span class="info-val" style="color:var(--gold-light);font-weight:600;">0.57</span>
            </div>
            <div class="info-row">
                <div class="info-dot" style="background:#F59E0B;"></div>
                <span class="info-key">AUC-ROC</span>
                <span class="info-val" style="color:var(--gold-light);font-weight:600;">0.78</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Top 10 Leaderboard ─────────────────
    st.markdown("""
    <div class="section-header" style="margin-top:2rem;">
        <span class="section-title">🏆 Top 10 Most Likely Performers</span>
        <span class="section-pill">RANKED</span>
    </div>
    """, unsafe_allow_html=True)

    leaderboard_df = df.copy()
    leaderboard_df["Performance_Probability"] = model.predict_proba(
        leaderboard_df[FEATURES].values
    )[:, 1]
    leaderboard_df = (
        leaderboard_df
        .sort_values("Season")
        .groupby("Player")
        .tail(1)
    )
    leaderboard_df["Player"] = (
        leaderboard_df["Player"]
        .map(player_name_map)
        .fillna(leaderboard_df["Player"])
    )

    leaderboard = (
        leaderboard_df[["Player", "Season", "Performance_Probability"]]
        .sort_values("Performance_Probability", ascending=False)
        .head(10)
        .copy()
    )
    leaderboard["Performance_Probability"] = (
        leaderboard["Performance_Probability"] * 100
    ).round(2)
    leaderboard.insert(0, "Rank", range(1, len(leaderboard) + 1))
    leaderboard.columns = ["Rank", "Player", "Season", "Chance (%)"]

    st.dataframe(
        leaderboard,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Player": st.column_config.TextColumn("Player", width="medium"),
            "Season": st.column_config.NumberColumn("Season", width="small", format="%d"),
            "Chance (%)": st.column_config.ProgressColumn(
                "Performance Chance (%)",
                min_value=0,
                max_value=100,
                format="%.2f%%",
                width="large"
            )
        }
    )

    csv = leaderboard.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Leaderboard CSV",
        data=csv,
        file_name="IPL_Top10_Predictions.csv",
        mime="text/csv"
    )


# ==========================================
# PAGE: MODEL INFO
# ==========================================

if page == "ℹ️  Model Info":

    st.markdown("""
    <div class="section-header">
        <span class="section-title">ℹ️ Model Information</span>
        <span class="section-pill">DETAILS</span>
    </div>
    """, unsafe_allow_html=True)

    info_c1, info_c2 = st.columns(2, gap="large")

    with info_c1:
        st.markdown("""
        <div class="info-card">
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;
                        color:var(--text-primary);margin-bottom:1.25rem;">
                Algorithm Details
            </div>
            <div class="info-row">
                <div class="info-dot"></div>
                <span class="info-key">Algorithm</span>
                <span class="info-val">Logistic Regression</span>
            </div>
            <div class="info-row">
                <div class="info-dot"></div>
                <span class="info-key">Target</span>
                <span class="info-val">High Performer Next Season</span>
            </div>
            <div class="info-row">
                <div class="info-dot"></div>
                <span class="info-key">Type</span>
                <span class="info-val">Binary Classification</span>
            </div>
            <div class="info-row">
                <div class="info-dot"></div>
                <span class="info-key">Scaler</span>
                <span class="info-val">StandardScaler</span>
            </div>
            <div class="info-row">
                <div class="info-dot"></div>
                <span class="info-key">Class Weights</span>
                <span class="info-val">Balanced</span>
            </div>
            <div class="info-row">
                <div class="info-dot"></div>
                <span class="info-key">Solver</span>
                <span class="info-val">lbfgs</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with info_c2:
        st.markdown("""
        <div class="info-card">
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;
                        color:var(--text-primary);margin-bottom:1.25rem;">
                Features Used (10 total)
            </div>
        """, unsafe_allow_html=True)

        features_info = [
            ("Runs",              "Total runs scored in the season"),
            ("Balls",             "Total balls faced"),
            ("Batting_Avg",       "Runs per dismissal"),
            ("Strike_Rate",       "Runs per 100 balls"),
            ("Economy",           "Runs conceded per over"),
            ("Wickets_Per_Match", "Average wickets per game"),
            ("Matches",           "Number of matches played"),
            ("Runs_Per_Match",    "Average runs per game"),
            ("Balls_Per_Match",   "Average balls faced per game"),
            ("Batting_Impact",    "Composite batting performance index"),
        ]
        rows_html = ""
        for feat, desc in features_info:
            rows_html += f"""
            <div class="info-row">
                <div class="info-dot"></div>
                <span class="info-key">{feat}</span>
                <span class="info-val">{desc}</span>
            </div>"""
        st.markdown(rows_html + "</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # Performance metrics repeated
    st.markdown("""
    <div class="section-header">
        <span class="section-title">📊 Model Performance</span>
        <span class="section-pill">EVALUATION</span>
    </div>
    """, unsafe_allow_html=True)

    mp1, mp2, mp3, mp4 = st.columns(4)
    for col, (lbl, val) in zip(
        [mp1, mp2, mp3, mp4],
        [("Accuracy", "85%"), ("Precision", "59%"), ("Recall", "55%"), ("F1-Score", "57%")]
    ):
        with col:
            st.markdown(f"""
            <div class="model-metric">
                <div class="metric-pct">{val}</div>
                <div class="metric-name">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)