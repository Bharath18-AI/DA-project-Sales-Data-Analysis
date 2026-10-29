"""
Sales Data Analysis Dashboard
=============================
A beginner-friendly, interactive business intelligence dashboard built with
Python, Pandas, Matplotlib, and Streamlit.

Features:
- Instant launch with bundled sample data (sales.csv)
- CSV upload support for custom datasets
- Dynamic KPI metrics (Revenue, Orders, Units, AOV, Best Seller)
- 4 Matplotlib charts (Product Revenue, Category Revenue, Monthly Trend, Revenue Share)
- Dynamic Category filtering
- Interactive data table with search and CSV export
- Graceful error handling and data validation
"""

import os
from typing import Dict, Optional, Tuple
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern card styling and visual appeal
st.markdown(
    """
    <style>
        /* Clean header styling */
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1E293B;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1rem;
            color: #64748B;
            margin-bottom: 1.5rem;
        }
        /* Metric container styling */
        div[data-testid="stMetric"] {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            padding: 1rem 1.2rem;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08);
        }
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #F1F5F9;
        }
        /* Chart container */
        .chart-box {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Color palettes for Matplotlib charts
COLOR_PRIMARY = "#2563EB"       # Royal Blue
COLOR_ACCENT = "#3B82F6"        # Dodger Blue
PALETTE = ["#2563EB", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4", "#EC4899"]


# -----------------------------------------------------------------------------
# 2. DATA LOADING & VALIDATION FUNCTIONS
# -----------------------------------------------------------------------------
REQUIRED_COLUMNS = ["Order_ID", "Order_Date", "Product", "Category", "Quantity", "Unit_Price"]


def load_data(file_source) -> Optional[pd.DataFrame]:
    """
    Reads a CSV file from a path or file-like buffer into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_source)
        return df
    except Exception as e:
        st.error(f"⚠️ Error reading CSV file: {e}")
        return None


