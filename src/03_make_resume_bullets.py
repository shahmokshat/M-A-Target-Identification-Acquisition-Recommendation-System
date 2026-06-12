"""
03_make_resume_bullets.py
Creates resume bullets and interview pitch for the M&A target screening project.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "resume_and_interview_pitch.txt"

TEXT = """
PROJECT TITLE
M&A Target Identification & Acquisition Recommendation System | Self Project

RESUME BULLET VERSION 1 - Finance / IB / Big 4
Built an M&A target-screening model for Indian consumer companies using public NSE/Yahoo Finance data; ranked potential targets across growth, profitability, leverage, cash flow, valuation and strategic-fit metrics to recommend acquisition candidates for a strategic buyer.

RESUME BULLET VERSION 2 - Consulting
Developed a structured acquisition-screening framework for an Indian consumer-sector buyer, combining market attractiveness, financial performance, valuation multiples and strategic fit to shortlist high-priority targets for due diligence.

RESUME BULLET VERSION 3 - Data / Analyst
Created a Python + Excel-based scoring engine to collect public company data, normalize financial metrics, assign weighted scores and generate an acquisition-attractiveness ranking with actionable recommendations.

30-SECOND INTERVIEW PITCH
I wanted a project that looked closer to real deal advisory work than a normal ML project. So I built an M&A target identification model for Indian consumer companies. I created a target universe, fetched public financial and valuation metrics, and scored companies on growth, profitability, free cash flow, leverage, valuation and strategic fit. The final output is a ranked shortlist of acquisition targets with a recommendation on which companies should move to deeper due diligence.

TECHNICAL EXPLANATION
The model converts each metric into percentile scores to make different metrics comparable. I used positive scoring for growth, margins, ROE and free cash flow, and inverse scoring for leverage and valuation multiples. Then I applied weights to calculate the acquisition attractiveness score. This mirrors the initial screening stage used before a full due diligence process.

WHAT TO SAY IF ASKED ABOUT DATA
The company universe can come from NSE/Nifty Indices public lists, and the financial data is pulled from Yahoo Finance using yfinance for educational analysis. I manually verify final metrics before using them in my resume or presentation.
""".strip()

OUTPUT.parent.mkdir(exist_ok=True)
OUTPUT.write_text(TEXT, encoding="utf-8")
print(f"Saved: {OUTPUT}")
