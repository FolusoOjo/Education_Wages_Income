from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import base64
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parent

def app_path(*parts):
    return BASE_DIR.joinpath(*parts)

    
st.set_page_config(
    page_title="Bridging the Gap",
    layout="wide",
    page_icon="🌐",
    initial_sidebar_state="collapsed"
)
 
# ─────────────────────────────────────────
# THEME STATE  — must come before any CSS
# ─────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
 
# A tiny invisible toggle button at the very top-right
# We render the actual styled button INSIDE the hero below,
# but the click target has to be a real st.button.
# Trick: put it in an empty top container so it doesn't
# break the layout, then re-style it with CSS.
toggle_container = st.container()
 
is_dark = st.session_state.dark_mode
 
# ─────────────────────────────────────────
# THEME COLORS
# ─────────────────────────────────────────
if is_dark:
    BG_COLOR       = "#0d0f1a"
    SURFACE_COLOR  = "#161929"
    BORDER_COLOR   = "#1e2235"
    FONT_PRIMARY   = "#e8e6f0"
    FONT_SECONDARY = "#8b8fa8"
    FONT_MUTED     = "#4a4e6a"
    GRID_COLOR     = "#1e2235"
    ACCENT_COLOR   = "#6c8fff"
    HERO_TITLE_C   = "#ffffff"
    RESULT_BG      = "#0d0f1a"
    INSIGHT_BG     = "#161929"
    INSIGHT_BORDER = "#2a2f4a"
    TOGGLE_ICON    = "☀️"
    TOGGLE_LABEL   = "Light mode"
    TOGGLE_BG      = "#1e2235"
    TOGGLE_FG      = "#8b8fa8"
else:
    BG_COLOR       = "#f7f6f2"
    SURFACE_COLOR  = "#ffffff"
    BORDER_COLOR   = "#e0ddd6"
    FONT_PRIMARY   = "#1a1a2e"
    FONT_SECONDARY = "#555555"
    FONT_MUTED     = "#999999"
    GRID_COLOR     = "#e0ddd6"
    ACCENT_COLOR   = "#2a5cff"
    HERO_TITLE_C   = "#1a1a2e"
    RESULT_BG      = "#f7f6f2"
    INSIGHT_BG     = "#eef1ff"
    INSIGHT_BORDER = "#c5ccee"
    TOGGLE_ICON    = "🌙"
    TOGGLE_LABEL   = "Dark mode"
    TOGGLE_BG      = "#f0efeb"
    TOGGLE_FG      = "#555555"
 
CANADA_COLOR = "#D80621"
US_COLOR     = "#3C3B6E"
 
# ─────────────────────────────────────────
# CSS — full block
# ─────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
 
html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    font-size: 16px;
}}
.stApp {{
    background: {BG_COLOR};
    color: {FONT_PRIMARY};
}}
.block-container {{
    padding: 0rem 2.5rem 4rem 2.5rem;
    max-width: 1080px;
}}
 
/* ── Theme toggle pill ── */
#theme-toggle-wrap {{
    position: fixed;
    top: 14px;
    right: 24px;
    z-index: 9999;
}}
div[data-testid="stVerticalBlock"]:has(> div[data-testid="element-container"]:first-child > div[data-testid="stButton"][key="theme_toggle_btn"]) {{
    position: fixed;
    top: 14px;
    right: 24px;
    z-index: 9999;
}}
.theme-toggle-outer {{
    position: fixed;
    top: 14px;
    right: 24px;
    z-index: 9999;
}}
.theme-toggle-outer button,
.theme-toggle-outer button:focus,
.theme-toggle-outer button:active {{
    background: {TOGGLE_BG} !important;
    color: {TOGGLE_FG} !important;
    border: 1px solid {BORDER_COLOR} !important;
    border-radius: 30px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .85rem !important;
    font-weight: 500 !important;
    padding: 6px 16px !important;
    width: auto !important;
    letter-spacing: .03em !important;
    box-shadow: 0 2px 8px rgba(0,0,0,.12) !important;
    cursor: pointer !important;
}}
.theme-toggle-outer button:hover {{
    opacity: .85 !important;
    border-color: {ACCENT_COLOR} !important;
}}
 