def validate_and_clean_data(df: pd.DataFrame) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Validates column structure, cleans data, handles missing values,
    and computes the Revenue column.

    Returns:
        (cleaned_df, warning_message) or (None, error_message)
    """
    if df is None or df.empty:
        return None, "The uploaded file contains no data."

    # Standardize column names (strip whitespace)
    df.columns = [c.strip() for c in df.columns]

    # Check for missing required columns (case-insensitive check)
    col_mapping = {}
    lower_df_cols = {c.lower(): c for c in df.columns}
    missing_cols = []

    for req in REQUIRED_COLUMNS:
        if req.lower() in lower_df_cols:
            col_mapping[lower_df_cols[req.lower()]] = req
        else:
            missing_cols.append(req)

    if missing_cols:
        error_msg = (
            f"Missing required column(s): **{', '.join(missing_cols)}**.\\n\\n"
            f"Expected schema: `{', '.join(REQUIRED_COLUMNS)}`"
        )
        return None, error_msg

    # Rename matched columns to canonical names
    df = df.rename(columns=col_mapping).copy()

    # Track missing values
    initial_rows = len(df)
    missing_count = df[REQUIRED_COLUMNS].isnull().any(axis=1).sum()

    # Drop rows where critical fields are null
    df = df.dropna(subset=REQUIRED_COLUMNS).copy()

    # Convert Quantity and Unit_Price to numeric (coerce errors into NaN and drop)
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
    df = df.dropna(subset=["Quantity", "Unit_Price"]).copy()

    # Keep only positive quantities and prices
    df = df[(df["Quantity"] > 0) & (df["Unit_Price"] >= 0)].copy()

    # Convert Order_Date to datetime
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df = df.dropna(subset=["Order_Date"]).copy()

    # Clean text columns
    df["Product"] = df["Product"].astype(str).str.strip()
    df["Category"] = df["Category"].astype(str).str.strip()
    df["Order_ID"] = df["Order_ID"].astype(str).str.strip()

    # Calculate Revenue: Quantity × Unit_Price
    df["Revenue"] = df["Quantity"] * df["Unit_Price"]

    if df.empty:
        return None, "No valid data rows remaining after cleaning. Please check your data."

    warning_msg = None
    dropped_rows = initial_rows - len(df)
    if dropped_rows > 0:
        warning_msg = f"Cleaned {dropped_rows} row(s) containing missing or invalid values."

    return df, warning_msg


# -----------------------------------------------------------------------------
# 3. KPI METRICS CALCULATION
# -----------------------------------------------------------------------------
def calculate_kpis(df: pd.DataFrame) -> Dict:
    """
    Calculates summary business performance indicators.
    """
    total_revenue = df["Revenue"].sum()
    total_orders = df["Order_ID"].nunique()
    total_units = int(df["Quantity"].sum())
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0

    # Best-selling product by revenue
    product_revenue = df.groupby("Product")["Revenue"].sum()
    if not product_revenue.empty:
        best_product = product_revenue.idxmax()
        best_product_rev = product_revenue.max()
    else:
        best_product = "N/A"
        best_product_rev = 0.0

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_units": total_units,
        "avg_order_value": avg_order_value,
        "best_product": best_product,
        "best_product_rev": best_product_rev,
    }


# -----------------------------------------------------------------------------
# 4. DATA VISUALIZATION FUNCTIONS (MATPLOTLIB)
# -----------------------------------------------------------------------------
def plot_revenue_by_product(df: pd.DataFrame) -> plt.Figure:
    """
    Horizontal bar chart showing revenue generated by each product.
    """
    prod_rev = df.groupby("Product")["Revenue"].sum().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(7, 4.8), dpi=100)
    bars = ax.barh(prod_rev.index, prod_rev.values, color="#3B82F6", edgecolor="#1D4ED8", height=0.6)

    ax.set_title("Total Revenue by Product", fontsize=13, fontweight="bold", pad=12, color="#1E293B")
    ax.set_xlabel("Revenue (USD)", fontsize=10, fontweight="bold", color="#475569")
    ax.set_ylabel("Product", fontsize=10, fontweight="bold", color="#475569")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Add data labels at the end of each bar
    max_val = prod_rev.max() if not prod_rev.empty else 0
    for bar in bars:
        width = bar.get_width()
        ax.annotate(
            f" ${width:,.0f}",
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(3, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=8.5,
            color="#1E293B",
            fontweight="bold",
        )

    # Provide head space for text annotations
    if max_val > 0:
        ax.set_xlim(0, max_val * 1.18)

    fig.tight_layout()
    return fig


def plot_revenue_by_category(df: pd.DataFrame) -> plt.Figure:
    """
    Vertical bar chart showing revenue by product category.
    """
    cat_rev = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(7, 4.8), dpi=100)
    colors = PALETTE[: len(cat_rev)]
    bars = ax.bar(cat_rev.index, cat_rev.values, color=colors, edgecolor="#334155", width=0.55)

    ax.set_title("Revenue by Product Category", fontsize=13, fontweight="bold", pad=12, color="#1E293B")
    ax.set_xlabel("Category", fontsize=10, fontweight="bold", color="#475569")
    ax.set_ylabel("Revenue (USD)", fontsize=10, fontweight="bold", color="#475569")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(rotation=15, ha="right")

    # Add data labels on top of each bar
    max_val = cat_rev.max() if not cat_rev.empty else 0
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"${height:,.0f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#1E293B",
            fontweight="bold",
        )

    if max_val > 0:
        ax.set_ylim(0, max_val * 1.15)

    fig.tight_layout()
    return fig


def plot_monthly_trend(df: pd.DataFrame) -> plt.Figure:
    """
    Line chart showing sales revenue trend over months.
    """
    temp_df = df.copy()
    temp_df["YearMonth"] = temp_df["Order_Date"].dt.to_period("M")
    monthly = temp_df.groupby("YearMonth")["Revenue"].sum().reset_index()
    monthly["Period_Str"] = monthly["YearMonth"].astype(str)

    fig, ax = plt.subplots(figsize=(7, 4.8), dpi=100)
    ax.plot(
        monthly["Period_Str"],
        monthly["Revenue"],
        marker="o",
        linewidth=2.5,
        markersize=6,
        color="#2563EB",
        label="Monthly Revenue",
    )
    ax.fill_between(monthly["Period_Str"], monthly["Revenue"], color="#93C5FD", alpha=0.3)

    ax.set_title("Monthly Sales Revenue Trend", fontsize=13, fontweight="bold", pad=12, color="#1E293B")
    ax.set_xlabel("Month", fontsize=10, fontweight="bold", color="#475569")
    ax.set_ylabel("Revenue (USD)", fontsize=10, fontweight="bold", color="#475569")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(rotation=35, ha="right")

    # Annotate points
    for _, row in monthly.iterrows():
        ax.annotate(
            f"${row['Revenue']:,.0f}",
            xy=(row["Period_Str"], row["Revenue"]),
            xytext=(0, 7),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            fontweight="bold",
            color="#1E3A8A",
        )

    max_val = monthly["Revenue"].max() if not monthly.empty else 0
    if max_val > 0:
        ax.set_ylim(0, max_val * 1.18)

    fig.tight_layout()
    return fig


def plot_category_pie(df: pd.DataFrame) -> plt.Figure:
    """
    Pie chart showing each category's share of total revenue.
    """
    cat_rev = df.groupby("Category")["Revenue"].sum()

    fig, ax = plt.subplots(figsize=(7, 4.8), dpi=100)
    colors = PALETTE[: len(cat_rev)]

    wedges, texts, autotexts = ax.pie(
        cat_rev.values,
        labels=cat_rev.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.75, edgecolor="white", linewidth=2),
        pctdistance=0.75,
    )

    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(9.5)
        autotext.set_weight("bold")

    for text in texts:
        text.set_fontsize(9.5)
        text.set_color("#1E293B")

    ax.set_title("Revenue Share by Category", fontsize=13, fontweight="bold", pad=12, color="#1E293B")
    fig.tight_layout()
    return fig


# -----------------------------------------------------------------------------
# 5. MAIN APPLICATION
# -----------------------------------------------------------------------------
def main():
    # Header Section
    st.markdown('<div class="main-header">📈 Sales Performance Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Interactive analytics tool to track business revenue, order volume, and category trends.</div>',
        unsafe_allow_html=True,
    )

    # Determine default sample dataset location
    app_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file_path = os.path.join(app_dir, "sales.csv")

    # -------------------------------------------------------------------------
    # SIDEBAR: DATA INPUT & FILTERS
    # -------------------------------------------------------------------------
    st.sidebar.header("⚙️ Dashboard Controls")

    # 1. File Upload
    st.sidebar.subheader("1. Data Source")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Sales CSV",
        type=["csv"],
        help="Upload your custom sales data CSV file with columns: Order_ID, Order_Date, Product, Category, Quantity, Unit_Price",
    )

    is_sample_data = uploaded_file is None
    data_source_name = "Sample Dataset (sales.csv)" if is_sample_data else f"Uploaded: {uploaded_file.name}"

    # Load raw data
    if is_sample_data:
        if not os.path.exists(sample_file_path):
            st.error(f"Sample data file not found at `{sample_file_path}`. Please upload a CSV file.")
            st.stop()
        raw_df = load_data(sample_file_path)
    else:
        raw_df = load_data(uploaded_file)

    if raw_df is None:
        st.stop()

    # Validate and clean data
    cleaned_df, cleaning_notice = validate_and_clean_data(raw_df)
    if cleaned_df is None:
        st.error(f"❌ Data Validation Error: {cleaning_notice}")
        st.info("💡 Please make sure your CSV contains: Order_ID, Order_Date, Product, Category, Quantity, Unit_Price")
        st.stop()

    if cleaning_notice:
        st.sidebar.warning(cleaning_notice)

    # Data Source Status Indicator
    st.sidebar.info(f"📂 **Active Dataset:** {data_source_name}")
    if is_sample_data:
        st.sidebar.caption("ℹ️ *Currently displaying bundled sample data. Upload your own CSV above to analyze custom data.*")

    # 2. Category Filter
    st.sidebar.subheader("2. Filter Category")
    available_categories = ["All Categories"] + sorted(cleaned_df["Category"].unique().tolist())
    selected_category = st.sidebar.selectbox(
        "Select Category",
        options=available_categories,
        index=0,
        help="Filter the entire dashboard by product category.",
    )

    # Apply Category Filter
    if selected_category == "All Categories":
        filtered_df = cleaned_df.copy()
    else:
        filtered_df = cleaned_df[cleaned_df["Category"] == selected_category].copy()

    if filtered_df.empty:
        st.warning(f"No records found for category '{selected_category}'.")
        st.stop()

    # -------------------------------------------------------------------------
    # TOP KPI METRIC CARDS
    # -------------------------------------------------------------------------
    kpis = calculate_kpis(filtered_df)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="💵 Total Revenue",
            value=f"${kpis['total_revenue']:,.2f}",
            help="Sum of (Quantity × Unit Price) for all matching orders",
        )
    with col2:
        st.metric(
            label="📦 Total Orders",
            value=f"{kpis['total_orders']:,}",
            help="Total number of unique orders placed",
        )
    with col3:
        st.metric(
            label="🛍️ Units Sold",
            value=f"{kpis['total_units']:,}",
            help="Cumulative quantity of units purchased across products",
        )
    with col4:
        st.metric(
            label="🏷️ Average Order Value",
            value=f"${kpis['avg_order_value']:,.2f}",
            help="Total Revenue divided by Total Orders",
        )
    with col5:
        st.metric(
            label="🏆 Best-Selling Product",
            value=kpis["best_product"],
            delta=f"${kpis['best_product_rev']:,.0f} rev",
            help="Product generating the highest revenue",
        )

    st.markdown("---")

    # -------------------------------------------------------------------------
    # VISUALIZATION CHARTS (2x2 GRID)
    # -------------------------------------------------------------------------
    st.subheader(f"📊 Business Visualizations ({selected_category})")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Chart 1: Bar Chart - Revenue by Product
        fig_prod = plot_revenue_by_product(filtered_df)
        st.pyplot(fig_prod)
        plt.close(fig_prod)

        # Chart 3: Line Chart - Monthly Sales Trend
        fig_trend = plot_monthly_trend(filtered_df)
        st.pyplot(fig_trend)
        plt.close(fig_trend)

    with chart_col2:
        # Chart 2: Bar Chart - Revenue by Category
        # If a single category is selected, also show comparison or single bar
        fig_cat = plot_revenue_by_category(filtered_df)
        st.pyplot(fig_cat)
        plt.close(fig_cat)

        # Chart 4: Pie Chart - Category Share of Revenue
        # Note: If single category is filtered, show its share across all categories or alert
        if selected_category == "All Categories":
            fig_pie = plot_category_pie(cleaned_df)
            st.pyplot(fig_pie)
            plt.close(fig_pie)
        else:
            # When filtered, show category share in context of full dataset
            fig_pie = plot_category_pie(cleaned_df)
            st.pyplot(fig_pie)
            plt.close(fig_pie)
            st.caption(f"*Pie chart shows category revenue distribution across the entire dataset.*")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # DATA TABLE & EXPORT SECTION
    # -------------------------------------------------------------------------
    st.subheader("📋 Detailed Sales Records")

    # Format dataframe for clean display
    display_df = filtered_df.copy()
    display_df["Order_Date"] = display_df["Order_Date"].dt.strftime("%Y-%m-%d")
    display_df["Unit_Price"] = display_df["Unit_Price"].apply(lambda x: f"${x:,.2f}")
    display_df["Revenue"] = display_df["Revenue"].apply(lambda x: f"${x:,.2f}")

    table_col1, table_col2 = st.columns([4, 1])
    with table_col1:
        st.caption(f"Showing **{len(filtered_df)}** records for **{selected_category}**")
    with table_col2:
        # CSV Download Button
        csv_export = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv_export,
            file_name=f"sales_data_{selected_category.lower().replace(' ', '_')}.csv",
            mime="text/csv",
        )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )


if __name__ == "__main__":
    main()
