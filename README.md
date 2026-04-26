# ACC102:ESG-Explorer-S&P-500-Dashboard-Analysis
This project was built for the ACC102 Mini Assignment (Track 4) at Xi'an Jiaotong-Liverpool University, April 2026.

ESG Explorer is an interactive Streamlit dashboard that evaluates the Environmental, Social,  and Governance (ESG) performance of S&amp;P 500 companies. Key features allow users to spot sector risk trends, compare companies under different weighting schemes, and dive deep into specific tickers.

# ESG Explorer: Interactive S&P 500 ESG Dashboard

## 1. Problem Statement & Target User
### Why This Project?
Most ESG ratings are static, one-number scores that hide which pillar (Environment, Social, or Governance) drives the overall risk. Investors rarely get a tool to explore the data through their own lens or adjust the weighting of each pillar. This dashboard is built for individual investors, finance students, and anyone wanting to interactively compare S&P 500 companies on sustainability without needing advanced technical skills.

### Core Questions This Tool Answers
1. How do sectors differ across Environment, Social, and Governance dimensions?
2. Which companies are ESG leaders or laggards in their industry?
3. If an investor prioritises Governance (higher weight), which companies become more attractive?
   

## 2. Data

| Item | Detail |
|------|--------|
| **Source** | Kaggle — "S&P 500 ESG Risk Ratings" |
| **Access Date** | April 2026 |
| **Key Fields** |Symbol, Name, Sector, Total ESG Risk Score, Environment Risk Score, Social Risk Score, Governance Risk Score, ROE, Dividend Yield|
|**Scope**|roughly 500 S&P 500 constituents across all GICS sectors|


## 3. Methods
The project follows a Python pipeline: load, clean, engineer features, visualize, and deploy.

- Smart column matching – A keyword-based function find_col() automatically maps CSV headers to standard variables, making the code robust to formatting variations.
- Data cleaning – Removes currency symbols, commas, and extra spaces; converts columns to numeric types; fills missing values with the median.
- Feature engineering – Creates industry-relative scores (groupby transform), ESG risk categories (Negligible to Severe), a custom governance-weighted composite score (Gov 40%, Env 35%, Social 25%), and rank-shift metrics.
- Visualization – Interactive Plotly Express charts: box plots, grouped bar charts, radar charts, and a correlation heatmap.
- Interactive dashboard – A Streamlit app with filters for sector and risk category, a company search bar, five analysis tabs, metric cards, and a CSV download.


## 4. Key Findings

The dashboard reveals several useful insights.
1. ESG risk differs clearly across sectors. Energy companies tend to have higher environmental risk scores, which reflects exposure to carbon emissions and regulatory pressure. Technology companies show relatively higher social risk in some cases, which may relate to data privacy and labour practices.
2. The relationship between ESG scores and short-term financial performance is weak. The correlation heatmap shows very low linear association between ESG scores and ROE. This suggests ESG performance is more closely linked to long-term stability rather than immediate profitability.
3. The custom ESG model provides additional perspective. Some companies move significantly in ranking when governance is given more weight. This shows that ESG evaluation depends on how different pillars are prioritised.
4. Sector comparison charts make it easier to understand overall patterns. Users can quickly see how industries differ across environmental, social, and governance dimensions, which supports more informed decision-making.


## 5. Product Link & Demo

GitHub Repository: []
Streamlit Community Cloud[]
Demo Video (Mediasite): [Insert your video link]

Course: ACC102 — AI-Driven Data Analytics
Track: Track 4 — Interactive Data Analysis Tool
Student: [Fanli XU/2469997]
Date: April 2026


## 6. Limitations & Next Steps

This project has several limitations related to data and methodology.

- Earlier attempts to include text-based analysis for detecting greenwashing were limited by small sample size and unclear definitions. This experience showed the importance of matching project design with available data. The current project therefore focuses on structured ESG ratings.
- The dataset is static and reflects a single point in time. It does not capture recent ESG events, policy changes, or company-level updates. Adding real-time data sources would improve the relevance of the analysis.
- The analysis is based on cross-sectional data. It focuses on comparison across companies at one time, which limits the ability to study long-term trends. Future work could include time-series data to track ESG changes over time.
- The custom ESG composite score uses fixed weights. These weights reflect one interpretation of ESG importance and may differ across users. Adding adjustable sliders would allow users to define their own preferences.
- The correlation analysis is simple and does not include deeper statistical models. More advanced methods such as regression analysis could provide stronger insight into the relationship between ESG and financial performance.	


## 7. How to Run
### Prerequisites
Python 3.9+

The CSV file (`SP 500 ESG Risk Ratings.csv`) must be placed in the `/data` folder.

### Steps
```bash
# 1. Clone the repository
git clone [Your GitHub Repository URL]
cd [Your Repository Folder Name]

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
