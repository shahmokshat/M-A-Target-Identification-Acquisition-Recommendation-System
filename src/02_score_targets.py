"""
02_score_targets.py
Scores acquisition targets using growth, profitability, cash flow, leverage, valuation and strategic fit.

Run:
    python src/02_score_targets.py

Output:
    outputs/acquisition_target_scores.csv
    outputs/acquisition_screen_output.xlsx
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "outputs" / "raw_public_company_data.csv"
SAMPLE_FILE = ROOT / "data" / "sample_illustrative_data.csv"
OUTPUT_CSV = ROOT / "outputs" / "acquisition_target_scores.csv"
OUTPUT_XLSX = ROOT / "outputs" / "acquisition_screen_output.xlsx"

WEIGHTS = {
    "growth_score": 0.25,
    "profitability_score": 0.25,
    "cash_flow_score": 0.15,
    "balance_sheet_score": 0.15,
    "valuation_score": 0.10,
    "strategic_fit_score_scaled": 0.10,
}

HIGHER_IS_BETTER = [
    "revenue_growth_pct",
    "ebitda_margin_pct",
    "free_cash_flow_cr",
    "roe_pct",
    "strategic_fit_score",
]
LOWER_IS_BETTER = [
    "debt_to_equity",
    "ev_to_revenue",
    "ev_to_ebitda",
]


def percentile_score(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    """Convert a metric into a 0-100 percentile score."""
    s = pd.to_numeric(series, errors="coerce")
    # winsorize lightly to reduce outlier impact
    lo, hi = s.quantile(0.05), s.quantile(0.95)
    s = s.clip(lower=lo, upper=hi)
    # fill missing with median so missing data is not automatically zero
    s = s.fillna(s.median())
    ranks = s.rank(pct=True)
    if not higher_is_better:
        ranks = 1 - ranks
    return (ranks * 100).round(1)


def load_data() -> pd.DataFrame:
    if RAW_FILE.exists():
        print(f"Using fetched public data: {RAW_FILE}")
        return pd.read_csv(RAW_FILE)
    print("Fetched data not found. Using illustrative sample data only for demonstration.")
    return pd.read_csv(SAMPLE_FILE)


def score_targets(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for col in HIGHER_IS_BETTER + LOWER_IS_BETTER:
        if col not in df.columns:
            df[col] = np.nan

    df["growth_score"] = percentile_score(df["revenue_growth_pct"], True)
    df["profitability_score"] = (
        0.60 * percentile_score(df["ebitda_margin_pct"], True)
        + 0.40 * percentile_score(df["roe_pct"], True)
    ).round(1)
    df["cash_flow_score"] = percentile_score(df["free_cash_flow_cr"], True)
    df["balance_sheet_score"] = percentile_score(df["debt_to_equity"], False)
    df["valuation_score"] = (
        0.50 * percentile_score(df["ev_to_revenue"], False)
        + 0.50 * percentile_score(df["ev_to_ebitda"], False)
    ).round(1)
    df["strategic_fit_score_scaled"] = (pd.to_numeric(df["strategic_fit_score"], errors="coerce").fillna(5) * 10).clip(0, 100)

    df["acquisition_attractiveness_score"] = sum(
        df[col] * weight for col, weight in WEIGHTS.items()
    ).round(1)

    def recommendation(score):
        if score >= 75:
            return "High priority: shortlist for deeper due diligence"
        if score >= 60:
            return "Medium priority: monitor / diligence selectively"
        return "Low priority: not preferred unless strategic rationale is strong"

    df["recommendation"] = df["acquisition_attractiveness_score"].apply(recommendation)
    df = df.sort_values("acquisition_attractiveness_score", ascending=False)
    df.insert(0, "rank", range(1, len(df) + 1))
    return df


def make_excel(df: pd.DataFrame):
    OUTPUT_XLSX.parent.mkdir(exist_ok=True)
    top10 = df.head(10)

    with pd.ExcelWriter(OUTPUT_XLSX, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Scored Targets", index=False)
        top10.to_excel(writer, sheet_name="Top 10", index=False)

        weights_df = pd.DataFrame([
            ["Growth", "Revenue growth percentile", "25%"],
            ["Profitability", "EBITDA margin + ROE", "25%"],
            ["Cash Flow", "Free cash flow", "15%"],
            ["Balance Sheet", "Low debt/equity", "15%"],
            ["Valuation", "Low EV/Revenue and EV/EBITDA", "10%"],
            ["Strategic Fit", "Buyer-specific fit score", "10%"],
        ], columns=["Bucket", "Metric", "Weight"])
        weights_df.to_excel(writer, sheet_name="Methodology", index=False)

        sources_df = pd.DataFrame([
            ["NSE / Nifty Indices", "Public Indian listed company universe / Nifty 500 lists", "https://www.nseindia.com/static/products-services/indices-nifty500-index"],
            ["Yahoo Finance via yfinance", "Public market and financial data", "https://ranaroussi.github.io/yfinance/"],
        ], columns=["Source", "Use", "URL"])
        sources_df.to_excel(writer, sheet_name="Sources", index=False)

        workbook = writer.book
        header_fmt = workbook.add_format({"bold": True, "bg_color": "#1F4E78", "font_color": "#FFFFFF", "border": 1})
        percent_fmt = workbook.add_format({"num_format": "0.0%"})
        number_fmt = workbook.add_format({"num_format": "#,##0.0"})
        score_fmt = workbook.add_format({"num_format": "0.0"})

        for sheet_name in writer.sheets:
            ws = writer.sheets[sheet_name]
            ws.freeze_panes(1, 0)
            ws.set_row(0, None, header_fmt)
            ws.autofilter(0, 0, 0, 25)
            ws.set_column(0, 0, 6)
            ws.set_column(1, 3, 22)
            ws.set_column(4, 25, 16)

        ws = writer.sheets["Top 10"]
        chart = workbook.add_chart({"type": "bar"})
        chart.add_series({
            "name": "Acquisition Score",
            "categories": ["Top 10", 1, 1, min(10, len(top10)), 1],
            "values": ["Top 10", 1, top10.columns.get_loc("acquisition_attractiveness_score"), min(10, len(top10)), top10.columns.get_loc("acquisition_attractiveness_score")],
        })
        chart.set_title({"name": "Top Acquisition Targets"})
        chart.set_x_axis({"name": "Score"})
        chart.set_y_axis({"name": "Company"})
        chart.set_legend({"none": True})
        ws.insert_chart("AA2", chart)

    print(f"Saved Excel output to: {OUTPUT_XLSX}")


def main():
    df = load_data()
    scored = score_targets(df)
    OUTPUT_CSV.parent.mkdir(exist_ok=True)
    scored.to_csv(OUTPUT_CSV, index=False)
    make_excel(scored)
    print(f"Saved ranked scores to: {OUTPUT_CSV}")
    print("Next run: python src/03_make_resume_bullets.py")


if __name__ == "__main__":
    main()
