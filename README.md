# ACC102:ESG-Explorer-S&P-500-Dashboard-Analysis
ESG Explorer is an interactive Streamlit dashboard that evaluates the Environmental, Social,  and Governance (ESG) performance of S&amp;P 500 companies. Key features allow users to spot sector risk trends, compare companies under different weighting schemes, and dive deep into specific tickers.
# ESG Explorer: Interactive S&P 500 ESG Dashboard

# ESG Explorer: Interactive S&P 500 ESG Dashboard

## 1. Problem Statement & Target User

### Why This Project?
Most ESG ratings are delivered as static PDF reports or "one-number" scores. An investor looking at a company rated "Medium risk" cannot easily see:
- Which of E, S, or G is dragging the score down?
- Is this company better or worse than its industry peers?
- What happens if I care more about Governance than Environment?

**The Pain Point**: Investors lack a tool that lets them *interact* with ESG data — filter, compare, and re-weight based on their own priorities.

### Target User
- Individual investors who want to align portfolios with personal values.
- ESG analysts who need to quickly screen sectors for strengths and weaknesses.
- Finance students learning how sustainability metrics relate to financial performance.

### Core Questions This Tool Answers
1. How do sectors differ across Environment, Social, and Governance dimensions?
2. Which companies are ESG leaders or laggards in their industry?
3. If an investor prioritises Governance (higher weight), which companies become more attractive?

---

## 2. Data

| Item | Detail |
|------|--------|
| **Source** | Kaggle — "S&P 500 ESG Risk Ratings" |
| **Scope** | ~500 leading US companies across all GICS sectors |
| **Access Date** | April 2026 |
| **Key Fields** | Symbol, Name, Sector, Total ESG Risk Score, Environment Risk Score, Social Risk Score, Governance Risk Score, Market Cap, Dividend Yield, ROE |
| **Why This Dataset?** | S&P 500 is the most widely followed US equity benchmark. Its ESG data is publicly available, covers diverse industries, and includes financial metrics (ROE, dividend yield) for cross-analysis. |

---

## 3. Methodology: Analysis Logic & Workflow

The project follows a **Problem → Data → Clean → Engineer → Analyse → Visualise** pipeline.

### Step 1: Data Loading & Smart Column Matching
- Real-world CSV files often have inconsistent column headers (extra spaces, capitalisation differences).
- I wrote a `find_col()` function that uses keyword search to automatically detect columns like "Total ESG Risk score" regardless of formatting.
- **Why?** This makes the code reusable — if the dataset is updated with slightly different headers, the tool still works.

### Step 2: Data Cleaning
- Removed currency symbols (`$`) and commas from numeric fields using regex.
- Converted columns to numeric types (`pd.to_numeric`).
- Filled missing values with column medians — a robust method that minimises distortion from outliers.
- **Course Link**: Week 2 (data types, type conversion) and Week 5 (pandas cleaning, `fillna`).

### Step 3: Feature Engineering
I created five new analytical dimensions:

| Feature | Method | Purpose |
|---------|--------|---------|
| Industry-relative scores | `groupby('sector').transform('mean')` — compare each company to its sector average | Answers: "Is this company better than peers?" |
| ESG risk category | `if/elif` logic: Negligible/Low/Medium/High/Severe | Makes raw scores human-readable |
| Custom composite score | Weighted formula: Gov×0.40 + Env×0.35 + Social×0.25 | Tests how rankings change when Governance is prioritised |
| Rank shift | `rank()` difference between original and custom scores | Identifies companies undervalued by standard ratings |
| E-G gap | `gov_score - env_score` | Flags companies strong on governance but weak on environment |

- **Course Link**: Week 3 (functions, loops, conditionals) and Week 6 (parameterised logic, reusable functions).

### Step 4: Analysis & Visualisation
| Analysis | Chart Type | What It Reveals |
|----------|-----------|-----------------|
| Sector comparison of E/S/G | Radar Chart (Plotly) | Sectors have uneven ESG profiles — e.g. Utilities weak on E, Financials weak on S |
| Correlation between ESG & ROE | Heatmap | ESG and short-term profitability are nearly uncorrelated (r < 0.1) |
| E vs G relationship | Scatter Plot | Only moderate correlation (~0.35) — good environmental performance doesn't guarantee good governance |
| Top/Bottom 10 companies | Ranked Table | Leaders and laggards identified per dimension |
| Custom weighting impact | Rank-shift Table | Governance-first model surfaces "hidden leaders" |