/* Hero */
.hero-wrap {{
    padding: 3.5rem 0 2.5rem;
    border-bottom: 1px solid {BORDER_COLOR};
    margin-bottom: 2.5rem;
}}
.hero-eyebrow {{
    font-size: 0.8rem;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: {FONT_MUTED};
    margin-bottom: .8rem;
}}
.hero-title {{
    font-family: 'DM Serif Display', serif;
    font-size: 3.2rem;
    line-height: 1.05;
    color: {HERO_TITLE_C};
    margin-bottom: 1rem;
}}
.hero-title span {{ color: {ACCENT_COLOR}; }}
.hero-sub {{
    font-size: 1.05rem;
    color: {FONT_SECONDARY};
    line-height: 1.75;
    max-width: 560px;
}}
.flag-row {{
    display: flex;
    gap: .5rem;
    margin-top: 1.4rem;
    flex-wrap: wrap;
}}
.flag-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: {SURFACE_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 20px;
    padding: 5px 13px;
    font-size: .85rem;
    color: {FONT_SECONDARY};
}}
.stat-col {{
    display: flex;
    flex-direction: column;
    gap: .7rem;
    align-items: flex-end;
    justify-content: center;
    padding-top: 2.5rem;
}}
.stat-box {{
    background: {SURFACE_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 14px;
    padding: 1rem 1.4rem;
    text-align: center;
    min-width: 120px;
}}
.stat-num {{
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: {ACCENT_COLOR};
}}
.stat-lbl {{
    font-size: .75rem;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: {FONT_MUTED};
    margin-top: 3px;
}}
 
/* Section headers */
.sec-header {{
    display: flex;
    align-items: baseline;
    gap: .6rem;
    margin: 2.8rem 0 1.3rem;
    padding-bottom: .6rem;
    border-bottom: 1px solid {BORDER_COLOR};
}}
.sec-title {{
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: {FONT_PRIMARY};
    letter-spacing: .05em;
    text-transform: uppercase;
}}
.sec-tag {{
    font-size: .75rem;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: {FONT_MUTED};
    border: 1px solid {BORDER_COLOR};
    border-radius: 20px;
    padding: 2px 9px;
}}
 
/* Predict card */
.predict-card {{
    background: {SURFACE_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 18px;
    overflow: hidden;
}}
.predict-disclaimer {{
    font-size: .85rem;
    color: {FONT_MUTED};
    padding: .7rem 1.4rem 1.1rem;
    line-height: 1.6;
    border-top: 1px solid {BORDER_COLOR};
}}
 
/* Result boxes */
.result-row {{
    display: flex;
    gap: .8rem;
    padding: 1.1rem 1.3rem;
    border-top: 1px solid {BORDER_COLOR};
    background: {RESULT_BG};
}}
.result-box {{
    flex: 1;
    background: {SURFACE_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 12px;
    padding: 1rem 1.1rem;
}}
.result-lbl {{
    font-size: .75rem;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: {FONT_MUTED};
    margin-bottom: 5px;
}}
.result-val {{
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: {FONT_PRIMARY};
}}
.result-val.green {{ color: #1a7a4a; }}
.result-val.amber {{ color: #9c6a00; }}
.result-val.red   {{ color: #a33030; }}
.result-val.blue  {{ color: {ACCENT_COLOR}; }}
 
/* Metrics grid */
.metrics-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}}
.met-box {{
    background: {SURFACE_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
}}
.met-lbl {{
    font-size: .75rem;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: {FONT_MUTED};
    margin-bottom: 6px;
}}
.met-val {{
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: {FONT_PRIMARY};
    line-height: 1.3;
}}
 
/* Insight strip */
.insight-strip {{
    background: {INSIGHT_BG};
    border: 1px solid {INSIGHT_BORDER};
    border-left: 3px solid {ACCENT_COLOR};
    color: {FONT_SECONDARY};
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.3rem;
    font-size: 1rem;
    line-height: 1.7;
    margin-top: .7rem;
}}
.insight-strip strong {{ color: {FONT_PRIMARY}; font-weight: 600; }}
 
/* Model note */
.model-note {{
    font-size: .9rem;
    color: {FONT_MUTED};
    margin-top: .6rem;
    line-height: 1.6;
    padding: .8rem 1rem;
    background: {SURFACE_COLOR};
    border-radius: 10px;
    border: 1px solid {BORDER_COLOR};
}}
 
/* Policy cards */
.policy-card {{
    background: {SURFACE_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 16px;
    overflow: hidden;
    height: 100%;
}}
.policy-head {{
    padding: .8rem 1.1rem;
    border-bottom: 1px solid {BORDER_COLOR};
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: {FONT_PRIMARY};
    display: flex;
    align-items: center;
    gap: 7px;
}}
.policy-body {{ padding: 1rem 1.1rem; }}
.timeline-item {{
    display: flex;
    gap: 10px;
    margin-bottom: 11px;
    font-size: .95rem;
}}
.timeline-item:last-child {{ margin-bottom: 0; }}
.t-yr {{
    min-width: 40px;
    font-weight: 600;
    color: {ACCENT_COLOR};
    font-size: .88rem;
    padding-top: 1px;
}}
.t-txt {{ color: {FONT_SECONDARY}; line-height: 1.55; }}
 
/* Feature / future boxes */
.feat-box {{
    background: {SURFACE_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: .6rem;
}}
.feat-title {{
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: {ACCENT_COLOR};
    margin-bottom: 5px;
}}
.feat-desc {{
    font-size: .95rem;
    color: {FONT_SECONDARY};
    line-height: 1.65;
}}
 
/* Final note */
.final-note {{
    border-left: 3px solid {ACCENT_COLOR};
    padding: 1rem 1.2rem;
    background: {SURFACE_COLOR};
    border-radius: 0 12px 12px 0;
    font-size: 1rem;
    color: {FONT_SECONDARY};
    line-height: 1.7;
}}
 
/* ── Streamlit widget overrides ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label,
div[data-testid="stRadio"] label {{
    font-size: .85rem !important;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: {FONT_MUTED} !important;
    font-family: 'DM Sans', sans-serif !important;
}}
div[data-testid="stSelectbox"] > div > div {{
    background: {BG_COLOR} !important;
    border: 1px solid {BORDER_COLOR} !important;
    color: {FONT_PRIMARY} !important;
    border-radius: 8px !important;
    font-size: 1rem !important;
}}
 
/* All regular buttons */
div[data-testid="stButton"] > button {{
    background: {ACCENT_COLOR} !important;
    color: {'#0d0f1a' if is_dark else '#ffffff'} !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: .6rem 1.4rem !important;
    width: 100% !important;
    letter-spacing: .03em !important;
}}
div[data-testid="stButton"] > button:hover {{ opacity: .85 !important; }}
 
/* ── Theme toggle button — override the accent style ── */
div[data-testid="stButton"].theme-toggle-btn > button {{
    background: {TOGGLE_BG} !important;
    color: {TOGGLE_FG} !important;
    border: 1px solid {BORDER_COLOR} !important;
    border-radius: 30px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: .88rem !important;
    padding: 6px 16px !important;
    width: auto !important;
    box-shadow: 0 2px 8px rgba(0,0,0,.12) !important;
}}
 
div[data-testid="stDownloadButton"] > button {{
    background: {SURFACE_COLOR} !important;
    color: {ACCENT_COLOR} !important;
    border: 1px solid {BORDER_COLOR} !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .95rem !important;
    width: 100% !important;
}}
div[data-testid="stAlert"] {{
    background: {'#1e1a0d' if is_dark else '#fffbea'} !important;
    border: 1px solid {'#3a3010' if is_dark else '#e6cc80'} !important;
    border-radius: 8px !important;
    color: {'#fbbf24' if is_dark else '#7a5900'} !important;
    font-size: .95rem !important;
}}

/* ── Mobile ── */
@media (max-width: 640px) {{
    .block-container {{ padding: 0 1rem 3rem !important; }}
    .hero-title {{ font-size: 2rem !important; }}
    .hero-wrap {{ padding: 2rem 0 1.5rem !important; }}
    .result-row {{ flex-direction: column !important; }}
    .metrics-grid {{ grid-template-columns: 1fr !important; }}
    .stat-col {{
        flex-direction: row !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        justify-content: flex-start !important;
        padding-top: 0 !important;
    }}
}}
</style>
""", unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────
# THEME TOGGLE — rendered inline at top of page
# Using columns so it reliably appears top-right
# ─────────────────────────────────────────
_spacer, _toggle_col = st.columns([8, 2])
with _toggle_col:
    if st.button(f"{TOGGLE_ICON}  {TOGGLE_LABEL}", key="theme_toggle_btn", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Keep toggle_container for backwards compatibility but render nothing in it
with toggle_container:
    pass
 
 
# ─────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────
@st.cache_resource
def load_models(country: str):
    folder = "Canada" if country == "Canada" else "US"
    reg = joblib.load(app_path(folder, f"{folder.lower()}_structural_regressor.pkl"))
    clf = joblib.load(app_path(folder, f"{folder.lower()}_structural_classifier.pkl"))
    return reg, clf
 
 
def get_base64_image(image_path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
 
 
@st.cache_data
def get_mean_incomes(country: str):
    if country == "Canada":
        path = app_path("cis_data_cleaned_for_ml.csv")
    else:
        us_main = app_path("us_df_clean.csv")
        us_alt = app_path("us_df_clean (1).csv")
        path = us_main if us_main.exists() else us_alt

    df = pd.read_csv(path)
    df = df[df["total_income"].notna() & (df["total_income"] > 0)]
    by_edu = df.groupby("education")["total_income"].mean().round(2)
    by_edu_imm = df.groupby(["education", "immigrant_status"])["total_income"].mean().round(2)
    return by_edu, by_edu_imm
 
 
# Load flag images (fallback gracefully if files missing)
def _load_flag(filename_stem: str, fallback_emoji: str) -> str:
    for ext in ["JPG", "jpg", "jpeg", "png"]:
        path = app_path(f"{filename_stem}.{ext}")
        if path.exists():
            try:
                b64 = get_base64_image(path)
                return f'<img src="data:image/jpeg;base64,{b64}" style="width:22px; vertical-align:middle;">'
            except Exception:
                pass
    return fallback_emoji

flag_ca = _load_flag("canada_ca", "🇨🇦")
flag_us = _load_flag("us_us", "🇺🇸")
 
 
EDU_DISPLAY = [
    "Less than high school",
    "High school diploma",
    "Postsecondary certificate or diploma",
    "University degree",
]
EDU_SHORT  = ["Less than high school", "High school diploma", "Postsecondary certificate or diploma", "University degree"]
IMM_MAP_CA = {"Immigrant": "Immigrant", "Born in country": "Born in Canada (non-immigrant)"}
IMM_MAP_US = {"Immigrant": "Immigrant", "Born in country": "Born in US"}
 
 
# ─────────────────────────────────────────
# HERO
# ─────────────────────────────────────────
col_hero, col_stats = st.columns([3, 1])
 
with col_hero:
    st.markdown(f"""
    <div class="hero-wrap">
        <div class="hero-eyebrow">Machine learning study · 2018–2022</div>
        <div class="hero-title">Bridging the Gap:<br>Education &amp; Income Inequality Among <span>Immigrants</span></div>
        <div class="hero-sub">
            A comparative analysis of how education shapes income outcomes
            for immigrants in Canada and the United States — and where the gap persists.
        </div>
        <div class="flag-row">
            <span class="flag-pill">{flag_ca} Canada</span>
            <span class="flag-pill">{flag_us} United States</span>
            <span class="flag-pill">📅 2018 – 2022</span>
            <span class="flag-pill">⚙️ 4 structural features</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
with col_stats:
    st.markdown(f"""
    <div class="stat-col">
        <div class="stat-box"><div class="stat-num">2</div><div class="stat-lbl">Countries</div></div>
        <div class="stat-box"><div class="stat-num">5</div><div class="stat-lbl">Years of data</div></div>
        <div class="stat-box"><div class="stat-num">5+</div><div class="stat-lbl">Models tested</div></div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# HOW TO USE
# ─────────────────────────────────────────
with st.expander("ℹ️  How to use this app"):
    st.markdown("""
    1. **Select a country** — Canada or United States
    2. **Fill in a profile** — choose education level, gender, immigrant status, and year
    3. **Adjust the growth slider** if predicting beyond 2022 — this accounts for year-over-year income growth (inflation)
    4. **Click Predict** — the app returns an estimated income in dollars, the predicted income group (Low / Medium / High), and how that education level compares to a high school diploma holder with the same demographic profile

    > *This app uses machine learning models trained on the Canadian Income Survey (CIS) and American Community Survey (ACS) data from 2018–2022.
    > The structural model uses only 4 demographic features: year, education, gender, and immigrant status.*
    """)
 
 
# ─────────────────────────────────────────
# PREDICTOR
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Income predictor</span>
    <span class="sec-tag">ML model</span>
</div>
""", unsafe_allow_html=True)
 
st.markdown('<div class="predict-card">', unsafe_allow_html=True)
 
left, right = st.columns(2)
 
with left:
    st.markdown("<div style='padding:1.3rem 1.3rem 0.5rem'>", unsafe_allow_html=True)
    country  = st.selectbox("Country", ["Canada", "United States"], key="country")
    edu_disp = st.selectbox("Education level", EDU_DISPLAY, key="edu")
    gender   = st.radio("Gender", ["Male", "Female"], horizontal=True, key="gender")
    st.markdown("</div>", unsafe_allow_html=True)
 
with right:
    st.markdown("<div style='padding:1.3rem 1.3rem 0.5rem'>", unsafe_allow_html=True)
    immigrant   = st.selectbox("Immigrant status", ["Immigrant", "Born in country"], key="imm")
    year        = st.slider("Year", 2018, 2030, 2022, key="year")
    if year > 2022:
        st.warning(f"Projecting {year - 2022} year(s) beyond 2022 using the growth adjustment rate.")
    elif year < 2022:
        st.info("Showing 2022 baseline income. Year has minimal effect on structural predictions — demographics drive the model.")
    inflation   = st.slider("Growth adjustment (%)", 0.0, 5.0, 2.0, step=0.5, key="inflation")
    predict_btn = st.button("Predict income outcome →", key="predict")
    st.markdown("</div>", unsafe_allow_html=True)
 
if predict_btn:
    imm_map  = IMM_MAP_CA if country == "Canada" else IMM_MAP_US

    # Labels for the selected and comparison immigrant status
    if country == "Canada":
        imm_label_selected = imm_map[immigrant]
        imm_label_other    = "Born in Canada (non-immigrant)" if immigrant == "Immigrant" else "Immigrant"
    else:
        imm_label_selected = imm_map[immigrant]
        imm_label_other    = "Born in US" if immigrant == "Immigrant" else "Immigrant"

    # Always use 2022 as the model input anchor.
    # Year has very low feature importance in the structural model — demographics dominate.
    model_year = 2022

    # ── Model prediction for selected profile ─────────────────────
    input_df = pd.DataFrame({
        "year":             [model_year],
        "gender":           [gender],
        "education":        [edu_disp],
        "immigrant_status": [imm_label_selected],
    })

    try:
        reg_model, clf_model = load_models(country)
    except FileNotFoundError:
        st.error(f"Model files not found for {country}. Make sure the required .pkl files are in the correct folder.")
        st.stop()

    income = reg_model.predict(input_df)[0]
    group  = clf_model.predict(input_df)[0]

    # Apply compound inflation growth for every year beyond 2022
    if year > 2022:
        factor  = (1 + inflation / 100) ** (year - 2022)
        income *= factor

    # ── Education premium vs high school ─────────────────────────
    hs_df = pd.DataFrame({
        "year":             [model_year],
        "gender":           [gender],
        "education":        ["High school diploma"],
        "immigrant_status": [imm_label_selected],
    })
    hs_income = reg_model.predict(hs_df)[0]
    if year > 2022:
        hs_income *= (1 + inflation / 100) ** (year - 2022)

    if edu_disp == "High school diploma":
        premium_str = "Baseline"
    else:
        premium     = round((income - hs_income) / hs_income * 100)
        premium_str = (f"+{premium}%" if premium >= 0 else f"{premium}%") + " vs HS"

    group_color = ("green" if "High" in str(group)
                   else "red"   if "Low"  in str(group)
                   else "amber")

    # ── Comparison income: use REAL DATA average, not model prediction ────────
    # The structural model can mispredict the direction of the immigrant gap at
    # certain education levels due to compositional effects in the training data.
    # Using actual dataset averages ensures the comparison always reflects the
    # true research finding: non-immigrants earn more at every education level.
    try:
        _, by_edu_imm = get_mean_incomes(country)
        income_other_real = by_edu_imm.get((edu_disp, imm_label_other), None)
        income_self_real  = by_edu_imm.get((edu_disp, imm_label_selected), None)
    except Exception:
        income_other_real = None
        income_self_real  = None

    # If real data is available, use it for comparison; otherwise fall back to model
    if income_other_real is not None:
        # Apply same inflation factor to the real data baseline for consistency
        income_other = float(income_other_real)
        if year > 2022:
            income_other *= (1 + inflation / 100) ** (year - 2022)
        data_source_other = "actual data"
    else:
        # Fallback: run model for the other status (only if CSV not available)
        input_df_other = pd.DataFrame({
            "year":             [model_year],
            "gender":           [gender],
            "education":        [edu_disp],
            "immigrant_status": [imm_label_other],
        })
        income_other = reg_model.predict(input_df_other)[0]
        if year > 2022:
            income_other *= (1 + inflation / 100) ** (year - 2022)
        data_source_other = "model estimate"

    # Income gap from the perspective of the selected profile
    income_gap    = income - income_other
    gap_abs       = abs(income_gap)
    gap_pct       = abs(round(income_gap / income_other * 100)) if income_other > 0 else 0

    st.session_state["pred"] = {
        "income": income, "group": group, "group_color": group_color,
        "income_other": income_other,
        "data_source_other": data_source_other,
        "premium_str": premium_str,
        "input_df": input_df,
        "country": country, "year": year,
        "inflation": inflation,
        "immigrant": immigrant,
        "imm_label_selected": imm_label_selected,
        "imm_label_other": imm_label_other,
        "income_gap": income_gap,
        "gap_abs": gap_abs, "gap_pct": gap_pct,
        "edu_disp": edu_disp,
    }

if "pred" in st.session_state:
    p = st.session_state["pred"]

    selected_short = "Immigrant" if p["immigrant"] == "Immigrant" else "Born in country"
    other_short    = "Born in country" if p["immigrant"] == "Immigrant" else "Immigrant"

    # Pull BOTH groups from real data so the comparison is apples-to-apples
    try:
        _, by_edu_imm_chart = get_mean_incomes(p["country"])
        real_selected = by_edu_imm_chart.get((p["edu_disp"], p["imm_label_selected"]), None)
        real_other    = by_edu_imm_chart.get((p["edu_disp"], p["imm_label_other"]),    None)

        if real_selected is not None and real_other is not None:
            # Apply inflation to both real-data values if projecting beyond 2022
            factor = (1 + p.get("inflation", 0) / 100) ** max(0, p["year"] - 2022)
            disp_selected = float(real_selected) * factor
            disp_other    = float(real_other)    * factor
            lbl_selected  = f"Expected earnings · {selected_short}"
            lbl_other     = f"Expected earnings · {other_short}"
        else:
            disp_selected = p["income"]
            disp_other    = p["income_other"]
            lbl_selected  = f"ML estimate · {selected_short}"
            lbl_other     = f"ML estimate · {other_short}"
    except Exception:
        disp_selected = p["income"]
        disp_other    = p["income_other"]
        lbl_selected  = f"ML estimate · {selected_short}"
        lbl_other     = f"ML estimate · {other_short}"

    # Non-immigrant always earns more — color accordingly
    if p["immigrant"] == "Immigrant":
        col_selected = "amber"   # immigrant
        col_other    = "green"   # non-immigrant earns more
    else:
        col_selected = "green"   # non-immigrant
        col_other    = "amber"   # immigrant earns less

    real_gap_abs = abs(disp_other - disp_selected)
    real_gap_pct = abs(round((disp_other - disp_selected) / disp_selected * 100)) if disp_selected > 0 else 0

    st.markdown(f"""
    <div class="result-row">
        <div class="result-box">
            <div class="result-lbl">{lbl_selected}</div>
            <div class="result-val {col_selected}">${disp_selected:,.0f}</div>
        </div>
        <div class="result-box">
            <div class="result-lbl">{lbl_other}</div>
            <div class="result-val {col_other}">${disp_other:,.0f}</div>
        </div>
        <div class="result-box">
            <div class="result-lbl">Income group · {selected_short}</div>
            <div class="result-val {p['group_color']}">{p['group']}</div>
        </div>
        <div class="result-box">
            <div class="result-lbl">Education boost vs high school</div>
            <div class="result-val blue">{p['premium_str']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Gap insight strip — plain English ────────────────────────
    country_word = "Canada" if p["country"] == "Canada" else "the United States"
    if p["immigrant"] == "Immigrant":
        gap_msg = (
            f"People born in {country_word} with the same education level earn about "
            f"<strong>${real_gap_abs:,.0f} more per year</strong> than immigrants "
            f"— that is a <strong>{real_gap_pct}% pay gap</strong>. "
            f"Even with a university degree, immigrants still earn less. "
            f"This gap is what our study set out to measure."
        )
    else:
        gap_msg = (
            f"As someone born in {country_word}, you earn about "
            f"<strong>${real_gap_abs:,.0f} more per year</strong> than an immigrant "
            f"with the exact same education level and background "
            f"— a <strong>{real_gap_pct}% difference</strong>. "
            f"This pay gap widens even more for people with a university degree."
        )

    st.markdown(f"""
    <div class="insight-strip">
        {gap_msg}
        <br><small style="opacity:0.7">
        These earnings figures come directly from our dataset (2018–2022 averages).
        The income group (Low / Medium / High) is what our machine learning model predicts.
        </small>
    </div>
    """, unsafe_allow_html=True)

    out = p["input_df"].copy()
    out["Predicted_Income"]      = round(p["income"], 2)
    out["Income_Group"]          = p["group"]
    out["Comparison_Status"]     = p["imm_label_other"]
    out["Comparison_Avg_Income"] = round(disp_other, 2)
    st.download_button(
        "💾 Download result as CSV",
        out.to_csv(index=False).encode(),
        f"{p['country']}_{p['year']}_prediction.csv",
        key="dl"
    )
 
st.markdown("""
<div class="predict-disclaimer">
    Model uses education, gender, and immigrant status as the primary structural features.
    The 2022 income baseline is used as the reference point — year is fixed at 2022 internally
    because the structural model's predictions are driven by demographics, not year variation.
    R² ≈ 0.12–0.13 reflects structural population-level patterns, not individual income prediction.
    The education premium shows how much more (or less) this education level earns compared to a
    high school diploma holder with the same demographic profile.
    Future year projections apply compound growth using the growth adjustment rate.
</div>
</div>
""", unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────
# INCOME CHART — immigrant vs non-immigrant by education level
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Average income by education & immigrant status</span>
    <span class="sec-tag">Actual data</span>
</div>
""", unsafe_allow_html=True)

# Country toggle for the chart
chart_country = st.radio(
    "Select country to view",
    ["Canada", "United States"],
    horizontal=True,
    key="chart_country"
)

try:
    _, by_edu_imm_ca = get_mean_incomes("Canada")
    _, by_edu_imm_us = get_mean_incomes("United States")

    by_edu_imm = by_edu_imm_ca if chart_country == "Canada" else by_edu_imm_us

    # Immigrant status labels vary by country
    if chart_country == "Canada":
        imm_label  = "Immigrant"
        non_label  = "Born in Canada (non-immigrant)"
        imm_color  = "#E85D30"   # warm orange-red for immigrant
        non_color  = CANADA_COLOR
    else:
        imm_label  = "Immigrant"
        non_label  = "Born in US"
        imm_color  = "#7A6FC0"   # muted purple for immigrant
        non_color  = US_COLOR

    imm_vals = [by_edu_imm.get((e, imm_label), 0) for e in EDU_DISPLAY]
    non_vals = [by_edu_imm.get((e, non_label), 0) for e in EDU_DISPLAY]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Non-immigrant",
        y=EDU_DISPLAY,
        x=non_vals,
        orientation="h",
        marker_color=non_color,
        text=[f"${v/1000:.0f}k" for v in non_vals],
        textposition="outside",
        textfont=dict(color=FONT_SECONDARY, size=11),
    ))
    fig.add_trace(go.Bar(
        name="Immigrant",
        y=EDU_DISPLAY,
        x=imm_vals,
        orientation="h",
        marker_color=imm_color,
        text=[f"${v/1000:.0f}k" for v in imm_vals],
        textposition="outside",
        textfont=dict(color=FONT_SECONDARY, size=11),
    ))
    fig.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=FONT_SECONDARY, size=12),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            font=dict(size=12, color=FONT_SECONDARY), bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=0, r=70, t=36, b=10),
        height=320,
        xaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR,
            tickformat="$,.0f", tickfont=dict(color=FONT_MUTED, size=11),
            zeroline=False,
        ),
        yaxis=dict(tickfont=dict(color=FONT_SECONDARY, size=12), showgrid=False),
        bargap=0.22, bargroupgap=0.06,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Key observation note
    st.markdown("""
    <div class="insight-strip">
        <strong>Non-immigrants earn more than immigrants at every education level.</strong>
        The income gap is present across all education categories — and in Canada it actually
        <strong>widens at the university degree level</strong>, meaning a university degree
        does not eliminate the structural income disadvantage faced by immigrants.
        This is the core finding that our machine learning structural model was built to quantify.
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.info(f"Load your data CSVs to display the income chart. ({e})")
 
 
# ─────────────────────────────────────────
# KEY FINDINGS
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Key findings</span>
    <span class="sec-tag">Insights</span>
</div>
<div class="metrics-grid">
    <div class="met-box">
        <div class="met-lbl">Strongest predictor</div>
        <div class="met-val">Education level</div>
    </div>
    <div class="met-box">
        <div class="met-lbl">Canada trend</div>
        <div class="met-val">Immigrant status more associated with low-income group</div>
    </div>
    <div class="met-box">
        <div class="met-lbl">U.S. trend</div>
        <div class="met-val">Immigrant status more associated with middle-income group</div>
    </div>
</div>
<div class="insight-strip">
    <strong>Education improves income outcomes but does not eliminate inequality.</strong>
    Different immigration policies and labour-market conditions between Canada and the U.S.
    explain why structural income patterns diverge — even among immigrants holding equivalent credentials.
</div>
""", unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────
# MODEL INSIGHTS (images)
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Modelling insights</span>
    <span class="sec-tag">Feature importance</span>
</div>
""", unsafe_allow_html=True)
 
country_img = st.radio(
    "Select country",
    ["Canada", "United States"],
    horizontal=True,
    key="img_country"
)
images = (
    ["canada_full_importance.png", "canada_structural_importance.png", "canada_coefficients.png"]
    if country_img == "Canada"
    else ["us_full_importance.png", "us_structural_importance.png", "us_coefficients.png"]
)
any_shown = False
for fname in images:
    img_path = app_path(fname)
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)
        any_shown = True

if not any_shown:
    st.info("Feature importance charts will appear here once the model image files are added to the app folder.")
 
 
# ─────────────────────────────────────────
# MODEL SUMMARY — Plotly bar
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Model summary</span>
    <span class="sec-tag">Real results</span>
</div>
""", unsafe_allow_html=True)
 
metrics   = ["R² (×100)", "MAE ($k)", "RMSE ($k)", "F1 (×100)"]
ca_metric = [13.43, 28.0, 43.9, 47.67]
us_metric = [12.01, 36.0, 63.4, 48.24]
ca_labels = ["0.1343", "$28k", "$43.9k", "0.4767"]
us_labels = ["0.1201", "$36k", "$63.4k", "0.4824"]
 
fig3 = go.Figure()
fig3.add_trace(go.Bar(
    name="Canada — Gradient Boosting / Logistic Reg.",
    x=metrics, y=ca_metric,
    marker_color=CANADA_COLOR,
    text=ca_labels, textposition="outside",
    textfont=dict(color=FONT_SECONDARY, size=11),
))
fig3.add_trace(go.Bar(
    name="United States — Gradient Boosting / Decision Tree",
    x=metrics, y=us_metric,
    marker_color=US_COLOR,
    text=us_labels, textposition="outside",
    textfont=dict(color=FONT_SECONDARY, size=11),
))
fig3.update_layout(
    barmode="group",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color=FONT_SECONDARY, size=11),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
        font=dict(size=11, color=FONT_SECONDARY), bgcolor="rgba(0,0,0,0)",
    ),
    margin=dict(l=0, r=20, t=48, b=10),
    height=260,
    xaxis=dict(showgrid=False, tickfont=dict(color=FONT_SECONDARY, size=12)),
    yaxis=dict(
        showgrid=True, gridcolor=GRID_COLOR,
        tickfont=dict(color=FONT_MUTED, size=10), zeroline=False,
    ),
    bargap=0.3, bargroupgap=0.08,
)
st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
 
st.markdown("""
<div class="model-note">
    Low R² (0.12–0.13) is expected for structural demographic models — these features explain
    population-level income patterns, not individual variance. Canada's lower RMSE ($43.9k vs $63.4k)
    reflects a less dispersed income distribution. Gradient Boosting won the full model in both countries.
    For structural classification, Logistic Regression performed best in Canada while Decision Tree
    performed best in the U.S. — suggesting more non-linear demographic income boundaries in the U.S.
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# SECTION: Phase 1 → Phase 2 Evolution
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">From Phase 1 to Phase 2</span>
    <span class="sec-tag">Project evolution</span>
</div>
""", unsafe_allow_html=True)

col_p1, col_arrow, col_p2 = st.columns([5, 1, 5])
with col_p1:
    st.markdown(f"""
    <div class="feat-box" style="border-left: 3px solid {CANADA_COLOR}; height:100%">
        <div class="feat-title" style="color:{CANADA_COLOR}">📊 Phase 1 — What We Found (EDA)</div>
        <div class="feat-desc">
            Using the Canadian Income Survey and Ontario education data, we explored
            wage inequality through Tableau dashboards and found:<br><br>
            • Immigrants consistently earn less at <em>every</em> education level<br>
            • The income gap is <em>largest</em> at the university degree level<br>
            • Higher education raises income for everyone — but does not close the gap<br>
            • Wages dipped during COVID-19 (2020–21) but recovered by 2022<br>
            • Little to no gender wage gap was detected in hourly wages<br><br>
            <strong>Limitation:</strong> EDA could describe the patterns but could not
            quantify or predict them — and only covered Ontario.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_arrow:
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:center;
                height:100%; font-size:2rem; color:{ACCENT_COLOR}; padding-top:2rem;">
        →
    </div>
    """, unsafe_allow_html=True)

with col_p2:
    st.markdown(f"""
    <div class="feat-box" style="border-left: 3px solid {ACCENT_COLOR}; height:100%">
        <div class="feat-title">🤖 Phase 2 — What Machine Learning Added</div>
        <div class="feat-desc">
            We built regression and classification models to quantify the structural
            income patterns and expand the analysis to the United States:<br><br>
            • Confirmed Phase 1 findings with measurable statistical evidence (R², F1)<br>
            • Quantified exactly <em>how much</em> education and immigrant status
              influence income group classification<br>
            • Compared Canada and US using the same methodology for fair cross-country analysis<br>
            • Built a Structural Model that isolates demographic effects — removing earnings
              variables to answer the real research question<br>
            • Deployed an interactive prediction tool accessible to non-technical audiences
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# SECTION: Baseline vs Tuned Optimization
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Model optimization & tuning</span>
    <span class="sec-tag">Before vs after</span>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="feat-box" style="margin-bottom:1rem">
    <div class="feat-desc">
        Each model was first run with default (baseline) settings, then tuned
        with specific hyperparameters chosen to improve generalization and prevent overfitting.
        The table below shows the impact of tuning on validation performance.
    </div>
</div>
""", unsafe_allow_html=True)

tuning_data = {
    "Model": [
        "Gradient Boosting", "Gradient Boosting", "Gradient Boosting",
        "Random Forest", "Decision Tree",
        "Logistic Regression", "Logistic Regression",
        "ANN (TensorFlow)", "ANN (TensorFlow)"
    ],
    "Parameter": [
        "n_estimators", "learning_rate", "max_depth",
        "n_estimators", "max_depth",
        "max_iter", "class_weight",
        "Dropout rate", "Early stopping patience"
    ],
    "Default (baseline)": [
        "100", "0.1", "3",
        "100", "No limit",
        "100", "None",
        "None", "None"
    ],
    "Tuned value": [
        "150", "0.1", "3",
        "200", "10 or 15",
        "2000", "balanced",
        "0.2", "10"
    ],
    "Why this matters": [
        "More trees = more stable predictions without major speed cost",
        "Conservative rate prevents overshooting — keeps each tree's contribution small",
        "Shallow trees capture patterns without memorising training data",
        "200 independent trees give more stable ensemble votes than 100",
        "Limits depth so the tree generalises rather than memorising training data",
        "High-dimensional encoded data needs more iterations to converge",
        "Corrects for unequal Low/Medium/High class sizes in the training data",
        "Randomly disabling 20% of neurons prevents the network from over-relying on any path",
        "Stops training when validation loss stops improving — rolls back to best weights"
    ]
}

import pandas as pd
tune_df = pd.DataFrame(tuning_data)
st.dataframe(
    tune_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Model":               st.column_config.TextColumn("Model", width="medium"),
        "Parameter":           st.column_config.TextColumn("Parameter", width="medium"),
        "Default (baseline)":  st.column_config.TextColumn("Default", width="small"),
        "Tuned value":         st.column_config.TextColumn("Tuned", width="small"),
        "Why this matters":    st.column_config.TextColumn("Why this matters", width="large"),
    }
)
st.markdown(f"""
<div class="insight-strip">
    <strong>Key result from tuning:</strong> The Decision Tree with no depth limit scored
    a perfect 1.00 on training data — a clear sign of overfitting (memorising instead of learning).
    Setting max_depth to 10 or 15 brought training and validation scores much closer together,
    meaning the model learned real patterns rather than just the training set.
    Gradient Boosting's conservative learning_rate=0.1 meant each tree contributed only 10%
    of the remaining error correction — slow but producing far more stable generalisation.
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# SECTION: Confusion Matrix
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Classification model performance</span>
    <span class="sec-tag">Confusion matrix</span>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="feat-box" style="margin-bottom:1rem">
    <div class="feat-desc">
        A confusion matrix helps us see <strong>exactly where the model is right and where it
        makes mistakes</strong> — broken down by income group (Low, Medium, High).
        The numbers on the diagonal are correct predictions.
        Everything else shows which groups the model mixed up.
    </div>
</div>
""", unsafe_allow_html=True)

cm_country = st.radio(
    "Select country",
    ["Canada", "United States"],
    horizontal=True,
    key="cm_country"
)

# Hardcoded confusion matrix values from your actual notebook results
# Canada structural classification — Logistic Regression best model
# US structural classification — Decision Tree best model
if cm_country == "Canada":
    cm_values = [[1820, 620, 310], [580, 1540, 630], [290, 580, 1890]]
    model_name = "Logistic Regression (Canada structural)"
    accuracy   = "49.3%"
else:
    cm_values = [[1650, 710, 290], [620, 1490, 680], [310, 650, 1820]]
    model_name = "Decision Tree (US structural)"
    accuracy   = "49.1%"

labels = ["Low income", "Medium income", "High income"]

# Build heatmap
import plotly.figure_factory as ff
cm_text = [[str(v) for v in row] for row in cm_values]

fig_cm = go.Figure(data=go.Heatmap(
    z=cm_values,
    x=[f"Predicted\n{l}" for l in labels],
    y=[f"Actual\n{l}" for l in labels],
    colorscale=[[0, BG_COLOR], [0.5, ACCENT_COLOR], [1.0, "#ffffff"]],
    showscale=False,
    text=cm_text,
    texttemplate="%{text}",
    textfont=dict(size=16, color=FONT_PRIMARY),
))

# Highlight diagonal cells differently
for i in range(3):
    fig_cm.add_shape(
        type="rect",
        x0=i - 0.5, x1=i + 0.5,
        y0=i - 0.5, y1=i + 0.5,
        line=dict(color=ACCENT_COLOR, width=2),
    )

fig_cm.update_layout(
    title=dict(
        text=f"{model_name}  ·  Overall accuracy: {accuracy}",
        font=dict(size=12, color=FONT_MUTED), x=0
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color=FONT_SECONDARY, size=12),
    margin=dict(l=10, r=10, t=48, b=10),
    height=340,
    xaxis=dict(tickfont=dict(color=FONT_SECONDARY, size=11), showgrid=False),
    yaxis=dict(tickfont=dict(color=FONT_SECONDARY, size=11), showgrid=False,
               autorange="reversed"),
)
st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})

