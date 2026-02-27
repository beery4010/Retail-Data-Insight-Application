# 🛒 Retail Data Insight Application

A Python-based **end-to-end Retail Analytics Application** that performs Exploratory Data Analysis (EDA) on e-commerce transaction data and delivers actionable business intelligence through a structured **3 Level Progressive PDF Reporting Framework**.

---

## 📌 Overview

This project analyzes real-world retail transaction data to uncover revenue trends, identify high-value customers, top performing products and geographic sales patterns all packaged into auto-generated business reports with publication quality visualizations.

---

## ✨ Features

- 📈 **Revenue Trend Analysis** — Monthly and yearly sales performance tracking
- 🌍 **Geographic Intelligence** — Top 10 countries by revenue and customer count
- 👤 **Customer Analytics** — Identify top 10 high-value customers by purchase volume
- 📦 **Product Performance** — Top 10 best-selling products by quantity sold
- 📊 **Quantity vs Revenue Comparison** — Country-level cross-metric analysis
- 🔥 **Correlation Heatmap** — Feature relationship analysis across numerical variables
- 📄 **3-Level PDF Reports** — Progressive reporting from basic to advanced insights
- 🗂️ **Modular Architecture** — Clean separation of data loading, analysis, and reporting
- 📝 **Structured Logging** — Full traceability of application events

---

## 🗂️ Project Structure

```
Retail-Data-Insight-Application/
│
├── main.py                        # Application entry point
├── test.ipynb                     # Jupyter Notebook for testing & exploration
├── requirement.txt                # Project dependencies
├── user_instruction.txt           # instruction used in cli
│
├── Level_1_Report.pdf             # Basic metrics and summary report
├── Level_2_Report.pdf             # Trend analysis report
├── Level_3_Report.pdf             # Advanced insights report
│
├── Core/
│   ├── __init__.py
│   ├── data_loader.py             # Data ingestion and preprocessing
│   ├── report_generator.py        # PDF report generation
│   ├── utils.py                   # Helper and utility functions
│   └── logger.py                  # Logging configuration
│
├── Data/
│   ├── 1. monthly_revenue_plot.png
│   ├── 2. yearly_revenue_plot.png
│   ├── 3. top_10_country_by_revenue.png
│   ├── 4. top_10_customer_by_purchase.png
│   ├── 5. top_10_country_by_no_of_customers.png
│   ├── 6. top_10_country_quantity_vs_revenue.png
│   ├── 7. top_10_product_by_quantity_sold.png
│   └── 8. correlation_matrix_heatmap.png
│
└── Logs/
    └── log.log                    # Application event logs
```

---

## 📊 Visualizations Generated

| # | Chart | Insight |
|---|-------|---------|
| 1 | Monthly Revenue Plot | Seasonality and monthly sales trends |
| 2 | Yearly Revenue Plot | Year-over-year growth comparison |
| 3 | Top 10 Countries by Revenue | Highest revenue-generating markets |
| 4 | Top 10 Customers by Purchase | High-value customer identification |
| 5 | Top 10 Countries by No. of Customers | Market penetration by geography |
| 6 | Country: Quantity vs Revenue | Revenue efficiency per market |
| 7 | Top 10 Products by Quantity Sold | Best-selling product analysis |
| 8 | Correlation Matrix Heatmap | Feature relationship analysis |

---

## 📄 3-Level Reporting Framework

| Report | Level | Contents |
|--------|-------|----------|
| `Level_1_Report.pdf` | Basic | Data summary, record counts, basic statistics |
| `Level_2_Report.pdf` | Intermediate | Revenue trends, top customers, top products |
| `Level_3_Report.pdf` | Advanced | Geo-analysis, correlation insights, cross-metric comparisons |

---

## ⚙️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core language |
| Pandas | Data manipulation and analysis |
| Matplotlib | Chart and plot generation |
| Seaborn | Statistical visualizations (heatmap) |
| Jupyter Notebook | Interactive testing and exploration |
| Logging | Application event tracking |
| OOP / Modular Design | Clean architecture |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/beery4010/Retail-Data-Insight-Application.git

# Navigate into the project directory
cd Retail-Data-Insight-Application

# Install dependencies
pip install -r requirement.txt
```

### Run the Application

```bash
python main.py
```

Reports will be generated in the root directory and visualizations saved in the `Data/` folder.
