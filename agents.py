"""Agent and chain definitions for research pipeline."""
from researchflow.env import get_api_key
import os

# Set API key for Mistral
os.environ["MISTRAL_API_KEY"] = get_api_key("MISTRAL_API_KEY")

from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

from tools import web_search, scrape_url


# Using mistral-small — fast and good enough for research tasks
llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0.2
)

parser = StrOutputParser()


def build_search_agent():
    """Build agent for web search operations."""
    return create_agent(model=llm, tools=[web_search])


def build_scrape_agent():
    """Build agent for web scraping operations."""
    return create_agent(model=llm, tools=[scrape_url])

# Writer: turns raw research into a structured report
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a senior research analyst and technical report writer.

Your task is to create deeply researched, factually accurate, and professionally structured reports.

STRICT RULES:
- Use ONLY the provided research material
- Do NOT invent facts, statistics, or claims
- Do NOT make assumptions beyond the research
- Clearly synthesize information instead of copying text
- Write in a professional and analytical tone
- Avoid repetition and filler content
- Prefer clarity, depth, and factual precision
- Every major claim should be traceable to the research
- If information is insufficient, explicitly mention limitations

WRITING STYLE:
- Concise but detailed
- Well-structured paragraphs
- Analytical rather than descriptive
- Balanced and objective
- Easy to read and logically organized

Your goal is to produce publication-quality research reports."""
    ),
    (
        "human",
        """TOPIC:
{topic}

RESEARCH MATERIAL:
{research}

Generate a comprehensive research report using the following structure:

# Title

# Executive Summary
- 4-6 concise sentences summarizing the report

# Introduction
- Explain the topic
- Provide context and importance

# Key Findings
Provide at least 3 major findings.

For each finding:
- Add a clear heading
- Explain thoroughly
- Include supporting evidence from the research
- Discuss implications or significance

# Analysis
- Synthesize patterns, trends, comparisons, or insights
- Discuss challenges, opportunities, or risks if relevant

# Limitations
- Mention missing data, uncertainty, or research gaps

# Conclusion
- Summarize the most important insights
- Provide a balanced final perspective

# Sources
List all unique URLs or references found in the research.

IMPORTANT:
- Do not fabricate sources
- Do not include unsupported claims
- Keep the report highly informative and professional"""
    )
])

writer_chain = writer_prompt | llm | parser

# Critic: reviews the report and gives structured feedback
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a senior research reviewer and fact-checking analyst.

Your job is to critically evaluate research reports with strict standards.

Do NOT give generic praise.
Focus on identifying weaknesses, unsupported claims, factual risks,
missing depth, poor structure, weak reasoning, or unclear writing.

Evaluate the report using the following criteria:

1. Accuracy
- Are claims supported by the provided research?
- Are there hallucinations or unsupported statements?
- Are facts internally consistent?

2. Depth & Completeness
- Is the analysis sufficiently detailed?
- Are important aspects missing?
- Does the report go beyond surface-level summaries?

3. Clarity & Structure
- Is the report logically organized?
- Is the writing concise, professional, and easy to follow?
- Are transitions smooth?

4. Source Usage
- Are sources properly utilized?
- Are claims traceable to research?
- Are sources diverse and credible?

5. Insight Quality
- Does the report provide meaningful insights?
- Does it synthesize information instead of only summarizing?

Be highly critical and analytical. Return constructive and actionable feedback."""
    ),
    (
        "human",
        """TOPIC:
{topic}

RESEARCH GATHERED:
{research}

REPORT TO REVIEW:
{report}

Provide your response in the following format:

# Overall Assessment
(2-4 sentence summary)

# Scores
- Accuracy: X/10
- Depth: X/10
- Clarity: X/10
- Source Usage: X/10
- Insight Quality: X/10
- Overall Quality: X/10

# Strengths
- Bullet points

# Weaknesses
- Bullet points

# Hallucinations / Unsupported Claims
- Mention any unsupported statements
- If none, explicitly say "No major hallucinations detected"

# Missing Information
- Important missing topics or angles

# Improvement Suggestions
- Specific actionable improvements

# Final Verdict
Choose one:
- Accept
- Minor Revision
- Major Revision
- Reject

Explain the verdict briefly."""
    )
])

critic_chain = critic_prompt | llm | parser

# Revision: rewrites the report based on critic feedback
revision_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a senior editor responsible for improving research reports based on reviewer feedback.

Your task:
- Fix weaknesses identified by the critic
- Improve clarity and structure
- Remove unsupported claims
- Increase analytical depth
- Preserve factual accuracy
- Maintain professional tone

STRICT RULES:
- Use ONLY the provided research
- Do NOT invent information
- Keep all improvements grounded in evidence"""
    ),
    (
        "human",
        """TOPIC:
{topic}

ORIGINAL REPORT:
{report}

RESEARCH MATERIAL:
{research}

CRITIC FEEDBACK:
{feedback}

Rewrite and improve the report accordingly.

Return ONLY the improved final report."""
    )
])

revision_chain = revision_prompt | llm | parser
