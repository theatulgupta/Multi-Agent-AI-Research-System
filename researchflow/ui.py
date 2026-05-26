from __future__ import annotations

from html import escape

import streamlit as st

from .config import APP_NAME, APP_TAGLINE, EXAMPLE_TOPICS, STEPS
from .service import score_color


def render_pipeline(active: int, done_up_to: int, error_at: int = -1, target=None) -> None:
    """Render the pipeline with proper HTML (v2 - fixed)."""
    cards = []
    for i, (label, desc) in enumerate(STEPS):
        if error_at == i:
            tone = "#ef4444"
            status = "Error"
            line = "Failed"
            symbol = "✕"
        elif i < done_up_to:
            tone = "#22c55e"
            status = "Complete"
            line = "Finished"
            symbol = "✓"
        elif i == active:
            tone = "#22c55e"
            status = "Active"
            line = "Running"
            symbol = "●"
        else:
            tone = "#1f2937"
            status = "Waiting"
            line = "Pending"
            symbol = "○"

        connector = ""
        if i < len(STEPS) - 1:
            connector = f'<div style="width:2px;height:22px;background:{"rgba(34,197,94,0.7)" if i < done_up_to else "rgba(75,85,99,0.7)"};margin:0 auto;border-radius:999px;"></div>'

        cards.append(
            f"""
            <div style="display:grid;grid-template-columns:64px 1fr;gap:1rem;align-items:stretch;">
                <div style="display:flex;flex-direction:column;align-items:center;">
                    <div style="width:52px;height:52px;border-radius:16px;border:1px solid {tone};background:rgba(5,7,11,0.96);display:flex;align-items:center;justify-content:center;color:{tone};font-size:1.1rem;font-weight:800;box-shadow:0 0 0 1px rgba(255,255,255,0.02) inset;">{symbol}</div>
                    {connector}
                </div>
                <div style="background:#0b1118;border:1px solid {tone}40;border-radius:18px;padding:1rem 1.05rem;min-height:118px;box-shadow:0 10px 30px rgba(0,0,0,0.18);">
                    <div style="display:flex;justify-content:space-between;align-items:center;gap:0.8rem;margin-bottom:0.75rem;">
                        <div style="font-size:0.72rem;color:{tone};font-weight:800;text-transform:uppercase;letter-spacing:0.08em;">{status}</div>
                        <div style="font-size:0.72rem;color:#94a3b8;font-weight:700;">{line}</div>
                    </div>
                    <div style="font-size:1.08rem;font-weight:800;color:#f8fafc;margin-bottom:0.35rem;">{label}</div>
                    <div style="font-size:0.84rem;line-height:1.6;color:#9aa9b8;">{desc}</div>
                </div>
            </div>
            """
        )

    content = f"""
    <div class="section-card">
        <div class="section-title">Evidence Pipeline</div>
        <p class="section-subtitle">Live pipeline: source discovery, extraction, synthesis, review, revision.</p>
    </div>
    <div style="height:0.85rem"></div>
    <div style="display:flex;flex-direction:column;gap:0.95rem;">{''.join(cards)}</div>
    """

    if target is not None:
        target.markdown(content, unsafe_allow_html=True)
    else:
        st.markdown(content, unsafe_allow_html=True)


def render_hero() -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-grid">
                <div>
                    <div class="hero-title">{APP_NAME}</div>
                    <p class="hero-sub">{APP_TAGLINE} <span style="color:#22c55e;font-size:0.7rem;">[UI v2.0 - HTML FIX APPLIED]</span></p>
                </div>
                <div class="hero-badges">
                    <span class="hero-badge">Professional research workspace</span>
                    <span class="hero-badge">Live evidence flow</span>
                    <span class="hero-badge">Source-aware review</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    st.markdown("## ResearchFlow")
    st.markdown("---")
    st.markdown("### Configuration")


def render_workspace_intro() -> None:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Topic briefing</div>
            <p class="section-subtitle">Enter a topic and the system will search, scrape, write, review, and revise while showing each stage live.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_process_note(current_stage: str, target=None) -> None:
    content = f"""
        <div class="section-card">
            <div class="section-title">Current stage</div>
            <p class="section-subtitle">{escape(current_stage)}</p>
            <div class="research-meta">
                <span class="meta-chip">Sources first</span>
                <span class="meta-chip">Draft from evidence</span>
                <span class="meta-chip">Critique before finalizing</span>
            </div>
        </div>
        """

    if target is not None:
        target.markdown(content, unsafe_allow_html=True)
        return

    st.markdown(content, unsafe_allow_html=True)


def render_input_row(key: str = "topic_field") -> str:
    return st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum Computing in 2025, AI in Healthcare ...",
        label_visibility="collapsed",
        key=key,
    )


def render_action_button(disabled: bool = False) -> bool:
    return st.button("Start Research", use_container_width=True, disabled=disabled)


def render_example_topics() -> None:
    st.markdown("### Example Topics")
    for topic in EXAMPLE_TOPICS:
        if st.button(topic, key=f"example_{topic}", use_container_width=True):
            st.session_state["topic_field"] = topic


def render_status_badge(label: str, state: str) -> None:
    st.markdown(f'<span class="status-badge badge-{state}">{escape(label)}</span>', unsafe_allow_html=True)


def render_score_pills(scores: dict[str, int]) -> None:
    pills = "".join(f'<span class="score-pill {score_color(v)}">{escape(k)}: {v}/10</span>' for k, v in scores.items())
    st.markdown(f'<div class="score-grid">{pills}</div>', unsafe_allow_html=True)


def render_raw_artifact(title: str, value: str) -> None:
    st.markdown(
        f'<div class="result-card"><div class="result-card-header"><span class="result-card-title">{escape(title)}</span></div><div class="artifact-card"><pre style="margin:0;white-space:pre-wrap;color:#c7d6eb;font-family:IBM Plex Mono, monospace;font-size:0.86rem;line-height:1.7;">{escape(value)}</pre></div></div>',
        unsafe_allow_html=True,
    )


def render_report_shell(content: str) -> None:
    st.markdown('<div class="paper-shell">', unsafe_allow_html=True)
    st.markdown(content, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
