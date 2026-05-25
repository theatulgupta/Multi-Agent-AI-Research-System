import streamlit as st
import time
import re
from typing import Any
from httpx import HTTPStatusError

# ── page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── fonts & base ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    border-right: 1px solid #2a2a4a;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* ── hero banner ── */
.hero {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 40%, #16213e 100%);
    border: 1px solid #2a2a4a;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(99,102,241,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.4rem; font-weight: 700; letter-spacing: -0.5px;
    background: linear-gradient(135deg, #818cf8, #c084fc, #38bdf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 0.4rem;
}
.hero-sub {
    color: #94a3b8; font-size: 1rem; font-weight: 400; margin: 0;
}

/* ── pipeline tracker ── */
.pipeline-wrap {
    display: flex; align-items: center; justify-content: center;
    gap: 0; margin: 1.5rem 0; flex-wrap: nowrap; overflow-x: auto;
}
.step-node {
    display: flex; flex-direction: column; align-items: center;
    min-width: 100px; position: relative;
}
.step-circle {
    width: 52px; height: 52px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; font-weight: 700;
    border: 2px solid; transition: all 0.4s ease;
    position: relative; z-index: 1;
}
.step-idle   { background: #1e1e3a; border-color: #3a3a5c; color: #4a4a7a; }
.step-active { background: #1e1b4b; border-color: #818cf8; color: #818cf8;
               box-shadow: 0 0 20px rgba(129,140,248,0.4); animation: pulse 1.5s infinite; }
.step-done   { background: #052e16; border-color: #22c55e; color: #22c55e;
               box-shadow: 0 0 12px rgba(34,197,94,0.3); }
.step-error  { background: #2d0a0a; border-color: #ef4444; color: #ef4444; }
.step-label  { font-size: 0.68rem; color: #64748b; margin-top: 6px;
               text-align: center; font-weight: 500; letter-spacing: 0.3px; max-width: 90px; }
.step-label-active { color: #818cf8 !important; }
.step-label-done   { color: #22c55e !important; }
.step-connector {
    flex: 1; height: 2px; min-width: 20px; max-width: 50px;
    background: #2a2a4a; margin-bottom: 28px; transition: background 0.4s;
}
.step-connector-done { background: linear-gradient(90deg, #22c55e, #818cf8); }

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 20px rgba(129,140,248,0.4); }
    50%       { box-shadow: 0 0 35px rgba(129,140,248,0.7); }
}

/* ── status badge ── */
.status-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;
}
.badge-idle    { background: #1e1e3a; color: #64748b; border: 1px solid #2a2a4a; }
.badge-running { background: #1e1b4b; color: #818cf8; border: 1px solid #818cf8; }
.badge-done    { background: #052e16; color: #22c55e; border: 1px solid #22c55e; }
.badge-error   { background: #2d0a0a; color: #ef4444; border: 1px solid #ef4444; }

/* ── result cards ── */
.result-card {
    background: #0f0f1a;
    border: 1px solid #2a2a4a;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.result-card-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 0.8rem; padding-bottom: 0.8rem;
    border-bottom: 1px solid #1e1e3a;
}
.result-card-icon { font-size: 1.2rem; }
.result-card-title { font-size: 0.9rem; font-weight: 600; color: #e2e8f0; }

/* ── final report ── */
.final-report-wrap {
    background: linear-gradient(135deg, #0a0a1a, #0f0f1e);
    border: 1px solid #3730a3;
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1rem;
}
.final-report-wrap h1, .final-report-wrap h2, .final-report-wrap h3 { color: #c7d2fe; }
.final-report-wrap p, .final-report-wrap li { color: #cbd5e1; line-height: 1.75; }

/* ── score pills ── */
.score-grid { display: flex; flex-wrap: wrap; gap: 8px; margin: 0.5rem 0; }
.score-pill {
    padding: 4px 14px; border-radius: 20px; font-size: 0.78rem; font-weight: 600;
    border: 1px solid;
}
.score-high   { background: #052e16; color: #4ade80; border-color: #166534; }
.score-mid    { background: #1c1917; color: #fbbf24; border-color: #78350f; }
.score-low    { background: #2d0a0a; color: #f87171; border-color: #7f1d1d; }

/* ── input area ── */
.stTextInput > div > div > input, .stTextArea textarea {
    background: #0f0f1a !important;
    border: 1px solid #2a2a4a !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus, .stTextArea textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 2px rgba(129,140,248,0.2) !important;
}

/* ── buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    padding: 0.6rem 2rem !important; font-size: 0.95rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #4338ca, #6d28d9) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
}

/* ── expander ── */
[data-testid="stExpander"] {
    background: #0f0f1a !important;
    border: 1px solid #2a2a4a !important;
    border-radius: 10px !important;
}

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] { background: #0f0f1a; border-radius: 10px; gap: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; color: #64748b; font-weight: 500; }
.stTabs [aria-selected="true"] { background: #1e1b4b !important; color: #818cf8 !important; }

/* ── divider ── */
hr { border-color: #1e1e3a !important; }

/* ── metric ── */
[data-testid="stMetric"] {
    background: #0f0f1a; border: 1px solid #2a2a4a;
    border-radius: 10px; padding: 0.8rem 1rem;
}
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-size: 1.4rem !important; }
</style>
""", unsafe_allow_html=True)


# ── helpers ────────────────────────────────────────────────────────────────────

STEPS = [
    ("🔍", "Search",   "Finding sources"),
    ("🌐", "Scrape",   "Extracting content"),
    ("✍️", "Writer",   "Drafting report"),
    ("🧐", "Critic",   "Reviewing report"),
    ("✨", "Revision", "Final polish"),
]

def render_pipeline(active: int, done_up_to: int, error_at: int = -1):
    """Render the horizontal pipeline tracker."""
    nodes = []
    for i, (icon, label, _) in enumerate(STEPS):
        if error_at == i:
            circle_cls, label_cls = "step-circle step-error", "step-label"
            icon_show = "✗"
        elif i < done_up_to:
            circle_cls, label_cls = "step-circle step-done", "step-label step-label-done"
            icon_show = "✓"
        elif i == active:
            circle_cls, label_cls = "step-circle step-active", "step-label step-label-active"
            icon_show = icon
        else:
            circle_cls, label_cls = "step-circle step-idle", "step-label"
            icon_show = icon

        connector = ""
        if i < len(STEPS) - 1:
            conn_cls = "step-connector step-connector-done" if i < done_up_to - 1 else "step-connector"
            connector = f'<div class="{conn_cls}"></div>'

        nodes.append(f"""
        <div class="step-node">
            <div class="{circle_cls}">{icon_show}</div>
            <div class="{label_cls}">{label}</div>
        </div>
        {connector}
        """)

    st.markdown(f'<div class="pipeline-wrap">{"".join(nodes)}</div>', unsafe_allow_html=True)


def extract_scores(feedback: str) -> dict:
    """Pull X/10 scores out of the critic output."""
    scores = {}
    for metric in ["Accuracy", "Depth", "Clarity", "Source Usage", "Insight Quality", "Overall Quality"]:
        match = re.search(rf"{metric}[:\s]+(\d+)/10", feedback, re.IGNORECASE)
        if match:
            scores[metric] = int(match.group(1))
    return scores


def score_color(val: int) -> str:
    if val >= 8: return "score-high"
    if val >= 6: return "score-mid"
    return "score-low"


def extract_verdict(feedback: str) -> str:
    for verdict in ["Accept", "Minor Revision", "Major Revision", "Reject"]:
        if verdict.lower() in feedback.lower():
            return verdict
    return "Unknown"


def verdict_color(v: str) -> str:
    return {"Accept": "#22c55e", "Minor Revision": "#fbbf24",
            "Major Revision": "#f97316", "Reject": "#ef4444"}.get(v, "#94a3b8")


def _invoke_with_retry(runnable, payload, retries: int = 2, delay: float = 3.0) -> Any:
    for attempt in range(retries):
        try:
            return runnable.invoke(payload)
        except HTTPStatusError as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            if status == 429 and attempt < retries - 1:
                time.sleep(delay)
                continue
            raise


# ── session state init ─────────────────────────────────────────────────────────
for key in ["running", "done", "state", "active_step", "error", "elapsed"]:
    if key not in st.session_state:
        st.session_state[key] = False if key in ("running", "done", "error") else (0 if key in ("active_step", "elapsed") else {})


# ── sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔬 Research System")
    st.markdown("---")

    st.markdown("### ⚙️ Configuration")
    max_results = st.slider("Search results", 1, 5, 3)
    scrape_limit = st.slider("Scrape char limit", 1000, 5000, 3000, step=500)

    st.markdown("---")
    st.markdown("### 📋 Pipeline Steps")
    for icon, label, desc in STEPS:
        st.markdown(f"{icon} **{label}** — {desc}")

    st.markdown("---")
    st.markdown("### 💡 Example Topics")
    examples = [
        "Quantum Computing in 2025",
        "AI in Healthcare",
        "Climate Change Solutions",
        "SpaceX Starship Program",
        "Blockchain in Finance",
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            # write directly to the text_input's key so it actually shows up
            st.session_state["topic_field"] = ex

    st.markdown("---")
    st.markdown('<p style="color:#475569;font-size:0.75rem;text-align:center">Built with LangChain · LangGraph · Mistral · Tavily</p>', unsafe_allow_html=True)


# ── main layout ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">🔬 Multi-Agent Research System</div>
    <p class="hero-sub">Autonomous AI pipeline · Search → Scrape → Write → Review → Revise</p>
</div>
""", unsafe_allow_html=True)

# pipeline tracker (always visible)
active  = st.session_state.active_step if st.session_state.running else -1
done_up = st.session_state.active_step if st.session_state.done else (st.session_state.active_step if not st.session_state.running else 0)
if st.session_state.done:
    done_up = len(STEPS)
render_pipeline(active, done_up, error_at=st.session_state.active_step if st.session_state.error else -1)

st.markdown("---")

# ── input row ──────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1], gap="medium")

with col_input:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum Computing in 2025, AI in Healthcare ...",
        label_visibility="collapsed",
        key="topic_field"
    )

with col_btn:
    run_clicked = st.button("🚀 Research", use_container_width=True, disabled=st.session_state.running)

# ── metrics row (shown after run) ─────────────────────────────────────────────
if st.session_state.done and st.session_state.state:
    s = st.session_state.state
    scores = extract_scores(s.get("feedback", ""))
    verdict = extract_verdict(s.get("feedback", ""))
    overall = scores.get("Overall Quality", 0)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("⏱ Time Taken",    f"{st.session_state.elapsed:.0f}s")
    m2.metric("📊 Overall Score", f"{overall}/10" if overall else "—")
    m3.metric("⚖️ Verdict",       verdict)
    m4.metric("📄 Report Length", f"{len(s.get('final_report','').split()):,} words")

    st.markdown("---")

# ── run pipeline ───────────────────────────────────────────────────────────────
if run_clicked and topic.strip():
    # reset state
    st.session_state.running     = True
    st.session_state.done        = False
    st.session_state.error       = False
    st.session_state.state       = {}
    st.session_state.active_step = 0
    st.session_state.elapsed     = 0

    start_time = time.time()

    # live status placeholder
    status_ph  = st.empty()
    progress_ph = st.empty()

    try:
        from agents import (
            build_search_agent, build_scrape_agent,
            writer_chain, critic_chain, revision_chain
        )

        state = {}

        # ── step 1: search ──────────────────────────────────────────────────
        st.session_state.active_step = 0
        status_ph.markdown('<span class="status-badge badge-running">⟳ &nbsp;Running Search Agent...</span>', unsafe_allow_html=True)
        progress_ph.progress(5, text="Searching the web for sources...")

        search_agent = build_search_agent()
        search_response = _invoke_with_retry(search_agent, {
            "messages": [(
                "user",
                f"Find recent, reliable, and detailed information about:\n\nTOPIC: {topic}\n\nFocus on trusted sources, factual information, useful URLs, and recent developments."
            )]
        })
        # content can be a list of dicts (structured agent output) — flatten to string
        raw = search_response["messages"][-1].content
        state["search_result"] = raw if isinstance(raw, str) else " ".join(
            c.get("text", "") for c in raw if isinstance(c, dict) and "text" in c
        )
        progress_ph.progress(20, text="Search complete ✓")

        # ── step 2: scrape ──────────────────────────────────────────────────
        st.session_state.active_step = 1
        status_ph.markdown('<span class="status-badge badge-running">⟳ &nbsp;Running Scrape Agent...</span>', unsafe_allow_html=True)
        progress_ph.progress(25, text="Scraping best URL for full content...")

        scrape_agent = build_scrape_agent()
        scrape_response = _invoke_with_retry(scrape_agent, {
            "messages": [(
                "user",
                f"From the search results below, pick the best URL and use scrape_url to extract its content.\n\nSEARCH RESULTS:\n{state['search_result'][:1500]}"
            )]
        })
        raw = scrape_response["messages"][-1].content
        state["scrape_result"] = raw if isinstance(raw, str) else " ".join(
            c.get("text", "") for c in raw if isinstance(c, dict) and "text" in c
        )
        research = f"SEARCH RESULTS:\n{state['search_result']}\n\nSCRAPED CONTENT:\n{state['scrape_result']}"
        progress_ph.progress(40, text="Scraping complete ✓")

        # ── step 3: writer ──────────────────────────────────────────────────
        st.session_state.active_step = 2
        status_ph.markdown('<span class="status-badge badge-running">⟳ &nbsp;Writer Chain drafting report...</span>', unsafe_allow_html=True)
        progress_ph.progress(45, text="Drafting the research report...")

        state["report"] = _invoke_with_retry(writer_chain, {"topic": topic, "research": research})
        progress_ph.progress(65, text="Draft complete ✓")

        # ── step 4: critic ──────────────────────────────────────────────────
        st.session_state.active_step = 3
        status_ph.markdown('<span class="status-badge badge-running">⟳ &nbsp;Critic Chain reviewing report...</span>', unsafe_allow_html=True)
        progress_ph.progress(68, text="Reviewing and scoring the report...")

        state["feedback"] = _invoke_with_retry(critic_chain, {
            "topic": topic, "research": research, "report": state["report"]
        })
        progress_ph.progress(85, text="Review complete ✓")

        # ── step 5: revision ────────────────────────────────────────────────
        st.session_state.active_step = 4
        status_ph.markdown('<span class="status-badge badge-running">⟳ &nbsp;Revision Chain polishing report...</span>', unsafe_allow_html=True)
        progress_ph.progress(88, text="Applying revisions based on feedback...")

        state["final_report"] = _invoke_with_retry(revision_chain, {
            "topic": topic, "report": state["report"],
            "research": research, "feedback": state["feedback"]
        })
        progress_ph.progress(100, text="Pipeline complete ✓")

        # done
        st.session_state.state   = state
        st.session_state.elapsed = time.time() - start_time
        st.session_state.done    = True
        st.session_state.running = False

        status_ph.markdown('<span class="status-badge badge-done">✓ &nbsp;Pipeline complete</span>', unsafe_allow_html=True)
        time.sleep(0.5)
        st.rerun()

    except Exception as e:
        st.session_state.running = False
        st.session_state.error   = True
        status_ph.markdown(f'<span class="status-badge badge-error">✗ &nbsp;Error: {e}</span>', unsafe_allow_html=True)
        st.error(f"Pipeline failed at step {st.session_state.active_step + 1}: {e}")

elif run_clicked and not topic.strip():
    st.warning("Please enter a research topic first.")


# ── results ────────────────────────────────────────────────────────────────────
if st.session_state.done and st.session_state.state:
    s = st.session_state.state

    tab_report, tab_critic, tab_raw = st.tabs(["📄 Final Report", "🧐 Critic Review", "🔎 Raw Pipeline Data"])

    # ── tab 1: final report ────────────────────────────────────────────────────
    with tab_report:
        col_dl, col_copy = st.columns([1, 5])
        with col_dl:
            st.download_button(
                "⬇️ Download",
                data=s.get("final_report", ""),
                file_name=f"report_{topic[:30].replace(' ','_')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        st.markdown('<div class="final-report-wrap">', unsafe_allow_html=True)
        st.markdown(s.get("final_report", ""), unsafe_allow_html=False)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── tab 2: critic review ───────────────────────────────────────────────────
    with tab_critic:
        feedback = s.get("feedback", "")
        scores   = extract_scores(feedback)
        verdict  = extract_verdict(feedback)
        v_color  = verdict_color(verdict)

        # verdict banner
        st.markdown(f"""
        <div style="background:#0f0f1a;border:1px solid {v_color}33;border-radius:12px;
                    padding:1rem 1.4rem;margin-bottom:1rem;display:flex;
                    align-items:center;gap:12px;">
            <span style="font-size:1.5rem">⚖️</span>
            <div>
                <div style="color:#94a3b8;font-size:0.75rem;font-weight:500">FINAL VERDICT</div>
                <div style="color:{v_color};font-size:1.2rem;font-weight:700">{verdict}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # score pills
        if scores:
            st.markdown("**Quality Scores**")
            pills = "".join(
                f'<span class="score-pill {score_color(v)}">{k}: {v}/10</span>'
                for k, v in scores.items()
            )
            st.markdown(f'<div class="score-grid">{pills}</div>', unsafe_allow_html=True)
            st.markdown("")

        # full feedback
        with st.expander("📋 Full Critic Feedback", expanded=True):
            st.markdown(feedback)

    # ── tab 3: raw pipeline data ───────────────────────────────────────────────
    with tab_raw:
        with st.expander("🔍 Search Agent Output", expanded=False):
            st.markdown(
                f'<div class="result-card"><div class="result-card-header">'
                f'<span class="result-card-icon">🔍</span>'
                f'<span class="result-card-title">Search Results</span></div></div>',
                unsafe_allow_html=True
            )
            raw_search = s.get("search_result", "")
            # render list items if it's a list repr
            st.text_area("", value=str(raw_search), height=300, label_visibility="collapsed")

        with st.expander("🌐 Scrape Agent Output", expanded=False):
            st.text_area("", value=s.get("scrape_result", ""), height=300, label_visibility="collapsed")

        with st.expander("✍️ Draft Report (pre-revision)", expanded=False):
            st.markdown(s.get("report", ""))
