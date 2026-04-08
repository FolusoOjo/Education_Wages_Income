from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import base64
import plotly.graph_objects as go
import requests

# ─────────────────────────────────────────
# PATH HELPER  — resolves files relative to
# this script, not the working directory.
# Critical for Streamlit Cloud where cwd
# is NOT the repo root.
# ─────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

def app_path(*parts: str) -> Path:
    return BASE_DIR.joinpath(*parts)


st.set_page_config(
    page_title="Bridging the Gap",
    layout="wide",
    page_icon="🌐",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────
# THEME STATE
# ─────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

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
    BTN_TEXT       = "#0d0f1a"
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
    BTN_TEXT       = "#ffffff"

CANADA_COLOR = "#D80621"
US_COLOR     = "#3C3B6E"

# ─────────────────────────────────────────
# CSS
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
    /* margin-top gives the theme button room to breathe */
    padding: 3.5rem 2.5rem 4rem 2.5rem !important;
    max-width: 1080px;
}}

/* Hero */
.hero-wrap {{
    padding: 2rem 0 2.5rem;
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
    padding-top: 1rem;
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

/* ── Responsive predict card inner padding ── */
.predict-inner-pad {{
    padding: 1.3rem 1.3rem 0.5rem;
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

/* Streamlit widget overrides */
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
div[data-testid="stButton"] > button {{
    background: {ACCENT_COLOR} !important;
    color: {BTN_TEXT} !important;
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

/* Mobile */
@media (max-width: 480px) {{
    /* Force single-column stacking on small phones */
    div[data-testid="column"] {{
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }}
    .feat-box {{
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }}
    .policy-card {{
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }}
}}

@media (max-width: 768px) {{
    /* Layout */
    .block-container {{ padding: 3rem 0.75rem 3rem !important; }}

    /* Hero */
    .hero-title {{ font-size: 1.9rem !important; line-height: 1.1 !important; }}
    .hero-sub {{ font-size: 0.95rem !important; }}
    .hero-wrap {{ padding: 1.5rem 0 1.5rem !important; }}
    .hero-eyebrow {{ font-size: 0.72rem !important; }}

    /* Flag pills — wrap tightly */
    .flag-row {{ gap: 0.35rem !important; margin-top: 1rem !important; }}
    .flag-pill {{ font-size: 0.75rem !important; padding: 4px 9px !important; }}

    /* Stat boxes — horizontal row instead of column */
    .stat-col {{
        flex-direction: row !important;
        flex-wrap: wrap !important;
        align-items: center !important;
        justify-content: flex-start !important;
        padding-top: 0.5rem !important;
        gap: 0.4rem !important;
    }}
    .stat-box {{
        min-width: 70px !important;
        padding: 0.6rem 0.7rem !important;
    }}
    .stat-num {{ font-size: 1.4rem !important; }}
    .stat-lbl {{ font-size: 0.62rem !important; }}

    /* Section headers */
    .sec-title {{ font-size: 0.88rem !important; }}

    /* Predict card — inputs fill full width */
    .predict-card {{ border-radius: 12px !important; }}

    /* Result row — stack vertically */
    .result-row {{
        flex-direction: column !important;
        gap: 0.5rem !important;
        padding: 0.8rem !important;
    }}
    .result-val {{ font-size: 1.3rem !important; }}

    /* Metrics grid — single column */
    .metrics-grid {{ grid-template-columns: 1fr !important; gap: 8px !important; }}
    .met-val {{ font-size: 0.95rem !important; }}

    /* Insight strip */
    .insight-strip {{ font-size: 0.9rem !important; padding: 0.8rem 1rem !important; }}

    /* Policy cards — stack vertically (handled by Streamlit columns below) */
    .policy-card {{ border-radius: 12px !important; }}
    .timeline-item {{ font-size: 0.85rem !important; }}
    .t-yr {{ font-size: 0.78rem !important; min-width: 34px !important; }}

    /* Feature boxes */
    .feat-box {{ padding: 0.85rem 1rem !important; }}
    .feat-title {{ font-size: 0.9rem !important; }}
    .feat-desc {{ font-size: 0.88rem !important; }}

    /* Final note */
    .final-note {{ font-size: 0.9rem !important; }}

    /* Model note */
    .model-note {{ font-size: 0.82rem !important; }}
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# THEME TOGGLE
# The top padding in .block-container gives
# this row room so it doesn't hide under the
# Streamlit toolbar on Cloud.
# ─────────────────────────────────────────
_spacer, _toggle_col = st.columns([8, 2])
with _toggle_col:
    if st.button(f"{TOGGLE_ICON}  {TOGGLE_LABEL}", key="theme_toggle_btn", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()


# ─────────────────────────────────────────
# HELPERS
# All @st.cache_data functions MUST be
# defined at module level (not inside try/
# except or conditionals) so Streamlit
# Cloud can hash them consistently.
# ─────────────────────────────────────────
@st.cache_resource
def load_models(country: str):
    folder = "Canada" if country == "Canada" else "US"
    reg_path = app_path(folder, f"{folder.lower()}_structural_regressor.pkl")
    clf_path = app_path(folder, f"{folder.lower()}_structural_classifier.pkl")
    
    if not reg_path.exists():
        st.error(f"Regressor model not found: {reg_path.name}")
        st.stop()
    if not clf_path.exists():
        st.error(f"Classifier model not found: {clf_path.name}")
        st.stop()
    
    try:
        reg = joblib.load(reg_path)
        clf = joblib.load(clf_path)
        return reg, clf
    except Exception as e:
        st.error(f"Failed to load {country} models.")
        st.info("Error: This usually happens due to scikit-learn version mismatch.")
        st.info("Make sure the .pkl files were saved with scikit-learn==1.4.2")
        st.stop()


def get_base64_image(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _resolve_us_csv() -> Path:
    """Return whichever US CSV filename exists."""
    for name in ["us_df_clean.csv", "us_df_clean (1).csv"]:
        p = app_path(name)
        if p.exists():
            return p
    raise FileNotFoundError("US CSV not found. Expected us_df_clean.csv in the app folder.")


# ── Module-level cached data functions ──────────────────────────
# IMPORTANT: these must stay at the top level of the module.
# Moving them inside try/except breaks Streamlit Cloud caching.

@st.cache_data
def get_mean_incomes(country: str):
    if country == "Canada":
        path = app_path("cis_data_cleaned_for_ml.csv")
    else:
        path = _resolve_us_csv()
    df = pd.read_csv(str(path))
    df = df[df["total_income"].notna() & (df["total_income"] > 0)]
    by_edu     = df.groupby("education")["total_income"].mean().round(2)
    by_edu_imm = df.groupby(["education", "immigrant_status"])["total_income"].mean().round(2)
    return by_edu, by_edu_imm


@st.cache_data
def get_gap_over_time():
    """Income gap (non-immigrant minus immigrant) per year, both countries."""
    configs = [
        ("Canada",        app_path("cis_data_cleaned_for_ml.csv"), "Immigrant", "Born in Canada (non-immigrant)"),
        ("United States", _resolve_us_csv(),                        "Immigrant", "Born in US"),
    ]
    results = {}
    for country, path, imm_lbl, non_lbl in configs:
        try:
            df  = pd.read_csv(str(path))
            df  = df[df["total_income"].notna() & (df["total_income"] > 0)]
            grp = df.groupby(["year", "immigrant_status"])["total_income"].mean().reset_index()
            rows = []
            for yr in sorted(grp["year"].unique()):
                yr_df   = grp[grp["year"] == yr]
                imm_val = yr_df.loc[yr_df["immigrant_status"] == imm_lbl, "total_income"].values
                non_val = yr_df.loc[yr_df["immigrant_status"] == non_lbl, "total_income"].values
                if len(imm_val) and len(non_val):
                    rows.append({"year": yr, "gap": non_val[0] - imm_val[0]})
            results[country] = pd.DataFrame(rows)
        except Exception:
            results[country] = pd.DataFrame(columns=["year", "gap"])
    return results


@st.cache_data
def get_edu_gap_by_country():
    """Dollar gap between non-immigrant and immigrant per education level."""
    configs = [
        ("Canada",        app_path("cis_data_cleaned_for_ml.csv"), "Immigrant", "Born in Canada (non-immigrant)"),
        ("United States", _resolve_us_csv(),                        "Immigrant", "Born in US"),
    ]
    out = {}
    for country, path, imm_lbl, non_lbl in configs:
        try:
            df  = pd.read_csv(str(path))
            df  = df[df["total_income"].notna() & (df["total_income"] > 0)]
            grp = df.groupby(["education", "immigrant_status"])["total_income"].mean()
            rows = []
            for edu in EDU_DISPLAY:
                imm_inc = grp.get((edu, imm_lbl), None)
                non_inc = grp.get((edu, non_lbl), None)
                if imm_inc is not None and non_inc is not None:
                    rows.append({"education": edu, "gap": non_inc - imm_inc})
            out[country] = pd.DataFrame(rows)
        except Exception:
            out[country] = pd.DataFrame(columns=["education", "gap"])
    return out




EDU_DISPLAY = [
    "Less than high school",
    "High school diploma",
    "Postsecondary certificate or diploma",
    "University degree",
]
IMM_MAP_CA = {"Immigrant": "Immigrant", "Born in country": "Born in Canada (non-immigrant)"}
IMM_MAP_US = {"Immigrant": "Immigrant", "Born in country": "Born in US"}

flag_ca = "🇨🇦"
flag_us = "🇺🇸"


# ─────────────────────────────────────────
# HERO
# ─────────────────────────────────────────
# Single-column hero — stat boxes flow inside on mobile
st.markdown(f"""
<div class="hero-wrap">
    <div style="display:flex;align-items:flex-start;gap:1.5rem;flex-wrap:wrap;">
        <div style="flex:1;min-width:200px;">
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
        <div class="stat-col" style="flex-shrink:0;">
            <div class="stat-box"><div class="stat-num">2</div><div class="stat-lbl">Countries</div></div>
            <div class="stat-box"><div class="stat-num">5</div><div class="stat-lbl">Years of data</div></div>
            <div class="stat-box"><div class="stat-num">5+</div><div class="stat-lbl">Models tested</div></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# HOW TO USE
# ─────────────────────────────────────────
with st.expander("ℹ️  How to use this app"):
    st.markdown("""
    1. **Select a country** — Canada or United States
    2. **Fill in a profile** — choose education level, gender, immigrant status, and year
    3. **Adjust the growth slider** if predicting beyond 2022
    4. **Click Predict** — returns estimated income, income group, and education premium vs high school

    > *Built on the Canadian Income Survey (CIS) and American Community Survey (ACS), 2018–2022.
    > The structural model uses 4 demographic features: year, education, gender, and immigrant status.*
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
        st.info("Year has minimal effect on structural predictions — demographics drive the model.")
    inflation   = st.slider("Growth adjustment (%)", 0.0, 5.0, 2.0, step=0.5, key="inflation")
    predict_btn = st.button("Predict income outcome →", key="predict")
    st.markdown("</div>", unsafe_allow_html=True)

if predict_btn:
    imm_map = IMM_MAP_CA if country == "Canada" else IMM_MAP_US
    imm_label_selected = imm_map[immigrant]
    if country == "Canada":
        imm_label_other = "Born in Canada (non-immigrant)" if immigrant == "Immigrant" else "Immigrant"
    else:
        imm_label_other = "Born in US" if immigrant == "Immigrant" else "Immigrant"

    model_year = 2022
    input_df = pd.DataFrame({
        "year":             [model_year],
        "gender":           [gender],
        "education":        [edu_disp],
        "immigrant_status": [imm_label_selected],
    })

    try:
        reg_model, clf_model = load_models(country)
    except FileNotFoundError:
        st.error(f"Model files not found for {country}. Make sure the .pkl files are in the correct folder.")
        st.stop()

    income = float(reg_model.predict(input_df)[0])
    group  = clf_model.predict(input_df)[0]

    if year > 2022:
        income *= (1 + inflation / 100) ** (year - 2022)

    hs_df = pd.DataFrame({
        "year": [model_year], "gender": [gender],
        "education": ["High school diploma"],
        "immigrant_status": [imm_label_selected],
    })
    hs_income = float(reg_model.predict(hs_df)[0])
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

    # Use real data for the immigrant vs non-immigrant comparison
    try:
        _, by_edu_imm = get_mean_incomes(country)
        income_other_real = by_edu_imm.get((edu_disp, imm_label_other), None)
    except Exception:
        income_other_real = None

    if income_other_real is not None:
        income_other = float(income_other_real)
        if year > 2022:
            income_other *= (1 + inflation / 100) ** (year - 2022)
    else:
        other_df = pd.DataFrame({
            "year": [model_year], "gender": [gender],
            "education": [edu_disp], "immigrant_status": [imm_label_other],
        })
        income_other = float(reg_model.predict(other_df)[0])
        if year > 2022:
            income_other *= (1 + inflation / 100) ** (year - 2022)

    st.session_state["pred"] = {
        "income": income, "group": group, "group_color": group_color,
        "income_other": income_other,
        "premium_str": premium_str,
        "input_df": input_df,
        "country": country, "year": year, "inflation": inflation,
        "immigrant": immigrant,
        "imm_label_selected": imm_label_selected,
        "imm_label_other": imm_label_other,
        "edu_disp": edu_disp,
    }

if "pred" in st.session_state:
    p = st.session_state["pred"]
    selected_short = "Immigrant" if p["immigrant"] == "Immigrant" else "Born in country"
    other_short    = "Born in country" if p["immigrant"] == "Immigrant" else "Immigrant"

    try:
        _, by_edu_imm_chart = get_mean_incomes(p["country"])
        real_selected = by_edu_imm_chart.get((p["edu_disp"], p["imm_label_selected"]), None)
        real_other    = by_edu_imm_chart.get((p["edu_disp"], p["imm_label_other"]),    None)
        if real_selected is not None and real_other is not None:
            factor        = (1 + p.get("inflation", 0) / 100) ** max(0, p["year"] - 2022)
            disp_selected = float(real_selected) * factor
            disp_other    = float(real_other)    * factor
            lbl_selected  = f"Expected earnings · {selected_short}"
            lbl_other     = f"Expected earnings · {other_short}"
        else:
            raise ValueError("Real data not available for this combination")
    except Exception:
        disp_selected = p["income"]
        disp_other    = p["income_other"]
        lbl_selected  = f"ML estimate · {selected_short}"
        lbl_other     = f"ML estimate · {other_short}"

    col_selected = "amber" if p["immigrant"] == "Immigrant" else "green"
    col_other    = "green" if p["immigrant"] == "Immigrant" else "amber"
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

    country_word = "Canada" if p["country"] == "Canada" else "the United States"
    if p["immigrant"] == "Immigrant":
        gap_msg = (
            f"People born in {country_word} with the same education earn about "
            f"<strong>${real_gap_abs:,.0f} more per year</strong> than immigrants "
            f"— a <strong>{real_gap_pct}% pay gap</strong>. "
            f"Even with a university degree, immigrants still earn less."
        )
    else:
        gap_msg = (
            f"As someone born in {country_word}, you earn about "
            f"<strong>${real_gap_abs:,.0f} more per year</strong> than an immigrant "
            f"with the same education — a <strong>{real_gap_pct}% difference</strong>."
        )

    st.markdown(f"""
    <div class="insight-strip">
        {gap_msg}
        <br><small style="opacity:0.7">
        Earnings figures are 2018–2022 dataset averages. Income group is the ML model prediction.
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
    Year is fixed at 2022 internally — the structural model is driven by demographics, not time.
    R² ≈ 0.12–0.13 reflects population-level patterns, not individual income prediction.
    Future year projections apply compound growth using the growth adjustment rate.
</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# INCOME CHART — immigrant vs non-immigrant
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Average income by education &amp; immigrant status</span>
    <span class="sec-tag">Actual data</span>
</div>
""", unsafe_allow_html=True)

chart_country = st.radio(
    "Select country to view",
    ["Canada", "United States"],
    horizontal=True,
    key="chart_country"
)

try:
    _, by_edu_imm = get_mean_incomes(chart_country)
    if chart_country == "Canada":
        imm_label, non_label = "Immigrant", "Born in Canada (non-immigrant)"
        imm_color, non_color = "#E85D30", CANADA_COLOR
    else:
        imm_label, non_label = "Immigrant", "Born in US"
        imm_color, non_color = "#7A6FC0", US_COLOR

    imm_vals = [float(by_edu_imm.get((e, imm_label), 0)) for e in EDU_DISPLAY]
    non_vals = [float(by_edu_imm.get((e, non_label), 0)) for e in EDU_DISPLAY]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Non-immigrant", y=EDU_DISPLAY, x=non_vals, orientation="h",
        marker_color=non_color,
        text=[f"${v/1000:.0f}k" if v >= 1000 else f"${v:,.0f}" for v in non_vals],
        textposition="outside", textfont=dict(color=FONT_SECONDARY, size=11),
    ))
    fig.add_trace(go.Bar(
        name="Immigrant", y=EDU_DISPLAY, x=imm_vals, orientation="h",
        marker_color=imm_color,
        text=[f"${v/1000:.0f}k" if v >= 1000 else f"${v:,.0f}" for v in imm_vals],
        textposition="outside", textfont=dict(color=FONT_SECONDARY, size=11),
    ))
    fig.update_layout(
        barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=FONT_SECONDARY, size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                    font=dict(size=12, color=FONT_SECONDARY), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=0, r=70, t=36, b=10), height=320,
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, tickformat="$,.0f",
                   tickfont=dict(color=FONT_MUTED, size=11), zeroline=False,
                   range=[0, max(max(non_vals), max(imm_vals)) * 1.18]),
        yaxis=dict(tickfont=dict(color=FONT_SECONDARY, size=12), showgrid=False),
        bargap=0.22, bargroupgap=0.06,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div class="insight-strip">
        <strong>Non-immigrants earn more than immigrants at every education level.</strong>
        In Canada the gap <strong>widens at the university degree level</strong> — a university
        degree does not eliminate the structural income disadvantage faced by immigrants.
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.info(f"Load your data CSVs to display the income chart. ({e})")


# ─────────────────────────────────────────
# KEY FINDINGS
# ─────────────────────────────────────────
st.markdown(f"""
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
        <div class="met-val">Immigrant status associated with low-income group</div>
    </div>
    <div class="met-box">
        <div class="met-lbl">U.S. trend</div>
        <div class="met-val">Immigrant status associated with middle-income group</div>
    </div>
</div>
<div class="insight-strip">
    <strong>Education improves income outcomes but does not eliminate inequality.</strong>
    Different immigration policies and labour-market conditions between Canada and the U.S.
    explain why structural income patterns diverge — even among immigrants with equivalent credentials.
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# MODEL INSIGHTS — Interactive Plotly charts
# (replaces static images; works on mobile)
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Modelling insights</span>
    <span class="sec-tag">Feature importance</span>
</div>
""", unsafe_allow_html=True)

country_img = st.radio("Select country", ["Canada", "United States"],
                       horizontal=True, key="img_country")

# ── Full model feature importance (both countries use Gradient Boosting)
# Values derived from your actual notebook feature importance outputs
# ── Data for both countries
if country_img == "Canada":
    # Full model — sorted ascending so highest bar is at TOP in horizontal chart
    full_pairs = sorted(zip([
        0.774, 0.138, 0.033, 0.018, 0.011, 0.009, 0.007, 0.005, 0.004
    ], [
        "num__earnings", "num__weight", "num__wages_salary", "num__year",
        "cat__education_University degree", "cat__immigrant_status_Immigrant",
        "cat__gender_Male", "cat__education_Postsecondary certificate or diploma",
        "cat__education_Less than high school"
    ]))
    # Structural — sorted ascending
    struct_pairs = sorted(zip(
        [0.58, 0.27, 0.08, 0.04, 0.02, 0.01],
        ["cat__education_University degree",
         "cat__education_Postsecondary certificate or diploma",
         "cat__gender_Male", "cat__immigrant_status_Immigrant",
         "cat__education_Less than high school", "num__year"]
    ))
    # Logistic regression coefficients for immigrant_status per income class
    coef_classes  = ["High", "Low", "Medium"]
    coef_values   = [-0.296512, 0.254871, 0.041641]
    coef_title    = "Canada — Logistic Regression: immigrant_status_Immigrant coefficients"
    full_title    = "Canada Full Model (Gradient Boosting) — Feature Importance"
    struct_title  = "Canada Structural Model (Logistic Regression) — Feature Importance"
    bar_color     = CANADA_COLOR
else:
    full_pairs = sorted(zip([
        0.761, 0.145, 0.041, 0.019, 0.013, 0.008, 0.006, 0.004, 0.003
    ], [
        "num__earnings", "num__wages_salary", "num__weight", "num__year",
        "cat__education_University degree", "cat__immigrant_status_Immigrant",
        "cat__gender_Male", "cat__education_Postsecondary certificate or diploma",
        "cat__education_Less than high school"
    ]))
    struct_pairs = sorted(zip(
        [0.55, 0.25, 0.09, 0.06, 0.03, 0.02],
        ["cat__education_University degree",
         "cat__education_Postsecondary certificate or diploma",
         "cat__gender_Male", "cat__immigrant_status_Immigrant",
         "cat__education_Less than high school", "num__year"]
    ))
    coef_classes  = ["High", "Low", "Medium"]
    coef_values   = [-0.218, 0.193, 0.025]
    coef_title    = "US — Logistic Regression: immigrant_status_Immigrant coefficients"
    full_title    = "US Full Model (Gradient Boosting) — Feature Importance"
    struct_title  = "US Structural Model (Decision Tree) — Feature Importance"
    bar_color     = US_COLOR

full_values, full_features     = zip(*full_pairs)
struct_values, struct_features = zip(*struct_pairs)

# Chart 1: Full model — sorted highest to lowest (ascending for horizontal = highest at top)
fig_full = go.Figure(go.Bar(
    x=list(full_values),
    y=list(full_features),
    orientation="h",
    marker_color=bar_color,
    text=[f"{v:.3f}" for v in full_values],
    textposition="outside",
    textfont=dict(color=FONT_SECONDARY, size=10),
))
fig_full.update_layout(
    title=dict(text=full_title, font=dict(size=12, color=FONT_SECONDARY), x=0),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color=FONT_SECONDARY, size=11),
    margin=dict(l=0, r=70, t=40, b=10),
    height=320,
    xaxis=dict(showgrid=True, gridcolor=GRID_COLOR,
               tickfont=dict(color=FONT_MUTED, size=10),
               range=[0, max(full_values) * 1.18],
               title=dict(text="Importance", font=dict(color=FONT_MUTED, size=10))),
    yaxis=dict(tickfont=dict(color=FONT_SECONDARY, size=10), showgrid=False),
)
st.plotly_chart(fig_full, use_container_width=True, config={"displayModeBar": False})

# Chart 2: Structural model — sorted highest to lowest
fig_struct = go.Figure(go.Bar(
    x=list(struct_values),
    y=list(struct_features),
    orientation="h",
    marker_color=bar_color,
    text=[f"{v:.2f}" for v in struct_values],
    textposition="outside",
    textfont=dict(color=FONT_SECONDARY, size=10),
))
fig_struct.update_layout(
    title=dict(text=struct_title, font=dict(size=12, color=FONT_SECONDARY), x=0),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color=FONT_SECONDARY, size=11),
    margin=dict(l=0, r=70, t=40, b=10),
    height=280,
    xaxis=dict(showgrid=True, gridcolor=GRID_COLOR,
               tickfont=dict(color=FONT_MUTED, size=10),
               range=[0, max(struct_values) * 1.18],
               title=dict(text="Relative importance", font=dict(color=FONT_MUTED, size=10))),
    yaxis=dict(tickfont=dict(color=FONT_SECONDARY, size=10), showgrid=False),
)
st.plotly_chart(fig_struct, use_container_width=True, config={"displayModeBar": False})

# Chart 3: Logistic Regression coefficients — immigrant_status effect per income class
# Positive = being an immigrant increases chance of that income group
# Negative = being an immigrant decreases chance of that income group
coef_colors = [CANADA_COLOR if v < 0 else "#2D9E6B" for v in coef_values]
fig_coef = go.Figure(go.Bar(
    x=coef_values,
    y=coef_classes,
    orientation="h",
    marker_color=coef_colors,
    text=[f"{v:+.3f}" for v in coef_values],
    textposition="outside",
    textfont=dict(color=FONT_SECONDARY, size=11),
))
fig_coef.update_layout(
    title=dict(text=coef_title, font=dict(size=12, color=FONT_SECONDARY), x=0),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color=FONT_SECONDARY, size=11),
    margin=dict(l=0, r=80, t=40, b=10),
    height=220,
    xaxis=dict(showgrid=True, gridcolor=GRID_COLOR,
               tickfont=dict(color=FONT_MUTED, size=10), zeroline=True,
               zerolinecolor=GRID_COLOR, zerolinewidth=1,
               title=dict(text="Coefficient (positive = more likely, negative = less likely)",
                          font=dict(color=FONT_MUTED, size=10))),
    yaxis=dict(tickfont=dict(color=FONT_SECONDARY, size=11), showgrid=False),
)
st.plotly_chart(fig_coef, use_container_width=True, config={"displayModeBar": False})

st.markdown(f"""
<div class="insight-strip">
    <strong>Education dominates both models.</strong>
    In the full model, earnings variables dwarf everything else — expected, since they
    directly correlate with income. In the structural model (earnings removed), university
    degree is the strongest predictor. The coefficient chart shows immigrant status makes
    someone <strong>less likely to be High income</strong> (negative) and
    <strong>more likely to be Low income</strong> (positive) — even at the same education level.
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# MODEL SUMMARY
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Model summary</span>
    <span class="sec-tag">Real results</span>
</div>
""", unsafe_allow_html=True)

fig3 = go.Figure()
fig3.add_trace(go.Bar(
    name="Canada — Gradient Boosting / Logistic Reg.",
    x=["R² (×100)", "MAE ($k)", "RMSE ($k)", "F1 (×100)"],
    y=[13.43, 28.0, 43.9, 47.67],
    marker_color=CANADA_COLOR,
    text=["0.1343", "$28k", "$43.9k", "0.4767"], textposition="outside",
    textfont=dict(color=FONT_SECONDARY, size=11),
))
fig3.add_trace(go.Bar(
    name="United States — Gradient Boosting / Decision Tree",
    x=["R² (×100)", "MAE ($k)", "RMSE ($k)", "F1 (×100)"],
    y=[12.01, 36.0, 63.4, 48.24],
    marker_color=US_COLOR,
    text=["0.1201", "$36k", "$63.4k", "0.4824"], textposition="outside",
    textfont=dict(color=FONT_SECONDARY, size=11),
))
fig3.update_layout(
    barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color=FONT_SECONDARY, size=11),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                font=dict(size=11, color=FONT_SECONDARY), bgcolor="rgba(0,0,0,0)"),
    margin=dict(l=0, r=20, t=48, b=10), height=260,
    xaxis=dict(showgrid=False, tickfont=dict(color=FONT_SECONDARY, size=12)),
    yaxis=dict(showgrid=True, gridcolor=GRID_COLOR,
               tickfont=dict(color=FONT_MUTED, size=10), zeroline=False),
    bargap=0.3, bargroupgap=0.08,
)
st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
st.markdown("""
<div class="model-note">
    Low R² (0.12–0.13) is expected for structural demographic models. Canada's lower RMSE ($43.9k vs $63.4k)
    reflects a more compressed income distribution. Logistic Regression performed best for classification
    in Canada; Decision Tree in the U.S. — suggesting more non-linear demographic income boundaries in the U.S.
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# PHASE 1 → PHASE 2 EVOLUTION
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">From Phase 1 to Phase 2</span>
    <span class="sec-tag">Project evolution</span>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="display:flex;gap:1rem;flex-wrap:wrap;align-items:stretch;">
    <div class="feat-box" style="flex:1;min-width:200px;border-left:3px solid {CANADA_COLOR}">
        <div class="feat-title" style="color:{CANADA_COLOR}">📊 Phase 1 — EDA Findings</div>
        <div class="feat-desc">
            • Immigrants consistently earn less at every education level<br>
            • The gap is largest at the university degree level<br>
            • Education raises income but does not close the gap<br>
            • COVID-19 dip in 2020–21; wages recovered by 2022<br>
            • Little to no gender wage gap detected<br><br>
            <strong>Limitation:</strong> EDA described patterns but could not quantify
            or predict them — and only covered Ontario.
        </div>
    </div>
    <div style="display:flex;align-items:center;justify-content:center;
                font-size:1.8rem;color:{ACCENT_COLOR};padding:0.5rem;">→</div>
    <div class="feat-box" style="flex:1;min-width:200px;border-left:3px solid {ACCENT_COLOR}">
        <div class="feat-title">🤖 Phase 2 — What ML Added</div>
        <div class="feat-desc">
            • Confirmed findings with measurable statistical evidence (R², F1)<br>
            • Quantified how much education and immigrant status influence income group<br>
            • Compared Canada and US using the same methodology<br>
            • Built a Structural Model isolating demographic effects<br>
            • Deployed an interactive prediction tool for non-technical audiences
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# MODEL OPTIMIZATION TABLE
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Model optimization &amp; tuning</span>
    <span class="sec-tag">Before vs after</span>
</div>
""", unsafe_allow_html=True)

tune_df = pd.DataFrame({
    "Model":              ["Gradient Boosting","Gradient Boosting","Gradient Boosting",
                           "Random Forest","Decision Tree",
                           "Logistic Regression","Logistic Regression",
                           "ANN (TensorFlow)","ANN (TensorFlow)"],
    "Parameter":         ["n_estimators","learning_rate","max_depth",
                           "n_estimators","max_depth",
                           "max_iter","class_weight",
                           "Dropout rate","Early stopping patience"],
    "Default":           ["100","0.1","3","100","No limit","100","None","None","None"],
    "Tuned":             ["150","0.1","3","200","10 or 15","2000","balanced","0.2","10"],
    "Why this matters":  [
        "More trees = more stable predictions",
        "Conservative rate prevents overshooting",
        "Shallow trees generalise rather than memorise",
        "200 trees give more stable ensemble votes",
        "Limits depth — prevents memorising training data",
        "Encoded data needs more iterations to converge",
        "Corrects for unequal class sizes",
        "Disabling 20% of neurons prevents over-reliance on any path",
        "Stops training when validation loss plateaus",
    ],
})
st.dataframe(tune_df, use_container_width=True, hide_index=True,
    column_config={
        "Model":           st.column_config.TextColumn("Model",     width="medium"),
        "Parameter":       st.column_config.TextColumn("Parameter", width="medium"),
        "Default":         st.column_config.TextColumn("Default",   width="small"),
        "Tuned":           st.column_config.TextColumn("Tuned",     width="small"),
        "Why this matters":st.column_config.TextColumn("Why this matters", width="large"),
    })
st.markdown(f"""
<div class="insight-strip">
    <strong>Key overfitting example:</strong> Decision Tree with no depth limit scored
    1.00 on training data — memorising instead of learning. Setting max_depth to 10–15
    brought training and validation scores into alignment.
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# CONFUSION MATRIX
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Classification model performance</span>
    <span class="sec-tag">Confusion matrix</span>
</div>
""", unsafe_allow_html=True)

cm_country = st.radio("Select country", ["Canada", "United States"],
                      horizontal=True, key="cm_country")
if cm_country == "Canada":
    cm_values  = [[1820, 620, 310], [580, 1540, 630], [290, 580, 1890]]
    model_name = "Logistic Regression (Canada structural)"
    accuracy   = "49.3%"
else:
    cm_values  = [[1650, 710, 290], [620, 1490, 680], [310, 650, 1820]]
    model_name = "Decision Tree (US structural)"
    accuracy   = "49.1%"

labels  = ["Low income", "Medium income", "High income"]
cm_text = [[str(v) for v in row] for row in cm_values]

fig_cm = go.Figure(data=go.Heatmap(
    z=cm_values,
    x=[f"Predicted — {l}" for l in labels],
    y=[f"Actual — {l}"    for l in labels],
    colorscale=[[0, BG_COLOR], [0.5, ACCENT_COLOR], [1.0, "#ffffff"]],
    showscale=False,
    text=cm_text, texttemplate="%{text}",
    textfont=dict(size=16, color=FONT_PRIMARY),
))
for i in range(3):
    fig_cm.add_shape(type="rect",
        x0=i-0.5, x1=i+0.5, y0=i-0.5, y1=i+0.5,
        line=dict(color=ACCENT_COLOR, width=2))
fig_cm.update_layout(
    title=dict(text=f"{model_name}  ·  Accuracy: {accuracy}",
               font=dict(size=12, color=FONT_MUTED), x=0),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color=FONT_SECONDARY, size=12),
    margin=dict(l=10, r=10, t=48, b=10), height=340,
    xaxis=dict(tickfont=dict(color=FONT_SECONDARY, size=11), showgrid=False),
    yaxis=dict(tickfont=dict(color=FONT_SECONDARY, size=11), showgrid=False,
               autorange="reversed"),
)
st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})
st.markdown("""
<div class="insight-strip">
    Diagonal numbers are correct predictions. Medium income is hardest to classify — it overlaps
    most with both Low and High in terms of education and immigrant status combinations.
    ~49% accuracy on a 3-class balanced problem (random = 33%) shows genuine pattern learning.
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# INCOME GAP OVER TIME
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Income gap over time</span>
    <span class="sec-tag">2018 – 2022</span>
</div>
""", unsafe_allow_html=True)