### Step 5: Interactive Dashboard (Streamlit)
The app wraps the analysis into a user-friendly interface:
- **Sidebar filters**: Sector, risk category, and a company search bar.
- **5 Tabs**: Industry Analysis, Correlation Matrix, Leaders vs Laggards, Custom Model, Raw Data.
- **Download button**: Users can export filtered results as CSV.

---

## 4. Key Findings

- **Sector ESG profiles are highly uneven.** Technology leads in Governance; Utilities lag on Environment; Financials score lowest on Social metrics. This means a one-size-fits-all ESG score hides important structural differences.
- **Environment and Governance are only moderately correlated (r ≈ 0.35).** A company can be excellent at reducing carbon emissions but have weak board independence — or vice versa.
- **ESG total score shows almost no linear relationship with ROE (r < 0.1).** This challenges the common claim that "good ESG means good profits." Instead, ESG likely acts as *downside protection* — reducing risk rather than boosting short-term returns.
- **Changing weights changes rankings.** When Governance is weighted at 40% (vs. equal weighting), several companies with strong management structures rise in rank. A standard rating may undervalue governance quality — important for investors who believe good management drives long-term value.
- **The "E-G gap" reveals interesting outliers.** Some companies have high Governance scores but poor Environmental scores. These firms might face future regulatory risk if carbon disclosure rules tighten.

---

## 5. How to Run

### Prerequisites
- Python 3.9+
- The CSV file (`SP 500 ESG Risk Ratings.csv`) must be placed in the `/data` folder.

### Steps
```bash
# 1. Clone the repository
git clone [Your GitHub Repository URL]
cd [Your Repository Folder Name]

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py1. Problem Statement & Target User

### Why This Project?
Most ESG ratings are delivered as static PDF reports or "one-number" scores. An investor looking at a company rated "Medium risk" cannot easily see:
- Which of E, S, or G is dragging the score down?
- Is this company better or worse than its industry peers?
- What happens if I care more about Governance than Environment?

**The Pain Point**: Investors lack a tool that lets them *interact* with ESG data — filter, compare, and re-weight based on their own priorities.

### Target User
- Individual investors who want to align portfolios with personal values.
- ESG analysts who need to quickly screen sectors for strengths and weaknesses.
- Finance students learning how sustainability metrics relate to financial performance.

### Core Questions This Tool Answers
1. How do sectors differ across Environment, Social, and Governance dimensions?
2. Which companies are ESG leaders or laggards in their industry?
3. If an investor prioritises Governance (higher weight), which companies become more attractive?

---

  2. Data

| Item | Detail |
|------|--------|
| **Source** | Kaggle — "S&P 500 ESG Risk Ratings" |
| **Scope** | ~500 leading US companies across all GICS sectors |
| **Access Date** | April 2026 |
| **Key Fields** | Symbol, Name, Sector, Total ESG Risk Score, Environment Risk Score, Social Risk Score, Governance Risk Score, Market Cap, Dividend Yield, ROE |
| **Why This Dataset?** | S&P 500 is the most widely followed US equity benchmark. Its ESG data is publicly available, covers diverse industries, and includes financial metrics (ROE, dividend yield) for cross-analysis. |

---

## 3. Methodology: Analysis Logic & Workflow

The project follows a **Problem → Data → Clean → Engineer → Analyse → Visualise** pipeline.

### Step 1: Data Loading & Smart Column Matching
- Real-world CSV files often have inconsistent column headers (extra spaces, capitalisation differences).
- I wrote a `find_col()` function that uses keyword search to automatically detect columns like "Total ESG Risk score" regardless of formatting.
- **Why?** This makes the code reusable — if the dataset is updated with slightly different headers, the tool still works.

### Step 2: Data Cleaning
- Removed currency symbols (`$`) and commas from numeric fields using regex.
- Converted columns to numeric types (`pd.to_numeric`).
- Filled missing values with column medians — a robust method that minimises distortion from outliers.
- **Course Link**: Week 2 (data types, type conversion) and Week 5 (pandas cleaning, `fillna`).

### Step 3: Feature Engineering
I created five new analytical dimensions:

| Feature | Method | Purpose |
|---------|--------|---------|
| Industry-relative scores | `groupby('sector').transform('mean')` — compare each company to its sector average | Answers: "Is this company better than peers?" |
| ESG risk category | `if/elif` logic: Negligible/Low/Medium/High/Severe | Makes raw scores human-readable |
| Custom composite score | Weighted formula: Gov×0.40 + Env×0.35 + Social×0.25 | Tests how rankings change when Governance is prioritised |
| Rank shift | `rank()` difference between original and custom scores | Identifies companies undervalued by standard ratings |
| E-G gap | `gov_score - env_score` | Flags companies strong on governance but weak on environment |

- **Course Link**: Week 3 (functions, loops, conditionals) and Week 6 (parameterised logic, reusable functions).

### Step 4: Analysis & Visualisation
| Analysis | Chart Type | What It Reveals |
|----------|-----------|-----------------|
| Sector comparison of E/S/G | Radar Chart (Plotly) | Sectors have uneven ESG profiles — e.g. Utilities weak on E, Financials weak on S |
| Correlation between ESG & ROE | Heatmap | ESG and short-term profitability are nearly uncorrelated (r < 0.1) |
| E vs G relationship | Scatter Plot | Only moderate correlation (~0.35) — good environmental performance doesn't guarantee good governance |
| Top/Bottom 10 companies | Ranked Table | Leaders and laggards identified per dimension |
| Custom weighting impact | Rank-shift Table | Governance-first model surfaces "hidden leaders" |

### Step 5: Interactive Dashboard (Streamlit)
The app wraps the analysis into a user-friendly interface:
- **Sidebar filters**: Sector, risk category, and a company search bar.
- **5 Tabs**: Industry Analysis, Correlation Matrix, Leaders vs Laggards, Custom Model, Raw Data.
- **Download button**: Users can export filtered results as CSV.

---

## 4. Key Findings

- **Sector ESG profiles are highly uneven.** Technology leads in Governance; Utilities lag on Environment; Financials score lowest on Social metrics. This means a one-size-fits-all ESG score hides important structural differences.
- **Environment and Governance are only moderately correlated (r ≈ 0.35).** A company can be excellent at reducing carbon emissions but have weak board independence — or vice versa.
- **ESG total score shows almost no linear relationship with ROE (r < 0.1).** This challenges the common claim that "good ESG means good profits." Instead, ESG likely acts as *downside protection* — reducing risk rather than boosting short-term returns.
- **Changing weights changes rankings.** When Governance is weighted at 40% (vs. equal weighting), several companies with strong management structures rise in rank. A standard rating may undervalue governance quality — important for investors who believe good management drives long-term value.
- **The "E-G gap" reveals interesting outliers.** Some companies have high Governance scores but poor Environmental scores. These firms might face future regulatory risk if carbon disclosure rules tighten.

---

## 5. How to Run

### Prerequisites
- Python 3.9+
- The CSV file (`SP 500 ESG Risk Ratings.csv`) must be placed in the `/data` folder.

### Steps
```bash
# 1. Clone the repository
git clone [Your GitHub Repository URL]
cd [Your Repository Folder Name]

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py

