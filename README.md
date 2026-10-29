<div align="center">

# 📊 Sales Data Analysis Dashboard

An interactive, beginner-friendly business intelligence and sales analytics dashboard built with **Python**, **Pandas**, **Matplotlib**, and **Streamlit**.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8%2B-11557C.svg)](https://matplotlib.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production--Ready-success.svg)]()

<br />

> **Instant Insights Out of the Box:** Automatically loads realistic sample sales data on launch, and seamlessly lets you upload and analyze custom CSV files with dynamic filtering and visualizations.

---

</div>

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Live Dashboard Layout](#-live-dashboard-layout)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Run (Step-by-Step)](#installation--run-step-by-step)
- [Dataset Specifications](#-dataset-specifications)
- [Business Metrics & Calculations](#-business-metrics--calculations)
- [Custom CSV Upload Requirements](#-custom-csv-upload-requirements)
- [Troubleshooting & FAQs](#-troubleshooting--faqs)
- [License](#-license)

---

## 🚀 Overview

The **Sales Data Analysis Dashboard** bridges the gap between raw spreadsheet data and executive-level business intelligence. Without requiring external database setups, cloud credentials, or complex configurations, this dashboard allows anyone to explore sales trends, top-performing products, category revenues, and order volume in real-time.

```
       ┌────────────────────────┐
       │   sales.csv / Upload   │
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │  Pandas Cleaning &     │
       │  Revenue Calculation   │
       └───────────┬────────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
   ┌───────────┐       ┌───────────┐
   │ 5 Top KPI │       │     4     │
   │  Metrics  │       │Matplotlib │
   │   Cards   │       │  Charts   │
   └───────────┘       └───────────┘
```

---

## ✨ Key Features

- **⚡ Instant Out-of-the-Box Execution**: Comes pre-packaged with `sales.csv` containing 65+ realistic transaction records across multiple categories and months.
- **📁 Custom CSV Upload**: Effortlessly upload your own sales records directly through the sidebar.
- **🏷️ Dynamic Category Filtering**: Filter the entire dashboard by product category; all statistics, charts, and table rows update instantly.
- **📌 Executive KPI Cards**:
  - **Total Revenue**: Cumulative revenue calculated as `Quantity × Unit_Price`.
  - **Total Orders**: Count of unique completed orders.
  - **Units Sold**: Total volume of physical items purchased.
  - **Average Order Value (AOV)**: Revenue per completed order.
  - **Best-Selling Product**: Highest revenue-generating product and its total.
- **📊 4 Specialized Visualizations (Matplotlib)**:
  1. **Revenue by Product**: Sorted horizontal bar chart with exact revenue labels.
  2. **Revenue by Category**: Categorical revenue breakdown with custom color-coding.
  3. **Monthly Sales Trend**: Time-series line chart tracking monthly performance.
  4. **Category Revenue Share**: Clean donut/pie chart detailing revenue distribution.
- **🛡️ Graceful Error Handling & Data Validation**: Auto-detects missing columns, scrubs whitespace, coerces numeric strings, and gracefully drops corrupted rows with user feedback.
- **📥 CSV Export**: Filter your records and download the cleaned subset with a single click.

---

## 🖥️ Live Dashboard Layout

| Area | Component | Description |
| :--- | :--- | :--- |
| **Sidebar** | File Uploader | Drag & drop custom CSV files or retain default sample data. |
| **Sidebar** | Category Selector | Dropdown to filter records across all metrics & charts. |
| **Sidebar** | Dataset Status Badge | Real-time indicator of whether sample or uploaded data is active. |
| **Top Bar** | 5 KPI Cards | Revenue, Orders, Units Sold, Average Order Value, Top Product. |
| **Main Grid** | 2x2 Visualizations | Clean 2-column Matplotlib charts layout with formatted currency axes. |
| **Bottom** | Data Table & Export | Filtered tabular view with search, sort, and one-click CSV download. |

---

## 📂 Project Structure

```
sales-analysis/
├── app.py              # Main Streamlit web application & data pipeline
├── sales.csv           # Bundled realistic sample dataset (65+ records)
├── requirements.txt    # Python package dependencies
└── README.md           # Modern project documentation
```

---

## 🛠️ Getting Started

### Prerequisites

- **Python 3.9+** (Tested on Python 3.9, 3.10, 3.11, 3.12, 3.13)
- Command-line terminal (PowerShell, Command Prompt, Bash, or Zsh)

### Installation & Run (Step-by-Step)

#### 1. Navigate to the project directory
```bash
cd sales-analysis
```

#### 2. (Recommended) Create and activate a virtual environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(Or with the Python Launcher: `py -m venv venv`)*

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install required dependencies
```bash
pip install -r requirements.txt
```

#### 4. Launch the dashboard
```bash
streamlit run app.py
```
*(Or via Python module: `python -m streamlit run app.py`)*

The application will immediately open in your default browser at:
👉 **`http://localhost:8501`**

---

## 📊 Dataset Specifications

The included sample dataset (`sales.csv`) contains verified synthetic records clearly marked as sample data:

| Column | Data Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `Order_ID` | String | `ORD-1001` | Unique order identifier |
| `Order_Date` | Date (`YYYY-MM-DD`) | `2024-01-15` | Date the transaction took place |
| `Product` | String | `Wireless Headphones` | Name of the product sold |
| `Category` | String | `Electronics` | Category grouping |
| `Quantity` | Integer | `2` | Number of items purchased |
| `Unit_Price` | Float | `99.99` | Price per single unit in USD |

---

## 🧮 Business Metrics & Calculations

$$\text{Revenue} = \text{Quantity} \times \text{Unit\_Price}$$

$$\text{Total Revenue} = \sum \text{Revenue}$$

$$\text{Average Order Value (AOV)} = \frac{\text{Total Revenue}}{\text{Total Unique Orders}}$$

$$\text{Best-Selling Product} = \arg\max_{P} \left( \sum_{i \in P} \text{Revenue}_i \right)$$

---

## 📤 Custom CSV Upload Requirements

You can upload your own sales records via the sidebar! Ensure your CSV file includes these 6 header names (case-insensitive):

```csv
Order_ID,Order_Date,Product,Category,Quantity,Unit_Price
INV-001,2024-05-10,Mechanical Keyboard,Office Supplies,2,85.00
INV-002,2024-05-12,4K Monitor,Electronics,1,389.00
```

> [!NOTE]
> - Dates should be in a standard recognizable format (`YYYY-MM-DD` or `MM/DD/YYYY`).
> - Quantities and Unit Prices must be positive numeric values.
> - Any rows with invalid dates or non-numeric prices will be gracefully caught and cleaned with a friendly notification.

---

## ❓ Troubleshooting & FAQs

<details>
<summary><b>1. Streamlit command is not recognized?</b></summary>

If `streamlit` is not recognized on your system PATH, use Python's `-m` switch:
```bash
# Windows
py -m streamlit run app.py

# macOS / Linux
python3 -m streamlit run app.py
```
</details>

<details>
<summary><b>2. How can I change the default port?</b></summary>

You can specify a custom port by passing `--server.port`:
```bash
streamlit run app.py --server.port 8080
```
</details>

<details>
<summary><b>3. Does this app require internet access or API keys?</b></summary>

No! The dashboard runs 100% locally on your machine with zero external API calls or database dependencies.
</details>

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Free for personal, educational, and commercial use.