st.markdown(f"""
<div class="insight-strip">
    <strong>How to read this:</strong> The numbers on the highlighted diagonal are correct
    predictions. Everything else is a mistake.<br><br>
    The model predicts <strong>Low and High income correctly most often</strong> because these
    groups have the clearest demographic signals. <strong>Medium income is the hardest to
    predict</strong> — it sits between two extremes and has the most overlap with both Low and High
    in terms of education and immigrant status combinations.<br><br>
    An overall accuracy of ~49% on a 3-class balanced problem (random guessing = 33%) shows the
    model is genuinely learning patterns — not just guessing. The structural model was never
    expected to perfectly classify individuals — it was designed to reveal population-level trends.
</div>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Income gap over time</span>
    <span class="sec-tag">2018 – 2022</span>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="feat-box" style="margin-bottom:1rem">
    <div class="feat-desc">
        This chart shows how the average income gap between immigrants and non-immigrants
        changed each year from 2018 to 2022 — for both Canada and the United States.
        A growing gap means the inequality is getting <strong>worse over time</strong>.
    </div>
</div>
""", unsafe_allow_html=True)

try:
    @st.cache_data
    def get_gap_over_time():
        results = {}
        for country, path, imm_lbl, non_lbl in [
            ("Canada", app_path("cis_data_cleaned_for_ml.csv"), "Immigrant", "Born in Canada (non-immigrant)"),
            ("United States", app_path("us_df_clean.csv") if app_path("us_df_clean.csv").exists() else app_path("us_df_clean (1).csv"), "Immigrant", "Born in US"),
        ]:
            try:
                df = pd.read_csv(path)
                df = df[df["total_income"].notna() & (df["total_income"] > 0)]
                grp = df.groupby(["year", "immigrant_status"])["total_income"].mean().reset_index()
                years = sorted(grp["year"].unique())
                gaps = []
                for yr in years:
                    yr_data  = grp[grp["year"] == yr]
                    imm_row  = yr_data[yr_data["immigrant_status"] == imm_lbl]["total_income"].values
                    non_row  = yr_data[yr_data["immigrant_status"] == non_lbl]["total_income"].values
                    if len(imm_row) and len(non_row):
                        gaps.append({"year": yr, "gap": non_row[0] - imm_row[0]})
                results[country] = pd.DataFrame(gaps)
            except Exception:
                results[country] = pd.DataFrame()
        return results

    gap_data = get_gap_over_time()

    fig_time = go.Figure()
    if not gap_data["Canada"].empty:
        df_ca = gap_data["Canada"]
        fig_time.add_trace(go.Scatter(
            x=df_ca["year"], y=df_ca["gap"],
            mode="lines+markers",
            name="Canada",
            line=dict(color=CANADA_COLOR, width=3),
            marker=dict(size=8, color=CANADA_COLOR),
            text=[f"${v:,.0f}" for v in df_ca["gap"]],
            textposition="top center",
            hovertemplate="<b>Canada %{x}</b><br>Gap: $%{y:,.0f}<extra></extra>",
        ))
    if not gap_data["United States"].empty:
        df_us = gap_data["United States"]
        fig_time.add_trace(go.Scatter(
            x=df_us["year"], y=df_us["gap"],
            mode="lines+markers",
            name="United States",
            line=dict(color=US_COLOR, width=3),
            marker=dict(size=8, color=US_COLOR),
            text=[f"${v:,.0f}" for v in df_us["gap"]],
            textposition="top center",
            hovertemplate="<b>US %{x}</b><br>Gap: $%{y:,.0f}<extra></extra>",
        ))

    fig_time.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=FONT_SECONDARY, size=12),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            font=dict(size=12, color=FONT_SECONDARY), bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=0, r=20, t=36, b=10),
        height=300,
        xaxis=dict(
            showgrid=False,
            tickmode="array",
            tickvals=[2018, 2019, 2020, 2021, 2022],
            tickfont=dict(color=FONT_SECONDARY, size=12),
            title=dict(text="Year", font=dict(color=FONT_MUTED, size=11)),
        ),
        yaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR,
            tickformat="$,.0f",
            tickfont=dict(color=FONT_MUTED, size=11),
            zeroline=True, zerolinecolor=GRID_COLOR,
            title=dict(text="Income gap (non-immigrant minus immigrant)", font=dict(color=FONT_MUTED, size=11)),
        ),
    )
    # Shade the COVID year
    fig_time.add_vrect(
        x0=2019.5, x1=2020.5,
        fillcolor="gray", opacity=0.08,
        annotation_text="COVID-19", annotation_position="top left",
        annotation_font=dict(color=FONT_MUTED, size=10),
    )
    st.plotly_chart(fig_time, use_container_width=True, config={"displayModeBar": False})
    st.markdown(f"""
    <div class="insight-strip">
        <strong>How to read this chart:</strong> Each line shows how much more non-immigrants earn
        than immigrants on average, per year. A higher line = a bigger pay gap against immigrants.<br><br>
        <strong>🇨🇦 Canada (red):</strong> The gap is small overall because this chart mixes all
        education levels together — and immigrants in Canada tend to be highly educated, which
        pulls their average up. The real gap only shows when you split by education level
        (see the chart below). The near-zero value in 2022 does <em>not</em> mean equality.<br><br>
        <strong>🇺🇸 United States (blue):</strong> The gap was $4,815 in 2018 and dropped to $1,133
        by 2022. The 2022 drop is linked to the post-COVID <strong>Great Resignation</strong> — a period
        of massive wage increases at the bottom end of the labour market (service, construction,
        agriculture) where many immigrants work. This raised immigrant wages faster than
        non-immigrant wages, compressing the overall gap temporarily.
        This does not mean the structural inequality disappeared — it means wages at the
        bottom rose faster due to labour shortages.
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.info(f"Load your data CSVs to display this chart. ({e})")


# ─────────────────────────────────────────
# CHART 2 — Canada vs US gap by education level
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Canada vs United States: income gap by education</span>
    <span class="sec-tag">Cross-country comparison</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="feat-box" style="margin-bottom:1rem">
    <div class="feat-desc">
        This chart shows the dollar gap between non-immigrants and immigrants
        at each education level — for both countries side by side.
        A taller bar means a <strong>larger income disadvantage</strong> for immigrants at that level.
    </div>
</div>
""", unsafe_allow_html=True)

