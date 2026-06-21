# 🍳 Cloud Kitchen P&L Dashboard

An interactive Streamlit dashboard for analyzing the profit & loss performance of 50+ cloud kitchen stores across 4 cities — built to turn raw kitchen-level financials into store comparisons, variance tracking, and actionable business insights.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

<!-- 📸 Add a screenshot or GIF of the dashboard here -->
<!-- ![dashboard preview](assets/preview.gif) -->

---

## 🧭 Overview

Cloud kitchen operators run dozens of stores across cities, each with different revenue cohorts, EBITDA margins, and discount behavior. This dashboard consolidates that into three focused views so stakeholders can spot underperformers, track variance month-over-month, and act on data-backed recommendations — without digging through spreadsheets.

## ✨ Features

**📊 Dashboard 1 — Kitchen PNL**
- 8 cross-filters: store, city, zone, month, revenue cohort, EBITDA category/cohort, CM cohort
- 3 range sliders: net revenue, EBITDA, contribution margin
- Live KPIs: total net revenue, total orders, average GM%, average EBITDA%, active store count
- Top 10 stores by revenue & by EBITDA (bar charts)
- Monthly trends for revenue, discount %, and order count (line charts)
- "Kitchen Snapshot" — a multi-metric pivot table (revenue, EBITDA, GM%, CM%, EBITDA margin%) by store × month
- One-click CSV export of the filtered view

**📈 Dashboard 2 — Variance PNL**
- Filters by variance category, month, city, and zone
- Variance % by revenue cohort, tracked month-over-month
- Store count by revenue cohort, to see how the store mix shifts over time

**💡 Dashboard 3 — Business Insights**
A set of written observations and implications derived directly from the data, including:
- A small group of stores drives a disproportionate share of total revenue
- Pune shows weaker revenue than Mumbai but stronger EBITDA margins — better cost discipline despite lower scale
- January 2024 grew profit via a higher Average Order Value, not more orders — pointing to upselling/menu mix over volume
- Discounting increases order count but shows only a moderate link to revenue — a sign of margin being traded for volume without real growth
- Gross margin and EBITDA are almost perfectly correlated (0.99), while AOV and order count are nearly independent (-0.03) — profitability levers and volume levers can be pulled separately

## 🛠️ Tech Stack

- **Streamlit** — app framework & UI
- **Pandas** — data wrangling, pivoting, aggregation
- **Plotly Express** — interactive charts

## 🚀 Running Locally

```bash
git clone https://github.com/sonalbadapure-droid/cloud-kitchen-pnl-dashboard.git
cd cloud-kitchen-pnl-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure

```
cloud-kitchen-pnl-dashboard/
├── app.py                     # Main Streamlit app (3 dashboards)
├── kitchen_pnl_cleaned.csv    # Cleaned input dataset
├── Data/
│   └── Logo.jpg                # Sidebar logo / page icon
├── notebooks/
│   └── eda.ipynb               # Exploratory data analysis
├── requirements.txt
└── README.md
```

## 🔗 Live Demo

<!-- Add your Streamlit Community Cloud link once deployed -->
Coming soon — deployed via Streamlit Community Cloud.
