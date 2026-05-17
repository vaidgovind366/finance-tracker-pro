## 🏦 Finance Tracker Pro (SaaS Analytics Dashboard)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg)

Finance Tracker Pro is a premium, full-stack personal finance and analytics dashboard. Built with Python and Streamlit, it features a modern SaaS-style UI, custom CSS injections, interactive Plotly visualizations, and AI-driven financial insights.

## ✨ Features
* **Modern UI/UX:** Custom CSS implementation featuring gradient KPI cards, hover states, and responsive design.
* **Smart Analytics Engine:** Generates real-time text insights (e.g., top spending categories, warning alerts, month-over-month trends).
* **Advanced Visualizations:** Utilizing `Plotly Graph Objects` for dynamic area charts, donut distributions, and daily spending heatmaps.
* **Financial Health Scoring:** Custom algorithm that grades your financial health based on income-to-expense ratios.
* **Enterprise Data Grid:** Searchable, sortable transaction ledger with single-click CSV and Excel (`.xlsx`) report exporting.

## 🏗️ System Architecture
```mermaid
graph TD
    A[Streamlit Frontend] --> B[Custom UI/CSS Injector]
    A --> C[Analytics Engine]
    C --> D[Plotly Visualizations]
    A --> E[SQLAlchemy ORM]
    E --> F[(SQLite Database)]