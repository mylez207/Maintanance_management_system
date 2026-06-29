# ══════════════════════════════════════════════════════════════════════════════
# ARUMERU STORMWATER ROAD MAINTENANCE MANAGEMENT SYSTEM
# Developed by: Zahora | Streamlit Application
# ══════════════════════════════════════════════════════════════════════════════

import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
import base64

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Arumeru Road Maintenance System",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a1628 0%, #0d2137 30%, #0f3d2e 65%, #0a2818 100%);
    background-attachment: fixed;
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

/* ── LOGIN ── */
div[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 10px !important;
    color: #111111 !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #27ae60 !important;
    box-shadow: 0 0 0 3px rgba(39,174,96,0.18) !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: #9ca3af !important;
}
div[data-testid="stTextInput"] label {
    color: rgba(255,255,255,0.80) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* ── NUMBER INPUT — dark/black text on white background for clear visibility ── */
div[data-testid="stNumberInput"] input {
    background: #ffffff !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 10px !important;
    color: #000000 !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    text-align: center !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: #27ae60 !important;
    box-shadow: 0 0 0 3px rgba(39,174,96,0.20) !important;
}
div[data-testid="stNumberInput"] label {
    color: rgba(255,255,255,0.75) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}
div[data-testid="stNumberInput"] button {
    background: rgba(39,174,96,0.20) !important;
    border: none !important;
    color: #1a6b3c !important;
}

/* ── BUTTONS ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1a6b3c 0%, #27ae60 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 28px;
    font-size: 14px;
    font-weight: 600;
    width: 100%;
    transition: all 0.2s;
    font-family: 'Inter', sans-serif;
    box-shadow: 0 4px 16px rgba(39,174,96,0.30);
    cursor: pointer;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #27ae60, #2ecc71);
    box-shadow: 0 6px 20px rgba(39,174,96,0.45);
    transform: translateY(-1px);
}

/* ── FILE UPLOADER ── */
div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04) !important;
    border: 2px dashed rgba(39,174,96,0.40) !important;
    border-radius: 14px !important;
    padding: 10px !important;
}
div[data-testid="stFileUploader"] label {
    color: rgba(255,255,255,0.75) !important;
    font-weight: 500 !important;
}

/* ── DATAFRAME ── */
div[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

/* ── ALERTS ── */
.stAlert { border-radius: 10px !important; }

/* ── GLASS CARDS ── */
.glass-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 24px 28px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}
.card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.card-header-icon { font-size: 20px; }
.card-header-title {
    font-family: 'Poppins', sans-serif;
    font-size: 15px;
    font-weight: 600;
    color: #ffffff;
    margin: 0;
}
.card-header-sub {
    font-size: 11.5px;
    color: rgba(255,255,255,0.42);
    margin: 0;
}

/* ── VAR BADGES ── */
.var-badge-hazard {
    display: inline-block;
    background: rgba(231,76,60,0.18);
    border: 1px solid rgba(231,76,60,0.38);
    color: #ff7675;
    font-size: 9.5px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 20px;
    margin-left: 5px;
    vertical-align: middle;
    letter-spacing: 0.3px;
}
.var-badge-protect {
    display: inline-block;
    background: rgba(46,204,113,0.13);
    border: 1px solid rgba(46,204,113,0.33);
    color: #2ecc71;
    font-size: 9.5px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 20px;
    margin-left: 5px;
    vertical-align: middle;
    letter-spacing: 0.3px;
}