## 6. Product Link & Demo

GitHub Repository: []
Streamlit Community Cloud[]
Demo Video (Mediasite): [Insert your video link]

Course: ACC102 — AI-Driven Data Analytics
Track: Track 4 — Interactive Data Analysis Tool
Student: [Fanli XU/2469997]
Date: April 2026

---

## 7. Limitations & Next Steps

Limitation Why It Matters Next Step
Single snapshot data ESG ratings change over time. This dataset shows one point in time — it cannot show whether a company is improving or deteriorating. Incorporate time-series data from MSCI or Sustainalytics to track ESG momentum.
Rating methodology is not transparent Different ESG providers rate the same company differently. Findings may not generalise to other rating frameworks. Compare results using data from multiple agencies (e.g., Refinitiv vs. MSCI).
No Scope 3 emissions The Environment score does not include supply-chain carbon (Scope 3), which is often the largest source of emissions for many sectors. Integrate CDP (Carbon Disclosure Project) Scope 3 data.
Correlation is not causation The weak ESG-ROE correlation does not prove ESG has no financial impact — it may be masked by other variables. Add control variables (size, leverage, industry) and run panel regressions for more rigorous testing.
Custom weights are fixed The 40/35/25 weighting is one viewpoint (governance-focused). Users cannot yet set their own weights. Add sliders in the Streamlit app so users can define their own E/S/G priorities.
US-only focus S&P 500 covers only US large-caps. Results may not apply to emerging markets or small-cap companies. Extend analysis to include MSCI World or CSI 300 (China A-shares) for cross-market comparison.

---

This project was built for the ACC102 Mini Assignment (Track 4) at Xi'an Jiaotong-Liverpool University, April 2026.
