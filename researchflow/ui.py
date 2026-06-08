"""UI components and rendering functions for ResearchFlow."""
from __future__ import annotations

from html import escape

import streamlit as st

from .config import APP_NAME, APP_TAGLINE, EXAMPLE_TOPICS, STEPS
from .service import score_color


def render_pipeline(active: int, done_up_to: int, error_at: int = -1, target=None) -> None:
    """Render a clean horizontal pipeline with checkpoints.

    Args:
        active: Index of currently active step
        done_up_to: Number of completed steps
        error_at: Index of step with error (-1 if no error)
        target: Optional Streamlit placeholder to render into
    """

    # Calculate progress percentage
    total_steps = len(STEPS)
    progress_pct = (done_up_to / total_steps) * 100 if done_up_to > 0 else 0

    # Build checkpoint circles
    checkpoints = []
    for i, (label, desc) in enumerate(STEPS):
        # Determine state
        if error_at == i:
            state_color = "#ef4444"
            state_icon = "✕"
            state_class = "error"
        elif i < done_up_to:
            state_color = "#22c55e"
            state_icon = "✓"
            state_class = "done"
        elif i == active:
            state_color = "#22c55e"
            state_icon = "●"
            state_class = "active"
        else:
            state_color = "#4b5563"
            state_icon = "○"
            state_class = "idle"

        # Position on the line (evenly distributed)
        position_pct = (i / (total_steps - 1)) * 100 if total_steps > 1 else 50

        checkpoints.append(f'''
<div style="position:absolute;left:{position_pct}%;top:0;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:0.5rem;z-index:2;">
    <div style="width:36px;height:36px;border-radius:50%;background:{state_color}22;border:2px solid {state_color};display:flex;align-items:center;justify-content:center;font-size:1rem;color:{state_color};font-weight:700;box-shadow:0 0 15px {state_color}30;">{state_icon}</div>
    <div style="font-size:0.7rem;font-weight:600;color:{state_color};white-space:nowrap;margin-top:0.25rem;">{label}</div>
</div>''')

    html_content = f'''
<div style="background:rgba(10,14,20,0.6);border:1px solid rgba(34,197,94,0.15);border-radius:16px;padding:2rem 1.5rem;margin:1rem 0;">
    <div style="margin-bottom:1.5rem;">
        <div style="font-size:0.85rem;font-weight:700;color:#e5e7eb;margin-bottom:0.3rem;">Research Pipeline</div>
        <div style="font-size:0.75rem;color:#9ca3af;">Live progress through evidence collection and synthesis</div>
    </div>

    <div style="position:relative;height:90px;margin:1.5rem 0;padding:0 20px;">
        <div style="position:relative;height:100%;">
            <!-- Background track -->
            <div style="position:absolute;top:0;left:0;right:0;height:3px;background:#1f2937;border-radius:999px;"></div>

            <!-- Progress fill -->
            <div style="position:absolute;top:0;left:0;width:{progress_pct}%;height:3px;background:linear-gradient(90deg,#22c55e,#86efac);border-radius:999px;transition:width 0.5s ease;"></div>

            <!-- Checkpoints -->
            {''.join(checkpoints)}
        </div>
    </div>

    <div style="margin-top:1.5rem;padding:0.8rem 1rem;background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.2);border-radius:10px;">
        <div style="font-size:0.75rem;color:#86efac;font-weight:600;">
            {STEPS[active][1] if 0 <= active < len(STEPS) else "Ready to start"}
        </div>
    </div>
</div>'''

    if target is not None:
        target.html(html_content)
    else:
        st.html(html_content)


def render_hero() -> None:
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,rgba(8,10,15,0.96),rgba(7,14,10,0.94));border:1px solid rgba(34,197,94,0.2);border-radius:20px;padding:1.8rem 2rem;margin-bottom:1.5rem;box-shadow:0 20px 60px rgba(0,0,0,0.3);">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:1.5rem;flex-wrap:wrap;">
                <div>
                    <div style="font-size:2.2rem;font-weight:800;background:linear-gradient(135deg,#ecfdf5,#22c55e,#86efac);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0;">{APP_NAME}</div>
                    <p style="margin:0.4rem 0 0;color:#9ca3af;font-size:0.95rem;">{APP_TAGLINE}</p>
                </div>
                <div style="display:flex;gap:0.6rem;flex-wrap:wrap;">
                    <span style="padding:0.4rem 0.9rem;border-radius:999px;border:1px solid rgba(34,197,94,0.3);background:rgba(34,197,94,0.1);color:#86efac;font-size:0.75rem;font-weight:600;">Live Pipeline</span>
                    <span style="padding:0.4rem 0.9rem;border-radius:999px;border:1px solid rgba(34,197,94,0.3);background:rgba(34,197,94,0.1);color:#86efac;font-size:0.75rem;font-weight:600;">Source-Aware</span>
                    <span style="padding:0.4rem 0.9rem;border-radius:999px;border:1px solid rgba(34,197,94,0.3);background:rgba(34,197,94,0.1);color:#86efac;font-size:0.75rem;font-weight:600;">Auto-Review</span>
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
        <div style="background:rgba(10,14,20,0.6);border:1px solid rgba(34,197,94,0.15);border-radius:14px;padding:1rem 1.2rem;margin-bottom:1rem;">
            <div style="font-size:0.85rem;font-weight:700;color:#e5e7eb;margin-bottom:0.3rem;">Topic Briefing</div>
            <p style="margin:0;color:#9ca3af;font-size:0.8rem;line-height:1.5;">Enter a research topic below. The system will search, scrape, write, review, and revise while showing live progress.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_process_note(current_stage: str, target=None) -> None:
    content = f"""
        <div style="background:rgba(10,14,20,0.6);border:1px solid rgba(34,197,94,0.15);border-radius:14px;padding:1rem 1.2rem;margin-top:1rem;">
            <div style="font-size:0.85rem;font-weight:700;color:#e5e7eb;margin-bottom:0.3rem;">Current Stage</div>
            <p style="margin:0;color:#86efac;font-size:0.8rem;line-height:1.5;">{escape(current_stage)}</p>
        </div>
        """

    if target is not None:
        target.html(content)
        return

    st.html(content)


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