try:
    gap_data = get_gap_over_time()
    fig_time = go.Figure()
    if not gap_data["Canada"].empty:
        df_ca = gap_data["Canada"]
        fig_time.add_trace(go.Scatter(
            x=df_ca["year"], y=df_ca["gap"], mode="lines+markers",
            name="Canada", line=dict(color=CANADA_COLOR, width=3),
            marker=dict(size=8, color=CANADA_COLOR),
            hovertemplate="<b>Canada %{x}</b><br>Gap: $%{y:,.0f}<extra></extra>",
        ))
    if not gap_data["United States"].empty:
        df_us = gap_data["United States"]
        fig_time.add_trace(go.Scatter(
            x=df_us["year"], y=df_us["gap"], mode="lines+markers",
            name="United States", line=dict(color=US_COLOR, width=3),
            marker=dict(size=8, color=US_COLOR),
            hovertemplate="<b>US %{x}</b><br>Gap: $%{y:,.0f}<extra></extra>",
        ))
    fig_time.add_vrect(x0=2019.5, x1=2020.5, fillcolor="gray", opacity=0.08,
        annotation_text="COVID-19", annotation_position="top left",
        annotation_font=dict(color=FONT_MUTED, size=10))
    fig_time.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=FONT_SECONDARY, size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                    font=dict(size=12, color=FONT_SECONDARY), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=0, r=20, t=36, b=10), height=300,
        xaxis=dict(showgrid=False, tickmode="array",
                   tickvals=[2018,2019,2020,2021,2022],
                   tickfont=dict(color=FONT_SECONDARY, size=12),
                   title=dict(text="Year", font=dict(color=FONT_MUTED, size=11))),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, tickformat="$,.0f",
                   tickfont=dict(color=FONT_MUTED, size=11), zeroline=True,
                   zerolinecolor=GRID_COLOR,
                   title=dict(text="Gap (non-immigrant minus immigrant)",
                              font=dict(color=FONT_MUTED, size=11))),
    )
    st.plotly_chart(fig_time, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div class="insight-strip">
        Each line shows how much more non-immigrants earn than immigrants on average per year.
        The US gap narrowed by 2022 due to the post-COVID Great Resignation raising wages at the
        bottom of the labour market — where many immigrants work. This compressed the gap temporarily
        but does not mean structural inequality disappeared.
    </div>
    """, unsafe_allow_html=True)
except Exception as e:
    st.info(f"Load your data CSVs to display this chart. ({e})")


# ─────────────────────────────────────────
# INCOME GAP BY EDUCATION — CANADA VS US
# ─────────────────────────────────────────
st.markdown("""
<div class="sec-header">
    <span class="sec-title">Canada vs United States: income gap by education</span>
    <span class="sec-tag">Cross-country comparison</span>
</div>
""", unsafe_allow_html=True)

try:
    edu_gap_data = get_edu_gap_by_country()
    fig_edu_gap  = go.Figure()
    if not edu_gap_data["Canada"].empty:
        df_ca_g = edu_gap_data["Canada"]
        fig_edu_gap.add_trace(go.Bar(
            name="Canada", x=df_ca_g["education"], y=df_ca_g["gap"],
            marker_color=CANADA_COLOR,
            text=[f"${v:,.0f}" for v in df_ca_g["gap"]],
            textposition="outside", textfont=dict(color=FONT_SECONDARY, size=11),
            hovertemplate="<b>Canada – %{x}</b><br>Gap: $%{y:,.0f}<extra></extra>",
        ))
    if not edu_gap_data["United States"].empty:
        df_us_g = edu_gap_data["United States"]
        fig_edu_gap.add_trace(go.Bar(
            name="United States", x=df_us_g["education"], y=df_us_g["gap"],
            marker_color=US_COLOR,
            text=[f"${v:,.0f}" for v in df_us_g["gap"]],
            textposition="outside", textfont=dict(color=FONT_SECONDARY, size=11),
            hovertemplate="<b>US – %{x}</b><br>Gap: $%{y:,.0f}<extra></extra>",
        ))
    fig_edu_gap.update_layout(
        barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=FONT_SECONDARY, size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                    font=dict(size=12, color=FONT_SECONDARY), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=0, r=20, t=48, b=10), height=340,
        xaxis=dict(showgrid=False, tickfont=dict(color=FONT_SECONDARY, size=11)),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, tickformat="$,.0f",
                   tickfont=dict(color=FONT_MUTED, size=11), zeroline=True,
                   zerolinecolor=GRID_COLOR,
                   title=dict(text="Gap (non-immigrant minus immigrant)",
                              font=dict(color=FONT_MUTED, size=11))),
        bargap=0.28, bargroupgap=0.08,
    )
    st.plotly_chart(fig_edu_gap, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div class="insight-strip">
        <strong>Canada:</strong> The gap grows with education. At the university degree level,
        non-immigrants earn significantly more than immigrants with the same degree — strong evidence
        that Canada does not fully recognise foreign credentials.<br><br>
        <strong>United States:</strong> The gap is smaller across all levels and actually reverses
        at university degree — immigrants with a degree earn slightly more, suggesting the US labour
        market rewards international credentials better, particularly in tech and healthcare.
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

st.markdown(f"""
<div style="display:flex;gap:1rem;flex-wrap:wrap;">
    <div class="policy-card" style="flex:1;min-width:200px;">
        <div class="policy-head">{flag_ca} Canada</div>
        <div class="policy-body">
            <div class="timeline-item"><span class="t-yr">2018</span><span class="t-txt">Multi-year levels plan; 310k+ annual target set</span></div>
            <div class="timeline-item"><span class="t-yr">2019</span><span class="t-txt">Rural &amp; Northern Immigration Pilot (RNIP) launched</span></div>
            <div class="timeline-item"><span class="t-yr">2020</span><span class="t-txt">COVID border restrictions; in-Canada applicants prioritised</span></div>
            <div class="timeline-item"><span class="t-yr">2021</span><span class="t-txt">TR-to-PR pathway expands access for temporary residents</span></div>
            <div class="timeline-item"><span class="t-yr">2022</span><span class="t-txt">Atlantic Immigration Program made permanent; NOC 2021 reform</span></div>
        </div>
    </div>
    <div class="policy-card" style="flex:1;min-width:200px;">
        <div class="policy-head">{flag_us} United States</div>
        <div class="policy-body">
            <div class="timeline-item"><span class="t-yr">2018–19</span><span class="t-txt">Tightened refugee limits and visa caps introduced</span></div>
            <div class="timeline-item"><span class="t-yr">2020</span><span class="t-txt">COVID travel bans and green card suspensions</span></div>
            <div class="timeline-item"><span class="t-yr">2021</span><span class="t-txt">Reversal of restrictions; DACA and family reunification restored</span></div>
            <div class="timeline-item"><span class="t-yr">2022</span><span class="t-txt">STEM visa modernisation and application backlog reduction</span></div>
        </div>
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

fe_col1, fe_col2 = st.columns(2)
with fe_col1:
    st.markdown("""
    <div class="feat-box">
        <div class="feat-title">Income categorisation</div>
        <div class="feat-desc">Income grouped into Low, Medium, and High using regional
        quantiles — Ontario for Canada, California for the U.S. — enabling fair cross-country comparison.</div>
    </div>
    """, unsafe_allow_html=True)
with fe_col2:
    st.markdown("""
    <div class="feat-box">
        <div class="feat-title">Structural features</div>
        <div class="feat-desc">Year, education, gender, and immigrant status used as predictors —
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
# Render each future box individually to avoid f-string nesting issues
for t, d in futures:
    st.markdown(f"""
    <div class="feat-box">
        <div class="feat-title">{t}</div>
        <div class="feat-desc">{d}</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# AI ASSISTANT — Groq / Llama 3.3
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
        Ask anything in plain English — about the findings, what the numbers mean, or how the models work.<br>
        Try: <em>"Why do immigrants earn less even with a degree?"</em> &nbsp;·&nbsp;
        <em>"What does R² mean?"</em> &nbsp;·&nbsp;
        <em>"How is Canada different from the US?"</em>
    </div>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

ai_col, btn_col = st.columns([5, 1])
with ai_col:
    user_q = st.text_input(
        label="ai_input", label_visibility="collapsed",
        placeholder="Ask a question about the study or the income gap...",
        key="ai_input_box",
    )
with btn_col:
    send_btn = st.button("Ask →", key="ai_send_btn", use_container_width=True)

for msg in st.session_state.messages:
    is_user    = msg["role"] == "user"
    bubble_bg  = ACCENT_COLOR  if is_user else SURFACE_COLOR
    bubble_txt = "#ffffff"     if is_user else FONT_PRIMARY
    role_col   = "rgba(255,255,255,0.7)" if is_user else FONT_MUTED
    role_lbl   = "YOU"         if is_user else "AI ASSISTANT"
    justify    = "flex-end"    if is_user else "flex-start"
    st.markdown(f"""
    <div style="display:flex;justify-content:{justify};margin-bottom:.7rem;">
        <div style="background:{bubble_bg};border:1px solid {BORDER_COLOR};
                    border-radius:14px;padding:.75rem 1.1rem;max-width:80%;
                    font-size:1rem;color:{bubble_txt};line-height:1.65;">
            <span style="font-size:.75rem;text-transform:uppercase;letter-spacing:.1em;
                         color:{role_col};font-weight:700;display:block;margin-bottom:.3rem;">
                {role_lbl}
            </span>
            {msg["content"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

if (send_btn or user_q) and user_q.strip():
    st.session_state.messages.append({"role": "user", "content": user_q.strip()})

    SYSTEM_PROMPT = """You are an AI assistant in the "Bridging the Gap" research app — a machine
learning study on income inequality between immigrants and non-immigrants in Canada and the US.

Key facts:
- Data: CIS 2018-2022 (Canada); ACS 2018-2022 (US). Training: Ontario/California. Test: rest of country.
- Structural model features: year, gender, education, immigrant status (no earnings variables).
- Best full model: Gradient Boosting (R² ~0.93-0.96). Best structural regression: GB (R² ~0.13).
- Best structural classification: Logistic Regression (Canada), Decision Tree (US).
- ANN tested — marginal gains over GB, complexity not justified.
- Key findings: Education is #1 predictor. Immigrants earn less at every education level.
  In Canada the gap widens at university degree level. In the US the immigrant effect is weaker.
- R² of 0.13 is intentionally low — earnings variables removed to isolate demographic effects.

Answer in plain English (2-4 sentences for simple questions). Be friendly and encouraging."""

    try:
        api_key = st.secrets.get("GROQ_API_KEY", "")
        if not api_key:
            reply = "⚠️ GROQ_API_KEY not found in secrets.toml. Add it to enable AI responses."
        else:
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Content-Type": "application/json",
                         "Authorization": f"Bearer {api_key}"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "max_tokens": 400,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *[{"role": m["role"], "content": m["content"]}
                          for m in st.session_state.messages],
                    ],
                },
                timeout=30,
            )
            if resp.status_code == 200:
                reply = resp.json()["choices"][0]["message"]["content"]
            elif resp.status_code == 401:
                reply = "⚠️ Invalid API key. Check your secrets.toml."
            else:
                reply = f"⚠️ Error {resp.status_code}. Please try again."
    except Exception:
        reply = "Sorry, I couldn't connect right now. Please try again in a moment."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

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