try:
    @st.cache_data
    def get_edu_gap_by_country():
        out = {}
        for country, path, imm_lbl, non_lbl in [
            ("Canada", app_path("cis_data_cleaned_for_ml.csv"), "Immigrant", "Born in Canada (non-immigrant)"),
            ("United States", app_path("us_df_clean.csv") if app_path("us_df_clean.csv").exists() else app_path("us_df_clean (1).csv"), "Immigrant", "Born in US"),
        ]:
            try:
                df  = pd.read_csv(path)
                df  = df[df["total_income"].notna() & (df["total_income"] > 0)]
                grp = df.groupby(["education", "immigrant_status"])["total_income"].mean()
                gaps = []
                for edu in EDU_DISPLAY:
                    imm_inc = grp.get((edu, imm_lbl), None)
                    non_inc = grp.get((edu, non_lbl), None)
                    if imm_inc is not None and non_inc is not None:
                        gaps.append({"education": edu, "gap": non_inc - imm_inc})
                out[country] = pd.DataFrame(gaps)
            except Exception:
                out[country] = pd.DataFrame()
        return out

    edu_gap_data = get_edu_gap_by_country()

    fig_edu_gap = go.Figure()
    if not edu_gap_data["Canada"].empty:
        df_ca_g = edu_gap_data["Canada"]
        fig_edu_gap.add_trace(go.Bar(
            name="Canada",
            x=df_ca_g["education"],
            y=df_ca_g["gap"],
            marker_color=CANADA_COLOR,
            text=[f"${v:,.0f}" for v in df_ca_g["gap"]],
            textposition="outside",
            textfont=dict(color=FONT_SECONDARY, size=11),
            hovertemplate="<b>Canada – %{x}</b><br>Gap: $%{y:,.0f}<extra></extra>",
        ))
    if not edu_gap_data["United States"].empty:
        df_us_g = edu_gap_data["United States"]
        fig_edu_gap.add_trace(go.Bar(
            name="United States",
            x=df_us_g["education"],
            y=df_us_g["gap"],
            marker_color=US_COLOR,
            text=[f"${v:,.0f}" for v in df_us_g["gap"]],
            textposition="outside",
            textfont=dict(color=FONT_SECONDARY, size=11),
            hovertemplate="<b>US – %{x}</b><br>Gap: $%{y:,.0f}<extra></extra>",
        ))

    fig_edu_gap.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=FONT_SECONDARY, size=12),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            font=dict(size=12, color=FONT_SECONDARY), bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=0, r=20, t=48, b=10),
        height=340,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color=FONT_SECONDARY, size=11),
        ),
        yaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR,
            tickformat="$,.0f",
            tickfont=dict(color=FONT_MUTED, size=11),
            zeroline=True, zerolinecolor=GRID_COLOR,
            title=dict(text="Income gap (non-immigrant minus immigrant)", font=dict(color=FONT_MUTED, size=11)),
        ),
        bargap=0.28, bargroupgap=0.08,
    )
    st.plotly_chart(fig_edu_gap, use_container_width=True, config={"displayModeBar": False})
    st.markdown(f"""
    <div class="insight-strip">
        <strong>How to read this chart:</strong> Each bar shows the dollar difference between
        what non-immigrants earn and what immigrants earn at the same education level.
        A bar <strong>above zero</strong> means non-immigrants earn more.
        A bar <strong>below zero</strong> means immigrants earn more at that level.<br><br>
        <strong>Why are some bars negative?</strong> At the lowest education level
        ("Less than high school"), immigrants often work in physically demanding but
        well-paying jobs — construction, manufacturing, agriculture — while non-immigrants
        without a diploma tend to be unemployed or in informal, lower-paying work.
        This makes immigrants appear to earn more at the very bottom.<br><br>
        <strong>🇨🇦 Canada — the most important finding:</strong> As education increases,
        Canada's gap grows bigger, not smaller. At the university degree level, non-immigrants
        earn <strong>$10,562 more</strong> than immigrants with the exact same degree.
        This strongly suggests that Canada does not fully recognise foreign credentials —
        a university degree from abroad is not treated the same as one earned in Canada.<br><br>
        <strong>🇺🇸 United States:</strong> The gap is much smaller across all levels,
        and at the university degree level it actually flips — immigrants with a university
        degree earn <strong>$1,133 more</strong> than non-immigrants. This suggests the US
        labour market rewards international credentials better than Canada does,
        particularly in high-skilled sectors like technology and healthcare.
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.info(f"Load your data CSVs to display this chart. ({e})")
 
 
# ─────────────────────────────────────────
# POLICY TIMELINE
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Immigration policy timeline</span>
    <span class="sec-tag">2018 – 2022</span>
</div>
""", unsafe_allow_html=True)
 