/* ── SII RESULT ── */
.sii-result-box {
    border-radius: 16px;
    padding: 28px 24px;
    text-align: center;
    margin: 16px 0;
}
.sii-result-box.very-low  { background: linear-gradient(135deg,#7f1d1d,#991b1b); border:1px solid #dc2626; }
.sii-result-box.low       { background: linear-gradient(135deg,#78350f,#92400e); border:1px solid #d97706; }
.sii-result-box.moderate  { background: linear-gradient(135deg,#713f12,#854d0e); border:1px solid #ca8a04; }
.sii-result-box.high      { background: linear-gradient(135deg,#14532d,#166534); border:1px solid #16a34a; }
.sii-result-box.very-high { background: linear-gradient(135deg,#064e3b,#065f46); border:1px solid #10b981; }

.sii-value {
    font-family: 'Poppins', sans-serif;
    font-size: 60px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 6px;
}
.sii-category { font-size: 19px; font-weight: 600; color: rgba(255,255,255,0.90); margin-bottom:4px; }
.sii-range    { font-size: 12px; color: rgba(255,255,255,0.55); }

/* ── EQUATION BOX ── */
.equation-box {
    background: rgba(0,0,0,0.35);
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 4px solid #27ae60;
    border-radius: 10px;
    padding: 16px 18px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    color: rgba(255,255,255,0.80);
    line-height: 1.9;
    margin: 12px 0;
    overflow-x: auto;
    white-space: pre-wrap;
}

/* ── IMPLEMENTATION TABLE ── */
.impl-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}
.impl-table th {
    background: rgba(39,174,96,0.16);
    color: rgba(255,255,255,0.82);
    padding: 11px 15px;
    text-align: left;
    font-weight: 600;
    font-size: 11.5px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 1px solid rgba(255,255,255,0.10);
}
.impl-table td {
    padding: 11px 15px;
    color: rgba(255,255,255,0.72);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    vertical-align: top;
    line-height: 1.5;
}
.impl-table tr:last-child td { border-bottom: none; }
.impl-table tr:hover td { background: rgba(255,255,255,0.03); }

.level-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 11.5px;
    white-space: nowrap;
}

/* ── EXPANDER ── */
details { border-radius: 10px !important; }
summary { color: rgba(255,255,255,0.70) !important; font-weight:500 !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LOAD MODEL
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
    with open('arumeru_sii_model.pkl', 'rb') as f:
        return pickle.load(f)

try:
    bundle          = load_model()
    model           = bundle['model']
    intercept       = bundle['intercept']
    coefficients    = bundle['coefficients']
    sig_vars        = bundle['sig_vars']
    hazard_vars     = bundle['hazard_vars']
    protective_vars = bundle['protective_vars']
    var_labels      = bundle['var_labels']
    sii_categories  = bundle['sii_categories']
    metrics         = bundle['metrics']
    MODEL_LOADED    = True
except Exception as e:
    MODEL_LOADED = False
    MODEL_ERROR  = str(e)


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
for key, val in [('authenticated', False), ('active_page', 'prediction'),
                 ('last_result', None), ('batch_results', None)]:
    if key not in st.session_state:
        st.session_state[key] = val


# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════
def sii_category_info(sii):
    for lo, hi, cat, rng in sii_categories:
        if lo <= sii < hi:
            return cat, rng
    return 'Very High', '80–100%'

def css_class(cat):
    return {'Very Low':'very-low','Low':'low','Moderate':'moderate',
            'High':'high','Very High':'very-high'}.get(cat, 'moderate')

def recommendation(cat):
    return {
        'Very Low':  '⚡ Emergency reactive repairs — unblock drains and patch critical road failures immediately.',
        'Low':       '🔧 Basic routine maintenance — drain cleaning, gravel replenishment, camber correction.',
        'Moderate':  '🏗️ Preventive maintenance programme — drainage rehabilitation, soil improvement, maintenance scheduling.',
        'High':      '📊 Integrated management — full drain upgrade, soil stabilisation, GIS-based planning.',
        'Very High': '🌿 Optimised system — comprehensive stormwater management with real-time monitoring.',
    }.get(cat, '')

def predict_single(scores: dict) -> dict:
    row     = pd.DataFrame([{v: scores[v] for v in sig_vars}])
    sii_raw = float(model.predict(row)[0])
    sii     = float(np.clip(sii_raw, 0, 100))
    cat, rng = sii_category_info(sii)

    term_vals = [coefficients[v] * scores[v] for v in sig_vars]
    eq1 = f"SII = {intercept:.4f}"
    for v, c, tv in zip(sig_vars, [coefficients[v] for v in sig_vars], term_vals):
        sign = '+' if c >= 0 else '-'
        eq1 += f" {sign} {abs(c):.4f}×{v}({scores[v]})"
    eq2 = f"    = {intercept:.4f} + {sum(term_vals):.4f}"
    eq3 = f"    = {sii_raw:.4f}%  →  SII = {sii:.2f}%"

    return {
        'sii_raw': round(sii_raw, 4), 'sii': round(sii, 2),
        'category': cat, 'range_str': rng,
        'equation': f"{eq1}\n{eq2}\n{eq3}",
        'recommendation': recommendation(cat),
        'css_class': css_class(cat),
        'input_scores': scores,
    }

def predict_batch(df_in: pd.DataFrame) -> pd.DataFrame:
    results = []
    for _, row in df_in.iterrows():
        scores = {v: float(row[v]) for v in sig_vars if v in row}
        missing = [v for v in sig_vars if v not in scores]
        if missing:
            results.append({v: row.get(v, None) for v in df_in.columns} |
                           {'SII (%)': None, 'Category': 'Missing variables', 'Recommendation': ''})
            continue
        r = predict_single(scores)
        base = {v: row.get(v, None) for v in df_in.columns}
        results.append(base | {'SII (%)': r['sii'], 'Category': r['category'],
                                'Recommendation': r['recommendation']})
    return pd.DataFrame(results)

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    out = BytesIO()
    with pd.ExcelWriter(out, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='SII Results')
    return out.getvalue()

def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode('utf-8')


# ══════════════════════════════════════════════════════════════════════════════
# NAVBAR
# ══════════════════════════════════════════════════════════════════════════════
def render_navbar():
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.04);backdrop-filter:blur(16px);
                    border:1px solid rgba(255,255,255,0.10);border-radius:16px;
                    padding:14px 26px;margin-bottom:22px;
                    box-shadow:0 4px 24px rgba(0,0,0,0.30);">
            <div style="display:flex;align-items:center;gap:14px;">
                <span style="font-size:28px;">🛣️</span>
                <div>
                    <div style="font-family:'Poppins',sans-serif;font-size:16px;
                                font-weight:700;color:#fff;">Arumeru Road Maintenance MMS</div>
                    <div style="font-size:11px;color:rgba(255,255,255,0.42);">
                        Stormwater Damage Prediction &amp; Management System · Arumeru District, Tanzania
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="display:flex;justify-content:flex-end;padding-top:6px;">
            <div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);
                        border-radius:50px;padding:8px 18px;display:inline-flex;
                        align-items:center;gap:10px;">
                <div style="width:34px;height:34px;
                            background:linear-gradient(135deg,#2ecc71,#1a8a4a);
                            border-radius:50%;display:flex;align-items:center;
                            justify-content:center;font-size:15px;font-weight:700;color:white;">Z</div>
                <div>
                    <div style="font-size:13px;font-weight:600;color:rgba(255,255,255,0.85);">Zahora</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.35);">Researcher</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE TABS
# ══════════════════════════════════════════════════════════════════════════════
def render_tabs():
    c1, c2, c3 = st.columns(3)
    with c1:
        label = "✅  Model Prediction" if st.session_state.active_page == 'prediction' else "🎯  Model Prediction"
        if st.button(label, use_container_width=True, key="tab_pred"):
            st.session_state.active_page = 'prediction'; st.rerun()
    with c2:
        label = "✅  Evaluation & Implementation" if st.session_state.active_page == 'evaluation' else "📋  Evaluation & Implementation"
        if st.button(label, use_container_width=True, key="tab_eval"):
            st.session_state.active_page = 'evaluation'; st.rerun()
    with c3:
        if st.button("🚪  Logout", use_container_width=True, key="logout"):
            st.session_state.authenticated = False
            st.session_state.last_result   = None
            st.session_state.batch_results = None
            st.session_state.active_page   = 'prediction'
            st.rerun()

    pg = "Model Prediction" if st.session_state.active_page == 'prediction' else "Evaluation & Implementation"
    st.markdown(f"""
    <div style="text-align:center;margin:-8px 0 22px 0;">
        <span style="font-size:11px;color:rgba(255,255,255,0.28);
                     text-transform:uppercase;letter-spacing:1px;">
            Currently viewing: {pg}
        </span>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
def render_login():
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown("""
        <div style="text-align:center;padding:55px 0 28px 0;">
            <div style="font-size:70px;margin-bottom:10px;">🛣️</div>
            <h1 style="font-family:'Poppins',sans-serif;font-size:27px;font-weight:800;
                       color:#ffffff;margin:0 0 6px 0;letter-spacing:-0.4px;">
                Arumeru Road MMS
            </h1>
            <p style="font-size:13px;color:rgba(255,255,255,0.42);margin:0 0 6px 0;">
                Stormwater Road Damage Maintenance Management System
            </p>
            <p style="font-size:10.5px;color:rgba(255,255,255,0.24);margin:0 0 32px 0;
                      text-transform:uppercase;letter-spacing:1.8px;">
                Arumeru District · Tanzania · 2026
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:rgba(255,255,255,0.05);backdrop-filter:blur(20px);
                    border:1px solid rgba(255,255,255,0.11);border-radius:20px;
                    padding:36px 34px 28px 34px;">
            <p style="font-family:'Poppins',sans-serif;font-size:17px;font-weight:600;
                      color:#ffffff;margin:0 0 22px 0;text-align:center;">
                🔐&nbsp; Sign In to Continue
            </p>
        """, unsafe_allow_html=True)

        username = st.text_input("👤  Username", placeholder="Enter username")
        password = st.text_input("🔑  Password", type="password", placeholder="Enter password")

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        if st.button("Sign In  →", use_container_width=True):
            if username == "Zahora" and password == "zahora@2026":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.markdown("""
                <div style="background:rgba(220,38,38,0.14);border:1px solid rgba(220,38,38,0.35);
                            border-radius:10px;padding:11px 16px;margin-top:10px;text-align:center;
                            color:#fca5a5;font-size:13px;font-weight:500;">
                    ❌&nbsp; Invalid username or password. Please try again.
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("""
        <p style="text-align:center;font-size:10.5px;color:rgba(255,255,255,0.18);
                  margin-top:22px;">
            University Research System · 2026
        </p>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — MODEL PREDICTION
# ══════════════════════════════════════════════════════════════════════════════
def render_prediction():

    st.markdown("""
    <div style="margin-bottom:20px;">
        <h2 style="font-family:'Poppins',sans-serif;font-size:21px;font-weight:700;
                   color:#ffffff;margin:0 0 4px 0;">
            🎯  Sustainability Improvement Index — Prediction
        </h2>
        <p style="font-size:12.5px;color:rgba(255,255,255,0.42);margin:0;">
            Enter Likert-scale ratings (1–5) manually for each factor, or upload a file for batch prediction.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Likert legend ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);
                border-radius:11px;padding:12px 18px;margin-bottom:20px;
                display:flex;flex-wrap:wrap;gap:16px;align-items:center;">
        <span style="font-size:11.5px;font-weight:700;color:rgba(255,255,255,0.50);
                     text-transform:uppercase;letter-spacing:0.5px;">Likert Scale:</span>
        <span style="font-size:12px;color:rgba(255,255,255,0.68);">1 = Strongly Disagree</span>
        <span style="font-size:12px;color:rgba(255,255,255,0.68);">2 = Disagree</span>
        <span style="font-size:12px;color:rgba(255,255,255,0.68);">3 = Neutral</span>
        <span style="font-size:12px;color:rgba(255,255,255,0.68);">4 = Agree</span>
        <span style="font-size:12px;color:rgba(255,255,255,0.68);">5 = Strongly Agree</span>
    </div>
    """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # MANUAL INPUT SECTION
    # ════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="glass-card">
        <div class="card-header">
            <span class="card-header-icon">✍️</span>
            <div>
                <p class="card-header-title">Manual Input — Enter Scores</p>
                <p class="card-header-sub">Type a value from 1 to 5 for each factor below</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── HAZARD VARIABLES — horizontal row ────────────────────────────────────
    st.markdown("""
    <p style="font-size:12px;font-weight:700;color:#ff7675;text-transform:uppercase;
              letter-spacing:0.8px;margin:0 0 10px 0;">
        ⚠️  Stormwater Hazard Factors
        <span style="font-size:11px;font-weight:400;color:rgba(255,255,255,0.38);
                     text-transform:none;letter-spacing:0;">
         — higher severity reduces SII (β &lt; 0)
        </span>
    </p>
    """, unsafe_allow_html=True)

    haz_cols = st.columns(3)
    hazard_inputs = {}

    with haz_cols[0]:
        st.markdown('<p style="font-size:12px;color:rgba(255,255,255,0.75);margin-bottom:4px;font-weight:500;">V1: Rainfall Intensity <span class="var-badge-hazard">HAZARD β−</span></p>', unsafe_allow_html=True)
        hazard_inputs['V1'] = st.number_input("V1", min_value=1, max_value=5, value=3,
                                               step=1, key="ni_v1", label_visibility="collapsed",
                                               help="Rainfall Intensity — 1=Very Low, 5=Very High severity")

    with haz_cols[1]:
        st.markdown('<p style="font-size:12px;color:rgba(255,255,255,0.75);margin-bottom:4px;font-weight:500;">V2: Seasonal Rainfall Concentration <span class="var-badge-hazard">HAZARD β−</span></p>', unsafe_allow_html=True)
        hazard_inputs['V2'] = st.number_input("V2", min_value=1, max_value=5, value=3,
                                               step=1, key="ni_v2", label_visibility="collapsed",
                                               help="Seasonal Rainfall Concentration — 1=Very Low, 5=Very High")

    with haz_cols[2]:
        st.markdown('<p style="font-size:12px;color:rgba(255,255,255,0.75);margin-bottom:4px;font-weight:500;">V3: Stormwater Runoff Speed <span class="var-badge-hazard">HAZARD β−</span></p>', unsafe_allow_html=True)
        hazard_inputs['V3'] = st.number_input("V3", min_value=1, max_value=5, value=3,
                                               step=1, key="ni_v3", label_visibility="collapsed",
                                               help="Stormwater Runoff Speed — 1=Very Low, 5=Very High")

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # ── PROTECTIVE VARIABLES — horizontal rows ────────────────────────────────
    st.markdown("""
    <p style="font-size:12px;font-weight:700;color:#2ecc71;text-transform:uppercase;
              letter-spacing:0.8px;margin:0 0 10px 0;">
        ✅  Protective &amp; Maintenance Factors
        <span style="font-size:11px;font-weight:400;color:rgba(255,255,255,0.38);
                     text-transform:none;letter-spacing:0;">
         — higher performance increases SII (β &gt; 0)
        </span>
    </p>
    """, unsafe_allow_html=True)

    prot_row1 = st.columns(3)
    prot_row2 = st.columns(2)
    protect_inputs = {}

    with prot_row1[0]:
        st.markdown('<p style="font-size:12px;color:rgba(255,255,255,0.75);margin-bottom:4px;font-weight:500;">V4: Subgrade Bearing Capacity (CBR) <span class="var-badge-protect">PROTECTIVE β+</span></p>', unsafe_allow_html=True)
        protect_inputs['V4'] = st.number_input("V4", min_value=1, max_value=5, value=3,
                                                step=1, key="ni_v4", label_visibility="collapsed",
                                                help="CBR Value — 1=Very Poor, 5=Excellent")

    with prot_row1[1]:
        st.markdown('<p style="font-size:12px;color:rgba(255,255,255,0.75);margin-bottom:4px;font-weight:500;">V7: Side Drain Condition &amp; Functionality <span class="var-badge-protect">PROTECTIVE β+</span></p>', unsafe_allow_html=True)
        protect_inputs['V7'] = st.number_input("V7", min_value=1, max_value=5, value=3,
                                                step=1, key="ni_v7", label_visibility="collapsed",
                                                help="Side Drain Condition — 1=Very Poor, 5=Excellent")

    with prot_row1[2]:
        st.markdown('<p style="font-size:12px;color:rgba(255,255,255,0.75);margin-bottom:4px;font-weight:500;">V8: Cross-Drainage Structure Capacity <span class="var-badge-protect">PROTECTIVE β+</span></p>', unsafe_allow_html=True)
        protect_inputs['V8'] = st.number_input("V8", min_value=1, max_value=5, value=3,
                                                step=1, key="ni_v8", label_visibility="collapsed",
                                                help="Cross-Drainage Capacity — 1=Very Poor, 5=Excellent")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    with prot_row2[0]:
        st.markdown('<p style="font-size:12px;color:rgba(255,255,255,0.75);margin-bottom:4px;font-weight:500;">V13: Routine Preventive Maintenance Coverage <span class="var-badge-protect">PROTECTIVE β+</span></p>', unsafe_allow_html=True)
        protect_inputs['V13'] = st.number_input("V13", min_value=1, max_value=5, value=3,
                                                 step=1, key="ni_v13", label_visibility="collapsed",
                                                 help="Routine Maintenance Coverage — 1=Very Low, 5=Very High")

    with prot_row2[1]:
        st.markdown('<p style="font-size:12px;color:rgba(255,255,255,0.75);margin-bottom:4px;font-weight:500;">V14: Maintenance Budget Adequacy &amp; Allocation <span class="var-badge-protect">PROTECTIVE β+</span></p>', unsafe_allow_html=True)
        protect_inputs['V14'] = st.number_input("V14", min_value=1, max_value=5, value=3,
                                                 step=1, key="ni_v14", label_visibility="collapsed",
                                                 help="Budget Adequacy — 1=Very Inadequate, 5=Very Adequate")

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── Predict button ────────────────────────────────────────────────────────
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        if st.button("🔍  Predict Sustainability Improvement Index", use_container_width=True):
            all_inputs = {**hazard_inputs, **protect_inputs}
            st.session_state.last_result = predict_single(all_inputs)
            st.rerun()

    # ── RESULT DISPLAY ────────────────────────────────────────────────────────
    if st.session_state.last_result:
        r = st.session_state.last_result
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        res_l, res_r = st.columns([1, 1], gap="large")

        with res_l:
            # SII Box
            st.markdown(f"""
            <div class="sii-result-box {r['css_class']}">
                <div style="font-size:12px;font-weight:600;color:rgba(255,255,255,0.50);
                            text-transform:uppercase;letter-spacing:1.8px;margin-bottom:8px;">
                    Sustainability Improvement Index
                </div>
                <div class="sii-value">{r['sii']:.1f}
                    <span style="font-size:30px;font-weight:400;">%</span>
                </div>
                <div class="sii-category">{r['category']}</div>
                <div class="sii-range">Implementation Range: {r['range_str']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Recommendation
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                        border-left:4px solid #27ae60;border-radius:10px;
                        padding:14px 16px;margin:14px 0;">
                <p style="font-size:10.5px;font-weight:700;color:rgba(255,255,255,0.40);
                           text-transform:uppercase;letter-spacing:0.5px;margin:0 0 5px 0;">
                    Recommended Strategy
                </p>
                <p style="font-size:13px;color:rgba(255,255,255,0.82);margin:0;line-height:1.6;">
                    {r['recommendation']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Download single result
            single_df = pd.DataFrame([{
                'V1': r['input_scores'].get('V1'), 'V2': r['input_scores'].get('V2'),
                'V3': r['input_scores'].get('V3'), 'V4': r['input_scores'].get('V4'),
                'V7': r['input_scores'].get('V7'), 'V8': r['input_scores'].get('V8'),
                'V13': r['input_scores'].get('V13'), 'V14': r['input_scores'].get('V14'),
                'SII (%)': r['sii'], 'Category': r['category'],
                'Recommendation': r['recommendation'],
            }])

            dl_c1, dl_c2 = st.columns(2)
            with dl_c1:
                st.download_button(
                    label="⬇️  Download CSV",
                    data=to_csv_bytes(single_df),
                    file_name="sii_prediction_result.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            with dl_c2:
                st.download_button(
                    label="⬇️  Download Excel",
                    data=to_excel_bytes(single_df),
                    file_name="sii_prediction_result.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

        with res_r:
            # Gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=r['sii'],
                number={'suffix': "%", 'font': {'size': 34, 'color': 'white', 'family': 'Poppins'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1,
                             'tickcolor': 'rgba(255,255,255,0.3)',
                             'tickfont': {'color': 'rgba(255,255,255,0.45)', 'size': 10}},
                    'bar':  {'color': '#27ae60', 'thickness': 0.26},
                    'bgcolor': 'rgba(0,0,0,0)', 'borderwidth': 0,
                    'steps': [
                        {'range': [0,  20],  'color': 'rgba(127,29,29,0.55)'},
                        {'range': [20, 40],  'color': 'rgba(120,53,15,0.55)'},
                        {'range': [40, 60],  'color': 'rgba(113,63,18,0.55)'},
                        {'range': [60, 80],  'color': 'rgba(20,83,45,0.55)'},
                        {'range': [80, 100], 'color': 'rgba(6,78,59,0.55)'},
                    ],
                    'threshold': {'line': {'color': '#fff', 'width': 3},
                                  'thickness': 0.85, 'value': r['sii']}
                },
                title={'text': "SII Gauge", 'font': {'color': 'rgba(255,255,255,0.45)', 'size': 12}}
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=220, margin=dict(l=20, r=20, t=28, b=10), font={'color': 'white'},
            )
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

            # Radar chart
            iv  = [r['input_scores'][v] for v in sig_vars]
            fig_radar = go.Figure(go.Scatterpolar(
                r=iv + [iv[0]], theta=sig_vars + [sig_vars[0]],
                fill='toself', fillcolor='rgba(39,174,96,0.16)',
                line=dict(color='#27ae60', width=2),
                marker=dict(size=6, color='#27ae60'),
            ))
            fig_radar.update_layout(
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, range=[0,5],
                                   tickfont=dict(color='rgba(255,255,255,0.35)', size=8),
                                   gridcolor='rgba(255,255,255,0.08)',
                                   linecolor='rgba(255,255,255,0.08)'),
                    angularaxis=dict(tickfont=dict(color='rgba(255,255,255,0.60)', size=10),
                                     linecolor='rgba(255,255,255,0.12)',
                                     gridcolor='rgba(255,255,255,0.06)'),
                ),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=250, margin=dict(l=28, r=28, t=36, b=16), showlegend=False,
                title=dict(text="Input Factor Profile",
                           font=dict(color='rgba(255,255,255,0.50)', size=11)),
            )
            st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

            # Equation expander
            with st.expander("🧮  View Equation Breakdown"):
                st.markdown(f'<div class="equation-box">{r["equation"]}</div>',
                            unsafe_allow_html=True)
                coef_df = pd.DataFrame({
                    'Variable': sig_vars,
                    'Factor': [var_labels[v] for v in sig_vars],
                    'Score': [r['input_scores'][v] for v in sig_vars],
                    'β': [round(coefficients[v], 4) for v in sig_vars],
                    'Contribution': [round(coefficients[v]*r['input_scores'][v], 4) for v in sig_vars],
                    'Type': ['⚠️ Hazard' if v in hazard_vars else '✅ Protective' for v in sig_vars],
                })
                st.dataframe(coef_df, use_container_width=True, hide_index=True,
                             column_config={
                                 'β':            st.column_config.NumberColumn(format="%.4f"),
                                 'Contribution': st.column_config.NumberColumn(format="%.4f"),
                             })

    # ════════════════════════════════════════════════════════════════════════
    # BATCH UPLOAD SECTION
    # ════════════════════════════════════════════════════════════════════════
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
        <div class="card-header">
            <span class="card-header-icon">📂</span>
            <div>
                <p class="card-header-title">Batch Prediction — Upload File</p>
                <p class="card-header-sub">
                    Upload CSV or Excel file containing columns: V1, V2, V3, V4, V7, V8, V13, V14
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Template download
    template_df = pd.DataFrame(columns=['V1','V2','V3','V4','V7','V8','V13','V14'])
    sample_rows = [
        {'V1':4,'V2':4,'V3':3,'V4':3,'V7':3,'V8':3,'V13':4,'V14':4},
        {'V1':2,'V2':2,'V3':2,'V4':4,'V7':4,'V8':4,'V13':4,'V14':4},
        {'V1':3,'V2':3,'V3':3,'V4':3,'V7':3,'V8':3,'V13':3,'V14':3},
    ]
    template_df = pd.DataFrame(sample_rows)

    tc1, tc2, _ = st.columns([1, 1, 2])
    with tc1:
        st.download_button(
            label="📥  Download CSV Template",
            data=to_csv_bytes(template_df),
            file_name="sii_input_template.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with tc2:
        st.download_button(
            label="📥  Download Excel Template",
            data=to_excel_bytes(template_df),
            file_name="sii_input_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload your data file (CSV or Excel)",
        type=["csv", "xlsx", "xls"],
        help="File must contain columns: V1, V2, V3, V4, V7, V8, V13, V14 with values 1–5",
    )

    if uploaded:
        try:
            if uploaded.name.endswith('.csv'):
                df_up = pd.read_csv(uploaded)
            else:
                df_up = pd.read_excel(uploaded)

            st.markdown(f"""
            <div style="background:rgba(39,174,96,0.10);border:1px solid rgba(39,174,96,0.30);
                        border-radius:10px;padding:10px 16px;margin:10px 0;font-size:13px;
                        color:rgba(255,255,255,0.80);">
                ✅  File loaded: <strong>{uploaded.name}</strong> —
                {len(df_up)} rows × {len(df_up.columns)} columns
            </div>
            """, unsafe_allow_html=True)

            missing_cols = [v for v in sig_vars if v not in df_up.columns]
            if missing_cols:
                st.error(f"⚠️  Missing required columns: {missing_cols}")
            else:
                st.markdown("**Preview of uploaded data:**")
                st.dataframe(df_up.head(5), use_container_width=True, hide_index=True)

                if st.button("🚀  Run Batch Prediction", use_container_width=True):
                    with st.spinner("Running predictions..."):
                        batch_df = predict_batch(df_up)
                        st.session_state.batch_results = batch_df
                    st.rerun()

        except Exception as e:
            st.error(f"❌  Error reading file: {e}")

    # ── Batch results ─────────────────────────────────────────────────────────
    if st.session_state.batch_results is not None:
        br = st.session_state.batch_results
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:rgba(39,174,96,0.09);border:1px solid rgba(39,174,96,0.28);
                    border-radius:12px;padding:14px 18px;margin-bottom:14px;">
            <span style="font-size:13.5px;font-weight:600;color:rgba(255,255,255,0.85);">
                📊 Batch Results — {len(br)} predictions completed
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(br, use_container_width=True, hide_index=True,
                     column_config={
                         'SII (%)': st.column_config.ProgressColumn(
                             min_value=0, max_value=100, format="%.2f%%"),
                     })

        bc1, bc2 = st.columns(2)
        with bc1:
            st.download_button(
                label="⬇️  Download Batch Results CSV",
                data=to_csv_bytes(br),
                file_name="sii_batch_results.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with bc2:
            st.download_button(
                label="⬇️  Download Batch Results Excel",
                data=to_excel_bytes(br),
                file_name="sii_batch_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — EVALUATION & IMPLEMENTATION  (figures and RII summary removed)
# ══════════════════════════════════════════════════════════════════════════════
def render_evaluation():

    st.markdown("""
    <div style="margin-bottom:20px;">
        <h2 style="font-family:'Poppins',sans-serif;font-size:21px;font-weight:700;
                   color:#ffffff;margin:0 0 4px 0;">
            📋  Evaluation &amp; Implementation Framework
        </h2>
        <p style="font-size:12.5px;color:rgba(255,255,255,0.42);margin:0;">
            Implementation guidelines and maintenance strategies based on predicted SII levels.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── REGRESSION EQUATION ───────────────────────────────────────────────────
    st.markdown("""
    <div class="glass-card">
        <div class="card-header">
            <span class="card-header-icon">🧮</span>
            <div>
                <p class="card-header-title">Corrected Regression Equation</p>
                <p class="card-header-sub">
                    Hazard variables carry negative β (reduce SII) · Protective variables carry positive β (increase SII)
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    int_val   = round(float(intercept), 4)
    eq_parts  = []
    for v in sig_vars:
        c    = coefficients[v]
        sign = '+' if c >= 0 else '−'
        eq_parts.append(f"{sign} {abs(c):.4f} · {v}")
    eq_display = f"SII (%) = {int_val}  " + "  ".join(eq_parts)

    st.markdown(f"""
    <div class="equation-box" style="font-size:13.5px;text-align:center;padding:20px 24px;">
        {eq_display}
    </div>
    <div style="display:flex;gap:24px;justify-content:center;
                margin:8px 0 18px 0;flex-wrap:wrap;">
        <span style="font-size:12px;color:rgba(255,255,255,0.48);">
            <span style="color:#ff7675;font-weight:700;">⚠️ Hazard (β &lt; 0):</span>
            V1, V2, V3 — higher severity reduces SII
        </span>
        <span style="font-size:12px;color:rgba(255,255,255,0.48);">
            <span style="color:#2ecc71;font-weight:700;">✅ Protective (β &gt; 0):</span>
            V4, V7, V8, V13, V14 — higher performance increases SII
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── IMPLEMENTATION FRAMEWORK ──────────────────────────────────────────────
    st.markdown("""
    <div class="glass-card" style="margin-top:6px;">
        <div class="card-header">
            <span class="card-header-icon">📋</span>
            <div>
                <p class="card-header-title">Maintenance Implementation Framework</p>
                <p class="card-header-sub">
                    Recommended maintenance strategies based on SII prediction level
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    impl_data = [
        {
            'Level': 'Very Low', 'SII': '0 – 20%', 'Likert': '≈ 1',
            'Color': ('#7f1d1d','#fca5a5'),
            'Strategy': 'Emergency Reactive Repairs',
            'Actions': (
                'Immediately unblock all drainage structures and culverts. '
                'Patch critical road surface failures and ruts. '
                'Install emergency slope protection measures. '
                'No systematic preventive planning in place — require urgent intervention.'
            ),
        },
        {
            'Level': 'Low', 'SII': '20 – 40%', 'Likert': '≈ 2',
            'Color': ('#78350f','#fcd34d'),
            'Strategy': 'Basic Routine Maintenance',
            'Actions': (
                'Regular periodic cleaning of side drains and cross-drainage structures. '
                'Replenish gravel wearing course on damaged sections. '
                'Carry out basic camber and cross-slope corrections. '
                'Initiate rainfall monitoring and road condition recording.'
            ),
        },
        {
            'Level': 'Moderate', 'SII': '40 – 60%', 'Likert': '≈ 3',
            'Color': ('#713f12','#fde68a'),
            'Strategy': 'Systematic Preventive Maintenance',
            'Actions': (
                'Implement structured drainage rehabilitation programme. '
                'Carry out subgrade soil improvement to increase CBR values. '
                'Develop and follow a maintenance scheduling system. '
                'Train maintenance staff and build institutional capacity.'
            ),
        },
        {
            'Level': 'High', 'SII': '60 – 80%', 'Likert': '≈ 4',
            'Color': ('#14532d','#86efac'),
            'Strategy': 'Integrated Proactive Management',
            'Actions': (
                'Undertake full upgrade of side drain and cross-drainage network. '
                'Apply soil stabilisation techniques on high-risk road sections. '
                'Optimise maintenance budget allocation using performance data. '
                'Implement GIS-based road maintenance planning and monitoring.'
            ),
        },
        {
            'Level': 'Very High', 'SII': '80 – 100%', 'Likert': '≈ 5',
            'Color': ('#064e3b','#6ee7b7'),
            'Strategy': 'Optimised Sustainability Management',
            'Actions': (
                'Deploy comprehensive stormwater management system across the network. '
                'Establish real-time road condition and rainfall monitoring. '
                'Engage community participation in maintenance activities. '
                'Implement long-term road asset management plan for sustainability.'
            ),
        },
    ]

    st.markdown("""
    <table class="impl-table">
        <thead>
            <tr>
                <th style="width:110px;">Level</th>
                <th style="width:100px;">SII Range</th>
                <th style="width:80px;">Likert</th>
                <th style="width:220px;">Strategy</th>
                <th>Key Actions</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)

    for row in impl_data:
        bg, fg = row['Color']
        badge  = (f'<span class="level-badge" '
                  f'style="background:{bg};color:{fg};">{row["Level"]}</span>')
        st.markdown(
            f"<tr>"
            f"<td>{badge}</td>"
            f"<td style='font-weight:700;color:rgba(255,255,255,0.88);'>{row['SII']}</td>"
            f"<td style='color:rgba(255,255,255,0.55);'>{row['Likert']}</td>"
            f"<td style='color:#a7f3d0;font-weight:600;'>{row['Strategy']}</td>"
            f"<td style='color:rgba(255,255,255,0.72);'>{row['Actions']}</td>"
            f"</tr>",
            unsafe_allow_html=True,
        )

    st.markdown("</tbody></table>", unsafe_allow_html=True)

    # ── SCENARIO TABLE (table only — chart removed) ──────────────────────────
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
        <div class="card-header">
            <span class="card-header-icon">🔭</span>
            <div>
                <p class="card-header-title">Scenario Analysis</p>
                <p class="card-header-sub">
                    Predicted SII when all significant variables are set to the same Likert score
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    scenario_rows = []
    for sv in [1, 2, 3, 4, 5]:
        inp = {v: sv for v in sig_vars}
        sii = float(np.clip(model.predict(pd.DataFrame([inp]))[0], 0, 100))
        cat, rng = sii_category_info(sii)
        scenario_rows.append({
            'All Variables =': sv,
            'Predicted SII (%)': f"{sii:.2f}%",
            'Category': cat,
            'SII Range': rng,
            'Recommended Strategy': [
                'Emergency Reactive Repairs',
                'Basic Routine Maintenance',
                'Systematic Preventive Maintenance',
                'Integrated Proactive Management',
                'Optimised Sustainability Management',
            ][sv - 1],
        })

    sc_df = pd.DataFrame(scenario_rows)
    st.dataframe(sc_df, use_container_width=True, hide_index=True)

    # Download implementation guide
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    impl_dl = pd.DataFrame([{
        'Level': r['Level'], 'SII Range': r['SII'], 'Likert': r['Likert'],
        'Strategy': r['Strategy'], 'Key Actions': r['Actions'],
    } for r in impl_data])

    ic1, ic2, _ = st.columns([1, 1, 2])
    with ic1:
        st.download_button(
            label="⬇️  Download Framework CSV",
            data=to_csv_bytes(impl_dl),
            file_name="implementation_framework.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with ic2:
        st.download_button(
            label="⬇️  Download Framework Excel",
            data=to_excel_bytes(impl_dl),
            file_name="implementation_framework.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def main():
    if not st.session_state.authenticated:
        render_login()
        return

    if not MODEL_LOADED:
        st.error(f"⚠️  Could not load model: {MODEL_ERROR}")
        st.info("Ensure `arumeru_sii_model.pkl` is in the same folder as `app.py`.")
        return

    render_navbar()
    render_tabs()

    if st.session_state.active_page == 'prediction':
        render_prediction()
    else:
        render_evaluation()


if __name__ == "__main__":
    main()