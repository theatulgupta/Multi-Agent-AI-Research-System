from __future__ import annotations

import time

import streamlit as st

from .config import APP_NAME, STAGE_GUIDES, STEPS
from .service import extract_scores, extract_verdict, run_research_pipeline
from .theme import apply_theme
from .ui import (
    render_action_button,
    render_example_topics,
    render_hero,
    render_input_row,
    render_pipeline,
    render_process_note,
    render_raw_artifact,
    render_report_shell,
    render_score_pills,
    render_sidebar,
    render_workspace_intro,
)


def _init_state() -> None:
    defaults = {
        "running": False,
        "done": False,
        "state": {},
        "active_step": 0,
        "error": False,
        "elapsed": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def main() -> None:
    st.set_page_config(page_title=APP_NAME, page_icon="R", layout="wide", initial_sidebar_state="expanded")
    apply_theme()
    _init_state()

    with st.sidebar:
        render_sidebar()
        st.markdown("### Configuration")
        max_results = st.slider("Search results", 1, 5, 3)
        scrape_limit = st.slider("Scrape char limit", 1000, 5000, 3000, step=500)
        st.markdown("---")
        render_example_topics()
        st.markdown("---")
        st.markdown('<p style="color:#7f8a99;font-size:0.75rem;text-align:center">Built for evidence-led research workflows.</p>', unsafe_allow_html=True)

    render_hero()

    left_col, right_col = st.columns([1.18, 0.92], gap="large")

    with left_col:
        render_workspace_intro()
        st.markdown("<div style='height:0.85rem'></div>", unsafe_allow_html=True)
        topic = render_input_row()
        run_clicked = render_action_button(disabled=st.session_state.running)

    active = st.session_state.active_step if st.session_state.running else -1
    done_up = st.session_state.active_step if st.session_state.done else (st.session_state.active_step if not st.session_state.running else 0)
    if st.session_state.done:
        done_up = len(STEPS)

    with right_col:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        pipeline_ph = st.empty()
        render_pipeline(active, done_up, error_at=st.session_state.active_step if st.session_state.error else -1, target=pipeline_ph)

    if st.session_state.done and st.session_state.state:
        s = st.session_state.state
        scores = extract_scores(s.get("feedback", ""))
        verdict = extract_verdict(s.get("feedback", ""))
        overall = scores.get("Overall Quality", 0)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Time Taken", f"{st.session_state.elapsed:.0f}s")
        m2.metric("Overall Score", f"{overall}/10" if overall else "—")
        m3.metric("Verdict", verdict)
        m4.metric("Report Length", f"{len(s.get('final_report','').split()):,} words")

        st.markdown("---")

    if run_clicked and topic.strip():
        st.session_state.running = True
        st.session_state.done = False
        st.session_state.error = False
        st.session_state.state = {}
        st.session_state.active_step = 0
        st.session_state.elapsed = 0
        start_time = time.time()

        status_ph = st.empty()
        progress_ph = st.empty()

        stage_progress = [8, 28, 52, 74, 92]

        def progress(step: int, state: str, message: str) -> None:
            st.session_state.active_step = step
            status_ph.markdown(
                f'<span class="status-badge badge-{state}">{message}</span>',
                unsafe_allow_html=True,
            )
            progress_ph.progress(stage_progress[step], text=message)
            done_up_to = step + 1 if state == "done" else step
            active_step = min(step + 1, len(STEPS) - 1) if state == "done" else step
            render_pipeline(active_step, done_up_to, error_at=-1, target=pipeline_ph)

        try:
            state = run_research_pipeline(topic, max_results=max_results, scrape_limit=scrape_limit, progress=progress)
            st.session_state.state = state
            st.session_state.elapsed = time.time() - start_time
            st.session_state.done = True
            st.session_state.running = False
            status_ph.markdown('<span class="status-badge badge-done">Completed</span>', unsafe_allow_html=True)
            progress_ph.progress(100, text="Pipeline complete")
            st.rerun()
        except Exception as e:
            st.session_state.running = False
            st.session_state.error = True
            status_ph.markdown(f'<span class="status-badge badge-error">Error: {e}</span>', unsafe_allow_html=True)
            st.error(f"Pipeline failed at step {st.session_state.active_step + 1}: {e}")

    elif run_clicked and not topic.strip():
        st.warning("Please enter a research topic first.")

    if st.session_state.done and st.session_state.state:
        s = st.session_state.state
        tab_report, tab_critic, tab_raw = st.tabs(["Research Report", "Critic Review", "Evidence Trail"])

        with tab_report:
            col_dl, _ = st.columns([1, 5])
            with col_dl:
                st.download_button(
                    "Download",
                    data=s.get("final_report", ""),
                    file_name=f"report_{topic[:30].replace(' ','_')}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
            render_report_shell(s.get("final_report", ""))

        with tab_critic:
            feedback = s.get("feedback", "")
            scores = extract_scores(feedback)
            verdict = extract_verdict(feedback)
            color = {"Accept": "#4ade80", "Minor Revision": "#fbbf24", "Major Revision": "#f97316", "Reject": "#ef4444"}.get(verdict, "#a4afbd")

            st.markdown(
                f"""
                <div style="background:#0f1014;border:1px solid {color}33;border-radius:12px;padding:1rem 1.4rem;margin-bottom:1rem;display:flex;align-items:center;gap:12px;">
                    <div>
                        <div style="color:#a4afbd;font-size:0.75rem;font-weight:500">Final verdict</div>
                        <div style="color:{color};font-size:1.2rem;font-weight:700">{verdict}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if scores:
                render_score_pills(scores)

            with st.expander("Full critic feedback", expanded=True):
                st.markdown(feedback)

        with tab_raw:
            render_raw_artifact("Search Results", str(s.get("search_result", "")))
            render_raw_artifact("Scrape Agent Output", str(s.get("scrape_result", "")))
            with st.expander("Draft Report (pre-revision)", expanded=False):
                render_report_shell(s.get("report", ""))


if __name__ == "__main__":
    main()
