from textwrap import dedent

STREAMLIT_CSS = dedent(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    :root {
        --bg: #05070b;
        --panel: rgba(10, 14, 20, 0.94);
        --text: #f3f4f6;
        --muted: #a4afbd;
        --accent: #22c55e;
        --accent-2: #86efac;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background:
            radial-gradient(circle at top left, rgba(34, 197, 94, 0.14), transparent 28%),
            radial-gradient(circle at top right, rgba(134, 239, 172, 0.08), transparent 26%),
            linear-gradient(180deg, var(--bg) 0%, #070b11 100%);
        color: var(--text);
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.1rem; padding-bottom: 2.4rem; max-width: 1260px; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070b10 0%, #0c1118 100%);
        border-right: 1px solid rgba(34, 197, 94, 0.08);
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }

    .hero {
        background: linear-gradient(135deg, rgba(8, 10, 15, 0.96) 0%, rgba(7, 14, 10, 0.94) 55%, rgba(8, 10, 15, 0.96) 100%);
        border: 1px solid rgba(34, 197, 94, 0.16);
        border-radius: 22px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 18px 60px rgba(0, 0, 0, 0.28);
    }
    .hero::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 15% 0%, rgba(34, 197, 94, 0.18), transparent 34%),
                radial-gradient(circle at 85% 0%, rgba(134, 239, 172, 0.12), transparent 30%);
        pointer-events: none;
    }
    .hero-grid { display: flex; justify-content: space-between; gap: 1rem; align-items: end; position: relative; z-index: 1; }
    .hero-title {
        font-size: 2.2rem; font-weight: 800; letter-spacing: -0.04em; margin: 0;
        background: linear-gradient(135deg, #ecfdf5 0%, var(--accent) 42%, var(--accent-2) 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero-sub { margin: 0.35rem 0 0; color: var(--muted); font-size: 0.98rem; line-height: 1.5; max-width: 58rem; }
    .hero-badges { display: flex; flex-wrap: wrap; gap: 0.55rem; justify-content: flex-end; }
    .hero-badge {
        display: inline-flex; align-items: center; gap: 0.45rem; padding: 0.42rem 0.8rem; border-radius: 999px;
        border: 1px solid rgba(34, 197, 94, 0.16); background: rgba(34, 197, 94, 0.05);
        color: var(--text); font-size: 0.78rem; font-weight: 600;
    }

    .section-card {
        background: var(--panel); border: 1px solid rgba(34, 197, 94, 0.08);
        border-radius: 20px; padding: 1rem 1.1rem; box-shadow: 0 16px 45px rgba(0, 0, 0, 0.22);
    }
    .section-title { font-size: 0.95rem; font-weight: 700; color: var(--text); margin: 0 0 0.35rem; }
    .section-subtitle { margin: 0; color: var(--muted); font-size: 0.85rem; line-height: 1.5; }

    .research-grid { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(280px, 0.9fr); gap: 1rem; margin-bottom: 1rem; }
    .research-console { background: linear-gradient(180deg, rgba(17, 14, 10, 0.96), rgba(10, 12, 16, 0.96)); border: 1px solid rgba(245, 158, 11, 0.12); border-radius: 22px; padding: 1rem; }
    .research-meta { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.75rem; }
    .meta-chip {
        display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.4rem 0.75rem; border-radius: 999px;
        border: 1px solid rgba(34, 197, 94, 0.14); background: rgba(34, 197, 94, 0.05);
        color: var(--muted); font-size: 0.76rem; font-weight: 600;
    }
    .workflow-note {
        border-left: 3px solid var(--accent); background: rgba(34, 197, 94, 0.07); padding: 0.8rem 0.9rem;
        border-radius: 14px; color: #cfe8ff; font-size: 0.88rem; line-height: 1.6;
    }

    .pipeline-shell { background: rgba(7, 15, 26, 0.78); border: 1px solid rgba(34, 197, 94, 0.1); border-radius: 20px; padding: 0.2rem; overflow: hidden; }
    .status-badge { display: inline-flex; align-items: center; gap: 0.45rem; padding: 0.42rem 0.8rem; border-radius: 999px; font-size: 0.77rem; font-weight: 700; }
    .badge-idle { background: rgba(255,255,255,0.04); color: var(--muted); border: 1px solid rgba(255,255,255,0.08); }
    .badge-running { background: rgba(34, 197, 94, 0.12); color: #bbf7d0; border: 1px solid rgba(34, 197, 94, 0.26); }
    .badge-done { background: rgba(74, 222, 128, 0.12); color: #9bf0b4; border: 1px solid rgba(74, 222, 128, 0.28); }
    .badge-error { background: rgba(251, 113, 133, 0.12); color: #fecdd3; border: 1px solid rgba(251, 113, 133, 0.28); }

    .result-card { background: rgba(8, 15, 27, 0.94); border: 1px solid rgba(34, 197, 94, 0.08); border-radius: 18px; padding: 1rem 1.1rem; margin-bottom: 1rem; }
    .result-card-header { display: flex; align-items: center; gap: 10px; margin-bottom: 0.8rem; padding-bottom: 0.75rem; border-bottom: 1px solid rgba(255, 255, 255, 0.06); }
    .result-card-icon { font-size: 1.1rem; }
    .result-card-title { font-size: 0.88rem; font-weight: 700; color: var(--text); }

    .paper-shell { background: linear-gradient(180deg, rgba(13, 15, 18, 0.94), rgba(8, 10, 13, 0.98)); border: 1px solid rgba(245, 158, 11, 0.1); border-radius: 20px; padding: 1.5rem; }
    .paper-shell h1, .paper-shell h2, .paper-shell h3 { color: #dce9ff; }
    .paper-shell p, .paper-shell li { color: #c7d6eb; line-height: 1.75; }

    .score-grid { display: flex; flex-wrap: wrap; gap: 8px; margin: 0.5rem 0 0; }
    .score-pill { padding: 0.38rem 0.8rem; border-radius: 999px; font-size: 0.78rem; font-weight: 700; border: 1px solid; }
    .score-high { background: rgba(74, 222, 128, 0.12); color: #9bf0b4; border-color: rgba(74, 222, 128, 0.25); }
    .score-mid { background: rgba(251, 191, 36, 0.12); color: #fde68a; border-color: rgba(251, 191, 36, 0.25); }
    .score-low { background: rgba(251, 113, 133, 0.12); color: #fecdd3; border-color: rgba(251, 113, 133, 0.25); }

    .artifact-card { background: rgba(7, 15, 26, 0.88); border: 1px solid rgba(245, 158, 11, 0.08); border-radius: 18px; padding: 1rem; margin-bottom: 1rem; }

    .stTextInput > div > div > input, .stTextArea textarea {
        background: #091220 !important; border: 1px solid rgba(34, 197, 94, 0.12) !important; border-radius: 14px !important;
        color: var(--text) !important; font-family: 'Inter', sans-serif !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea textarea:focus {
        border-color: rgba(34, 197, 94, 0.7) !important; box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.14) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #14532d, #22c55e) !important; color: white !important; border: none !important;
        border-radius: 14px !important; font-weight: 700 !important; padding: 0.7rem 1.2rem !important; font-size: 0.95rem !important;
        transition: all 0.18s ease !important; box-shadow: 0 10px 30px rgba(34, 197, 94, 0.25) !important;
    }
    .stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 14px 36px rgba(34, 197, 94, 0.28) !important; }

    [data-testid="stExpander"] { background: rgba(7, 15, 26, 0.85) !important; border: 1px solid rgba(34, 197, 94, 0.08) !important; border-radius: 14px !important; }
    .stTabs [data-baseweb="tab-list"] { background: rgba(7, 15, 26, 0.82); border-radius: 14px; gap: 6px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { border-radius: 10px; color: var(--muted); font-weight: 600; }
    .stTabs [aria-selected="true"] { background: rgba(34, 197, 94, 0.12) !important; color: #dcfce7 !important; }
    hr { border-color: rgba(255,255,255,0.06) !important; }
    [data-testid="stMetric"] { background: rgba(7, 15, 26, 0.88); border: 1px solid rgba(34,197,94,0.08); border-radius: 14px; padding: 0.85rem 1rem; }
    [data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.74rem !important; }
    [data-testid="stMetricValue"] { color: var(--text) !important; font-size: 1.35rem !important; }
    </style>
    """
)


def apply_theme() -> None:
    import streamlit as st

    st.markdown(STREAMLIT_CSS, unsafe_allow_html=True)