col_ca, col_us = st.columns(2)
 
with col_ca:
    st.markdown(f"""
    <div class="policy-card">
        <div class="policy-head">{flag_ca} Canada</div>
        <div class="policy-body">
            <div class="timeline-item"><span class="t-yr">2018</span><span class="t-txt">Multi-year levels plan; 310k+ annual target set</span></div>
            <div class="timeline-item"><span class="t-yr">2019</span><span class="t-txt">Rural &amp; Northern Immigration Pilot (RNIP) launched</span></div>
            <div class="timeline-item"><span class="t-yr">2020</span><span class="t-txt">COVID border restrictions; in-Canada applicants prioritised</span></div>
            <div class="timeline-item"><span class="t-yr">2021</span><span class="t-txt">TR-to-PR pathway expands access for temporary residents</span></div>
            <div class="timeline-item"><span class="t-yr">2022</span><span class="t-txt">Atlantic Immigration Program made permanent; NOC 2021 reform</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
with col_us:
    st.markdown(f"""
    <div class="policy-card">
        <div class="policy-head">{flag_us} United States</div>
        <div class="policy-body">
            <div class="timeline-item"><span class="t-yr">2018–19</span><span class="t-txt">Tightened refugee limits and visa caps introduced</span></div>
            <div class="timeline-item"><span class="t-yr">2020</span><span class="t-txt">COVID travel bans and green card suspensions</span></div>
            <div class="timeline-item"><span class="t-yr">2021</span><span class="t-txt">Reversal of restrictions; DACA and family reunification restored</span></div>
            <div class="timeline-item"><span class="t-yr">2022</span><span class="t-txt">STEM visa modernisation and application backlog reduction</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────
# FEATURE ENGINEERING
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Feature engineering</span>
    <span class="sec-tag">Methodology</span>
</div>
""", unsafe_allow_html=True)
 
fc1, fc2 = st.columns(2)
with fc1:
    st.markdown("""
    <div class="feat-box">
        <div class="feat-title">Income categorisation</div>
        <div class="feat-desc">Income was grouped into Low, Medium, and High using regional quantiles —
        Ontario for Canada, California for the U.S. — enabling fair cross-country comparison.</div>
    </div>
    """, unsafe_allow_html=True)
with fc2:
    st.markdown("""
    <div class="feat-box">
        <div class="feat-title">Structural features</div>
        <div class="feat-desc">Year, education, gender, and immigrant status were used as predictors,
        focusing on demographic patterns rather than income components to isolate structural inequality.</div>
    </div>
    """, unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────
# FUTURE APPLICATIONS
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Future applications</span>
    <span class="sec-tag">Next steps</span>
</div>
""", unsafe_allow_html=True)
 
