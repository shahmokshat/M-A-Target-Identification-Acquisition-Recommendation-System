# M&A Target Identification & Acquisition Recommendation System

## Project Overview

This project is a finance analytics model designed to identify and rank potential acquisition targets using publicly available financial and market data.

The system simulates the initial screening process used by investment banks, private equity firms, corporate development teams, and consulting firms when evaluating companies for possible acquisition.

Instead of manually analyzing many companies one by one, this project uses a structured scoring framework to evaluate companies based on growth, profitability, valuation, cash flow quality, and financial stability.

---

## Business Problem

Companies often use mergers and acquisitions to grow faster, enter new markets, acquire new capabilities, increase revenue, or strengthen their competitive position.

However, selecting the right acquisition target is difficult because many companies may appear attractive at first glance. A proper screening process must evaluate both financial performance and valuation.

This project solves that problem by creating a data-driven acquisition screening model that ranks companies based on their overall attractiveness as acquisition targets.

---

## Objective

The objective of this project is to build a system that can:

* Collect public financial and market data
* Analyze company-level financial metrics
* Evaluate valuation attractiveness
* Create an acquisition attractiveness score
* Rank companies based on acquisition potential
* Recommend suitable acquisition targets for a strategic buyer

---

## Methodology

The project follows a structured approach similar to the early-stage screening process used in M&A advisory and private equity.

### 1. Company Universe Selection

A set of publicly listed companies is selected from a chosen sector or industry.

Example sectors:

* FMCG
* Retail
* Consumer Goods
* Healthcare
* Technology
* Financial Services

The selected companies form the target universe for acquisition screening.

---

### 2. Data Collection

The model collects publicly available financial and market data.

Possible data sources include:

* Yahoo Finance
* NSE company data
* Company annual reports
* Public financial databases

The dataset may contain the following company-level variables:

* Company name
* Ticker symbol
* Sector
* Industry
* Market capitalization
* Revenue growth
* EBITDA margin
* Net profit margin
* Return on equity
* Return on capital employed
* Debt-to-equity ratio
* Free cash flow
* Price-to-earnings ratio
* EV/EBITDA
* Price-to-book ratio

---

### 3. Data Cleaning

Before scoring, the raw dataset is cleaned and prepared.

This step may include:

* Removing duplicate companies
* Handling missing values
* Converting text values into numeric values
* Standardizing financial ratios
* Removing extreme outliers
* Preparing the final dataset for scoring

---

### 4. Financial Analysis

Each company is evaluated using financial performance indicators.

Companies receive higher scores if they show:

* Strong revenue growth
* Healthy profitability
* Positive cash flow generation
* Reasonable debt levels
* Stable financial performance

Companies receive lower scores if they show:

* Weak profitability
* High leverage
* Poor cash flow generation
* Expensive valuation
* Unstable financial performance

---

### 5. Valuation Analysis

A company may be financially strong but still unattractive if it is too expensive.

Therefore, the model evaluates valuation using common market multiples such as:

* Price-to-Earnings Ratio
* EV/EBITDA
* Price-to-Book Ratio

Companies with reasonable valuations receive better scores than companies that appear overvalued relative to their fundamentals.

---

### 6. Acquisition Attractiveness Score

The project uses a weighted scoring framework to calculate the final acquisition attractiveness score.

Example weight structure:

| Metric Category          | Weight |
| ------------------------ | -----: |
| Growth                   |    30% |
| Profitability            |    25% |
| Cash Flow Quality        |    20% |
| Valuation Attractiveness |    15% |
| Financial Stability      |    10% |

The final score is calculated as:

```text
Acquisition Attractiveness Score =
(Growth Score × 30%) +
(Profitability Score × 25%) +
(Cash Flow Score × 20%) +
(Valuation Score × 15%) +
(Financial Stability Score × 10%)
```

Companies are then ranked from highest to lowest score.

---

## Project Workflow

```text
Raw Company Data
        |
        v
Data Cleaning and Processing
        |
        v
Financial Ratio Analysis
        |
        v
Valuation Analysis
        |
        v
Weighted Scoring Model
        |
        v
Acquisition Target Ranking
        |
        v
Final Recommendation
```

---

## Folder Structure

```text
M-A-Target-Identification-System/
│
├── data/
│   ├── raw/
│   │   └── target_universe.csv
│   │
│   └── processed/
│       └── cleaned_financial_data.csv
│
├── notebooks/
│   └── analysis.ipynb
│
├── src/
│   ├── data_collection.py
│   ├── scoring_model.py
│   └── ranking_engine.py
│
├── outputs/
│   ├── ranked_targets.xlsx
│   └── acquisition_ranking.csv
│
├── README.md
├── requirements.txt
└── LICENSE
```

---

## Technologies Used

