"""
01_fetch_public_data.py
Fetch public market/fundamental data for Indian listed companies using yfinance.

Run:
    python src/01_fetch_public_data.py

Output:
    outputs/raw_public_company_data.csv

Notes:
- This uses Yahoo Finance public data via yfinance for educational analysis.
- Always manually verify final numbers before putting them in a resume/project deck.
"""

from __future__ import annotations

import math
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "target_universe_consumer_food.csv"
OUTPUT_FILE = ROOT / "outputs" / "raw_public_company_data.csv"


def safe_number(value, divisor: float = 1.0):
    """Convert Yahoo values to float, with optional divisor."""
    try:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return np.nan
        return float(value) / divisor
    except Exception:
        return np.nan


def row_from_yfinance(input_row: pd.Series) -> dict:
    ticker = input_row["ticker"]
    company = input_row["company"]
    print(f"Fetching {ticker} - {company}")

    try:
        stock = yf.Ticker(ticker)
        info = stock.get_info()
    except Exception as exc:
        print(f"  Warning: could not fetch {ticker}: {exc}")
        info = {}

    # Yahoo gives rupee-level numbers. Convert to ₹ crore by dividing by 10,000,000.
    crore = 10_000_000

    market_cap_cr = safe_number(info.get("marketCap"), crore)
    enterprise_value_cr = safe_number(info.get("enterpriseValue"), crore)
    revenue_ttm_cr = safe_number(info.get("totalRevenue"), crore)
    free_cash_flow_cr = safe_number(info.get("freeCashflow"), crore)

    # Percent fields sometimes come as decimals: 0.15 = 15%.
    revenue_growth_pct = safe_number(info.get("revenueGrowth")) * 100
    ebitda_margin_pct = safe_number(info.get("ebitdaMargins")) * 100
    roe_pct = safe_number(info.get("returnOnEquity")) * 100

    debt_to_equity = safe_number(info.get("debtToEquity"))
    if not np.isnan(debt_to_equity):
        # Yahoo often returns debt/equity as percent. Convert 45 to 0.45.
        debt_to_equity = debt_to_equity / 100 if debt_to_equity > 5 else debt_to_equity

    ev_to_revenue = safe_number(info.get("enterpriseToRevenue"))
    ev_to_ebitda = safe_number(info.get("enterpriseToEbitda"))

    # Fallback calculations using financial statements if possible.
    try:
        financials = stock.financials
        cashflow = stock.cashflow
        if revenue_ttm_cr != revenue_ttm_cr and "Total Revenue" in financials.index:
            revenue_ttm_cr = safe_number(financials.loc["Total Revenue"].iloc[0], crore)
        if revenue_growth_pct != revenue_growth_pct and "Total Revenue" in financials.index and len(financials.loc["Total Revenue"]) >= 2:
            latest = financials.loc["Total Revenue"].iloc[0]
            previous = financials.loc["Total Revenue"].iloc[1]
            if previous and previous != 0:
                revenue_growth_pct = (latest / previous - 1) * 100
        if free_cash_flow_cr != free_cash_flow_cr and "Free Cash Flow" in cashflow.index:
            free_cash_flow_cr = safe_number(cashflow.loc["Free Cash Flow"].iloc[0], crore)
    except Exception:
        pass

    return {
        "company": company,
        "ticker": ticker,
        "sector_input": input_row.get("sector", ""),
        "industry_input": input_row.get("industry", ""),
        "sector_yahoo": info.get("sector", ""),
        "industry_yahoo": info.get("industry", ""),
        "strategic_fit_score": input_row.get("strategic_fit_score", np.nan),
        "why_fit": input_row.get("why_fit", ""),
        "market_cap_cr": market_cap_cr,
        "enterprise_value_cr": enterprise_value_cr,
        "revenue_ttm_cr": revenue_ttm_cr,
        "revenue_growth_pct": revenue_growth_pct,
        "ebitda_margin_pct": ebitda_margin_pct,
        "free_cash_flow_cr": free_cash_flow_cr,
        "debt_to_equity": debt_to_equity,
        "roe_pct": roe_pct,
        "ev_to_revenue": ev_to_revenue,
        "ev_to_ebitda": ev_to_ebitda,
        "data_source": "Yahoo Finance via yfinance",
    }


def main():
    universe = pd.read_csv(INPUT_FILE)
    rows = []
    for _, input_row in universe.iterrows():
        rows.append(row_from_yfinance(input_row))
        time.sleep(0.25)  # Be polite to public data endpoint.

    df = pd.DataFrame(rows)
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved raw public data to: {OUTPUT_FILE}")
    print("Next run: python src/02_score_targets.py")


if __name__ == "__main__":
    main()