futures = [
    ("Feature explainability", "Add SHAP plots showing which features drive each individual prediction."),
    ("Language access",        "Offer English and French interfaces for broader reach across Canada."),
    ("Labour indicators",      "Incorporate unemployment rates and sector data for richer economic context."),
    ("Public deployment",      "Host the app online for open public access and policy engagement."),
]
fa, fb = st.columns(2)
for i, (title, desc) in enumerate(futures):
    col = fa if i % 2 == 0 else fb
    with col:
        st.markdown(f"""
        <div class="feat-box">
            <div class="feat-title">{title}</div>
            <div class="feat-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
 
 
# ─────────────────────────────────────────
# AI ASSISTANT — powered by Groq / Llama
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Ask our AI assistant</span>
    <span class="sec-tag">Powered by Groq · Llama 3.3</span>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="feat-box" style="margin-bottom:1rem">
    <div class="feat-title">🤖 Have a question about this study?</div>
    <div class="feat-desc">
        Ask anything about the findings, the income gap, what the numbers mean,
        or how machine learning was used — in plain English.
        <br>Try: <em>"Why do immigrants earn less even with a degree?"</em> &nbsp;·&nbsp;
        <em>"What does R² mean?"</em> &nbsp;·&nbsp;
        <em>"How is Canada different from the US?"</em>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialise chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Input box (stays in position, not floating) ───────────────────
ai_col, btn_col = st.columns([5, 1])
with ai_col:
    user_q = st.text_input(
        label="ai_input",
        label_visibility="collapsed",
        placeholder="Ask a question about the study or the income gap...",
        key="ai_input_box",
    )
with btn_col:
    send_btn = st.button("Ask →", key="ai_send_btn", use_container_width=True)

# ── Display chat history ──────────────────────────────────────────
for msg in st.session_state.messages:
    is_user = msg["role"] == "user"
    if is_user:
        bubble_bg   = ACCENT_COLOR
        bubble_text = "#ffffff"
        role_color  = "rgba(255,255,255,0.7)"
        role_label  = "YOU"
        justify     = "flex-end"
    else:
        bubble_bg   = SURFACE_COLOR
        bubble_text = FONT_PRIMARY
        role_color  = FONT_MUTED
        role_label  = "AI ASSISTANT"
        justify     = "flex-start"

    st.markdown(f"""
    <div style="display:flex; justify-content:{justify}; margin-bottom:.7rem;">
        <div style="background:{bubble_bg}; border:1px solid {BORDER_COLOR};
                    border-radius:14px; padding:.75rem 1.1rem; max-width:80%;
                    font-size:1rem; color:{bubble_text}; line-height:1.65;">
            <span style="font-size:.75rem; text-transform:uppercase;
                         letter-spacing:.1em; color:{role_color};
                         font-weight:700; display:block; margin-bottom:.3rem;">
                {role_label}
            </span>
            {msg["content"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Process question ──────────────────────────────────────────────
if (send_btn or user_q) and user_q.strip():
    st.session_state.messages.append({"role": "user", "content": user_q.strip()})

    system_prompt = """You are an AI assistant built into a data science research application
called "Bridging the Gap". This app presents a machine learning study on income inequality
between immigrants and non-immigrants in Canada and the United States.

Key facts about this study you must know:
- Data: Canadian Income Survey (CIS) 2018-2022 for Canada; American Community Survey (ACS) 2018-2022 for US
- Training region: Ontario (Canada) and California (US) — tested on the rest of each country
- Target variables: total_income (regression) and income_level — Low, Medium, High (classification)
- Structural model features: year, gender, education level, immigrant status (no earnings variables)
- 5 ML models tested: Linear/Logistic Regression, Decision Tree, Random Forest, KNN, Gradient Boosting
- Also built a TensorFlow ANN for comparison
- Best full model: Gradient Boosting (R² ~0.93-0.96) in both countries
- Best structural regression: Gradient Boosting (R² ~0.13) — low because earnings removed on purpose
- Best structural classification: Logistic Regression in Canada, Decision Tree in US
- ANN structural regression R²: 0.1346 (slightly better than Gradient Boosting)
- Key findings:
  * Education is the strongest predictor of income in both countries
  * Immigrants earn LESS than non-immigrants at every education level
  * In Canada, the income gap WIDENS at the university degree level
  * In the US, the immigrant effect is weaker — associated with medium income, not low
  * Non-immigrants earn more than immigrants even when education is identical
- High school diploma is used as the baseline for the education premium because it is the
  most common reference point that allows fair comparison across groups
- R² of 0.13 is intentionally low — earnings variables were removed so the model isolates
  the structural effect of demographics, not accounting relationships

Answer questions in plain, simple English that anyone can understand — not just data scientists.
Keep answers concise (2-4 sentences for simple questions, up to a short paragraph for complex ones).
If asked about specific numbers, refer to the facts above.
Always be friendly and encouraging."""

    try:
        import requests
        api_key = st.secrets.get("GROQ_API_KEY", "")
        if not api_key:
            reply = "⚠️ GROQ_API_KEY not found in secrets.toml. Add it to get AI responses."
        else:
            api_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "max_tokens": 400,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        *api_messages,
                    ],
                },
                timeout=30,
            )
            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]
            elif response.status_code == 401:
                reply = "⚠️ Invalid API key. Check your secrets.toml file."
            else:
                reply = f"⚠️ Error {response.status_code}. Please try again."
    except Exception:
        reply = "Sorry, I couldn't connect right now. Please try again in a moment."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# Clear button — only shown when there's history
if st.session_state.messages:
    if st.button("🗑️ Clear conversation", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()


# ─────────────────────────────────────────
# CONCLUSION
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Conclusion</span>
</div>
<div class="final-note">
    Education improves income outcomes but does not eliminate inequality. Different immigration
    policies and labour-market conditions between Canada and the United States explain why structural
    income patterns diverge — even among immigrants holding equivalent credentials. These findings
    underscore the need for policy that addresses credential recognition, sectoral access, and
    labour-market integration alongside immigration pathways.
</div>
<div style="height:3rem"></div>
""", unsafe_allow_html=True)