* Python
* Pandas
* NumPy
* yFinance
* OpenPyXL
* Excel
* Jupyter Notebook

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/M-A-Target-Identification-System.git
cd M-A-Target-Identification-System
```

### Step 2: Create a Virtual Environment

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Libraries

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install the main libraries manually:

```bash
pip install pandas numpy yfinance openpyxl matplotlib
```

---

## How to Use the Data

### Input Data

The model requires a company universe file.

Place the input file inside:

```text
data/raw/target_universe.csv
```

The input file should contain at least:

```text
Company Name
Ticker
Sector
Industry
```

Example:

| Company Name | Ticker      | Sector         | Industry      |
| ------------ | ----------- | -------------- | ------------- |
| Company A    | COMPANYA.NS | Consumer Goods | FMCG          |
| Company B    | COMPANYB.NS | Consumer Goods | Retail        |
| Company C    | COMPANYC.NS | Consumer Goods | Food Products |

The ticker should follow the format supported by Yahoo Finance. For Indian listed companies, NSE tickers usually end with `.NS`.

Example:

```text
RELIANCE.NS
TATACONSUM.NS
HINDUNILVR.NS
DABUR.NS
MARICO.NS
```

---

## How to Run the Project

### Step 1: Collect Financial Data

Run the data collection script:

```bash
python src/data_collection.py
```

This script fetches financial and market data for the companies listed in `data/raw/target_universe.csv`.

The output is saved in:

```text
data/processed/cleaned_financial_data.csv
```

---

### Step 2: Run the Scoring Model

After collecting and cleaning the data, run:

```bash
python src/scoring_model.py
```

This script calculates individual scores for:

* Growth
* Profitability
* Cash flow quality
* Valuation attractiveness
* Financial stability

It then calculates the final acquisition attractiveness score.

---

### Step 3: Generate Final Ranking

Run:

```bash
python src/ranking_engine.py
```

This script ranks the companies from most attractive to least attractive acquisition targets.

The final ranked output is saved in:

```text
outputs/acquisition_ranking.csv
outputs/ranked_targets.xlsx
```

---

## How the Model Works

The model evaluates each company across five major categories.

### 1. Growth Score

The growth score measures how fast the company is expanding.

Typical metrics:

* Revenue growth
* Sales growth
* EBITDA growth

A company with higher growth receives a higher score.

---

### 2. Profitability Score

The profitability score measures how efficiently the company converts revenue into profit.

Typical metrics:

* EBITDA margin
* Net profit margin
* ROE
* ROCE

A company with stronger profitability receives a higher score.

---

### 3. Cash Flow Score

The cash flow score measures the quality and sustainability of the company's cash generation.

Typical metrics:

* Free cash flow
* Operating cash flow
* Cash conversion

A company with positive and stable cash flows receives a higher score.

---

### 4. Valuation Score

The valuation score checks whether the company is reasonably priced.

Typical metrics:

* P/E ratio
* EV/EBITDA
* Price-to-book ratio

A company with strong fundamentals and reasonable valuation receives a higher score.

---

### 5. Financial Stability Score

The financial stability score measures risk in the company's balance sheet.

Typical metrics:

* Debt-to-equity ratio
* Interest coverage ratio
* Liquidity position

A company with lower leverage and better financial stability receives a higher score.

---

## Output Files

After running the full project, the output folder will contain:

### 1. acquisition_ranking.csv

This file contains the final ranked list of companies.

Typical columns:

```text
Rank
Company Name
Ticker
Sector
Growth Score
Profitability Score
Cash Flow Score
Valuation Score
Financial Stability Score
Final Acquisition Score
Recommendation
```

---

### 2. ranked_targets.xlsx

This Excel file contains the final ranking in a user-friendly format.

It can be used for:

* Reviewing top acquisition targets
* Creating charts
* Preparing presentations
* Shortlisting companies for further analysis

---

## How to Interpret the Results

The companies with the highest acquisition attractiveness scores are the strongest potential acquisition candidates based on the model.

Example:

| Rank | Company   | Final Score | Recommendation |
| ---: | --------- | ----------: | -------------- |
|    1 | Company A |          91 | Strong Target  |
|    2 | Company B |          84 | Good Target    |
|    3 | Company C |          76 | Watchlist      |
|    4 | Company D |          62 | Low Priority   |

### Recommendation Logic

The model can classify companies as:

| Score Range | Recommendation |
| ----------: | -------------- |
|      85–100 | Strong Target  |
|       70–84 | Good Target    |
|       55–69 | Watchlist      |
|    Below 55 | Low Priority   |

---

## Example Use Case

Suppose a large consumer goods company wants to acquire smaller companies in the FMCG or food products sector.

The model can be used to:

1. Create a list of potential target companies.
2. Collect financial and valuation data.
3. Score each company.
4. Rank the companies.
5. Identify the top acquisition candidates.
6. Perform deeper due diligence on the highest-ranked firms.

This helps reduce manual screening time and makes the decision-making process more structured.

---

## Business Applications

This project can be useful in:

### Investment Banking

* M&A target screening
* Deal origination
* Strategic advisory

### Private Equity

* Deal sourcing
* Investment screening
* Target company evaluation

### Corporate Development

* Acquisition strategy
* Competitor analysis
* Expansion planning

### Consulting

* Market consolidation studies
* Industry attractiveness analysis
* Growth strategy projects

---

## Limitations

This model is designed for preliminary screening only.

It does not replace full due diligence.

Important limitations include:

* Public data may be incomplete or delayed
* Financial ratios may vary across industries
* Qualitative factors are not fully captured
* Management quality is not directly measured
* Synergy potential is not fully quantified
* Legal, tax, and regulatory issues are not included

Before making an actual acquisition decision, the shortlisted companies should be analyzed further through detailed due diligence.

---

## Future Improvements

The project can be improved by adding:

* DCF valuation module
* Synergy estimation module
* Industry-specific scoring weights
* Power BI dashboard
* Streamlit web application
* Machine learning-based target prediction
* Qualitative scoring for management quality
* Scenario analysis for different acquisition assumptions
* Peer benchmarking module

---

## Author

**Mokshat Shah**
B.Tech, Engineering Physics
Indian Institute of Technology Roorkee

Interests:

* Investment Banking
* Private Equity
* Corporate Finance
* Valuation
* Strategic Consulting
