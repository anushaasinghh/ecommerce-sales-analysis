# 📊 E-Commerce Sales Analysis

**Tools:** SQL · Python · Tableau  
**Dataset:** Olist Brazilian E-Commerce (Kaggle, 100k+ rows)

## What I Built
- Queried a 100,000-row retail dataset using SQL (window functions, CTEs)
- Analysed revenue trends, seasonal patterns, and customer segmentation (RFM)
- Built an interactive Tableau dashboard tracking 6 KPIs with drill-down filters
- Found that top 3 return-heavy categories drive 28%+ of all returns

  ##📌 Key Findings
- 📈 **Peak revenue** occurred in Q4 2017 — 38% above annual monthly average
- 🛒 **AOV** held steady at ~R$160 despite volume spikes, indicating healthy pricing
- 👥 **Champions + Loyal** customers = 42% of total revenue despite being 28% of base
- 🔁 Top 3 high-return categories drove **28% of all returns** → SKU rationalisation recommended (~8% margin improvement projected)


## Dashboard
🔗 [View Live on Tableau Public](https://public.tableau.com/views/E-CommerceSalesAnalysis_17803859303110/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link
)

## Project Structure
ecommerce-sales-analysis/
├── sql/           # All SQL queries
├── notebooks/     # EDA + KPI analysis
├── outputs/       # Charts and CSV exports
└── README.md

## Run Locally
```bash
pip install -r requirements.txt
python sql/load_data.py     # builds the SQLite database
python sql/queries.py       # runs all SQL analysis
jupyter notebook            # open notebooks/eda_and_kpis.ipynb
```
