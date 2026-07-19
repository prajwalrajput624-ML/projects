"""
Sales Insights Dashboard
-------------------------
Streamlit dashboard built from precomputed sales analytics
(2,739 records, order dates 02/01/2014 - 11/12/2017).

Run:
    pip install streamlit pandas plotly
    streamlit run app.py
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sales Insights Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# STYLING
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main > div {padding-top: 1.2rem;}
    div[data-testid="stMetric"] {
        background-color: #f8f9fb;
        border: 1px solid #e6e6e6;
        border-radius: 10px;
        padding: 14px 16px 8px 16px;
    }
    div[data-testid="stMetricLabel"] {font-weight: 600; color: #555;}
    h1, h2, h3 {color: #1f2937;}
    .stTabs [data-baseweb="tab-list"] {gap: 4px;}
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# STATIC DATA (from the precomputed SQL analysis)
# ----------------------------------------------------------------------------

DATASET_META = {
    "records": 2739,
    "order_start": "2014-01-02",
    "order_end": "2017-12-11",
    "ship_start": "2014-02-05",
    "ship_end": "2017-12-12",
    "sales_avg": 230.9713,
    "sales_median": 58.24,
    "avg_median_diff": 172.7313,
    "size_kb": 1544,
    "top_category": "Office Supplies",
    "top_subcategory": "Binders",
    "most_frequent_product": "Easy Staple Paper",
    "most_frequent_product_qty": 21,
}

category_df = pd.DataFrame(
    {
        "category": ["Technology", "Furniture", "Office Supplies"],
        "total_sales": [256390.09, 200920.67, 175319.89],
        "total_quantity": [520, 577, 1642],
        "total_profit": [50753.99, 8025.58, None],  # profit not given for office supplies
        "contribution_pct": [40.53, 31.76, 27.71],
    }
)

subcategory_df = pd.DataFrame(
    {
        "category": [
            "Furniture", "Technology", "Technology", "Office Supplies", "Furniture",
            "Technology", "Technology", "Office Supplies", "Furniture", "Office Supplies",
            "Furniture", "Office Supplies", "Office Supplies", "Office Supplies",
            "Office Supplies", "Office Supplies", "Office Supplies",
        ],
        "sub_category": [
            "Chairs", "Phones", "Machines", "Storage", "Tables", "Copiers", "Accessories",
            "Binders", "Bookcases", "Appliances", "Furnishings", "Paper", "Supplies",
            "Art", "Envelopes", "Labels", "Fasteners",
        ],
        "total_sales": [
            90947.35, 83805.55, 74140.44, 54722.14, 53592.58, 49409.33, 49034.77,
            42929.38, 31091.82, 27771.97, 25288.92, 20967.64, 11755.16, 8846.98,
            3920.27, 3615.51, 790.84,
        ],
        "total_quantity": [
            169, 237, 38, 234, 90, 24, 221, 421, 57, 123, 261, 380, 43, 212, 64, 107, 58,
        ],
        "contribution_pct": [
            14.38, 13.25, 11.72, 8.65, 8.47, 7.81, 7.75, 6.79, 4.91, 4.39, 4.00, 3.31,
            1.86, 1.40, 0.62, 0.57, 0.13,
        ],
    }
)

# profit only available for top-5 sub-categories in source data
subcategory_profit_df = pd.DataFrame(
    {
        "sub_category": ["Chairs", "Phones", "Machines", "Storage", "Tables"],
        "total_sales": [90947.35, 83805.55, 74140.44, 54722.14, 53592.58],
        "total_profit": [9980.29, 12302.38, 5858.99, 6488.04, -3456.94],
        "total_quantity": [169, 237, 38, 234, 90],
    }
)

top_products_df = pd.DataFrame(
    {
        "product_name": [
            "Canon imageCLASS 2200 Advanced Copier",
            "Lexmark MX611dhe Monochrome Laser Printer",
            'HP Designjet T520 Inkjet Large Format Printer - 24" Color',
            "Riverside Palais Royal Lawyers Bookcase, Royale Cherry Finish",
            "Hewlett Packard LaserJet 3310 Copier",
        ],
        "total_sales": [17499.95, 11219.93, 8749.95, 8298.84, 8159.86],
    }
)

lowest_products_df = pd.DataFrame(
    {
        "product_name": [
            "Self-Adhesive Ring Binder Labels",
            "Avery Triangle Shaped Sheet Lifters, Black, 2/Pack",
            "Eureka Disposable Bags for Sanitaire Vibra Groomer I Upright Vac",
            "Avery Hidden Tab Dividers for Binding Systems",
            "Acco Banker's Clasps, 5 3/4\"-long",
        ],
        "total_sales": [1.41, 1.48, 1.62, 1.79, 2.30],
    }
)

year_sales_df = pd.DataFrame(
    {
        "year": [2014, 2015, 2016, 2017],
        "total_sales": [110303.97, 116978.37, 203260.25, 202088.06],
        "growth_pct": [0.0, 6.05, 73.76, -0.58],
    }
)

year_profit_df = pd.DataFrame(
    {
        "year": [2014, 2015, 2016, 2017],
        "total_quantity": [506, 549, 745, 939],
        "total_profit": [13820.21, 12555.82, 36504.52, 22920.71],
        "growth_pct": [0.0, -9.15, 190.74, -37.21],
    }
)

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

month_sales_df = pd.DataFrame(
    {
        "month": month_order,
        "total_quantity": [337, 379, 365, 308, 366, 264, 261, 210, 106, 66, 60, 17],
        "total_sales": [
            95524.55, 105139.10, 72319.95, 68162.30, 64520.53, 47092.21,
            53903.39, 69297.31, 23855.94, 13519.52, 14585.22, 4710.63,
        ],
        "growth_pct": [
            0.0, 10.07, -31.21, -5.75, -5.34, -27.01, 14.46, 28.56, -65.57,
            -43.33, 7.88, -67.70,
        ],
    }
)

month_profit_df = pd.DataFrame(
    {
        "month": month_order,
        "total_quantity": [337, 379, 365, 308, 366, 264, 261, 210, 106, 66, 60, 17],
        "total_profit": [
            17006.78, 19441.11, 7090.50, 6873.67, 7498.33, 6746.37, 6716.54,
            6976.92, 5108.18, 844.02, 1416.73, 82.11,
        ],
        "growth_pct": [
            0.0, 14.31, -63.53, -3.06, 9.09, -10.03, -0.44, 3.88, -26.78,
            -83.48, 67.86, -94.20,
        ],
    }
)

quarter_df = pd.DataFrame(
    {
        "quarter": [
            "2014-Q1", "2014-Q2", "2014-Q3", "2014-Q4",
            "2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4",
            "2016-Q1", "2016-Q2", "2016-Q3", "2016-Q4",
            "2017-Q1", "2017-Q2", "2017-Q3", "2017-Q4",
        ],
        "total_quantity": [199, 195, 105, 7, 192, 193, 134, 30, 280, 286, 133, 46, 410, 264, 205, 60],
        "total_sales": [
            38633.72, 39579.84, 31316.66, 773.75,
            42927.38, 32692.79, 34058.09, 7300.11,
            95694.66, 60151.86, 36071.57, 11342.16,
            95727.84, 47350.55, 45610.32, 13399.35,
        ],
    }
)

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

day_sales_df = pd.DataFrame(
    {
        "day": day_order,
        "total_quantity": [458, 355, 319, 416, 371, 393, 427],
        "total_sales": [89180.33, 106278.31, 89830.55, 87462.15, 73439.74, 91003.62, 95435.95],
    }
)

day_profit_df = pd.DataFrame(
    {
        "day": day_order,
        "total_quantity": [458, 355, 319, 416, 371, 393, 427],
        "total_profit": [13018.49, 15526.26, 17188.97, 10674.14, 9130.97, 10004.40, 10258.03],
    }
)

weekend_weekday_sales_df = pd.DataFrame(
    {"day_type": ["Weekday", "Weekend"], "total_sales": [446191.08, 186439.57]}
)

weekend_weekday_profit_df = pd.DataFrame(
    {"day_type": ["Weekday", "Weekend"], "total_profit": [65538.83, 20262.43]}
)

top_transactions_df = pd.DataFrame(
    {
        "customer_id": [
            "QJ-19255", "RP-19390", "CJ-12010", "AB-10060", "GM-14695",
            "AA-10315", "TC-20980", "SE-20110", "BM-11140",
        ],
        "category": [
            "Furniture", "Furniture", "Furniture", "Office Supplies", "Office Supplies",
            "Office Supplies", "Technology", "Technology", "Technology",
        ],
        "sales": [4404.90, 2807.84, 2803.92, 4355.17, 4164.05, 3930.07, 17499.95, 8749.95, 8159.95],
        "rank": [1, 2, 3, 1, 2, 3, 1, 2, 3],
    }
)

ship_mode_df = pd.DataFrame(
    {
        "ship_mode": ["Standard Class", "Second Class", "First Class", "Same Day"],
        "total_sales": [325757.76, 130162.18, 115933.54, 60777.17],
        "total_quantity": [1418, 541, 535, 245],
    }
)

segment_df = pd.DataFrame(
    {
        "segment": ["Consumer", "Corporate", "Home Office"],
        "total_sales": [295429.78, 205852.12, 131348.75],
        "total_quantity": [1411, 809, 519],
    }
)

city_df = pd.DataFrame(
    {
        "city": [
            "New York City", "Los Angeles", "San Francisco", "Seattle", "Philadelphia",
            "Lafayette", "Houston", "Burlington", "San Antonio", "Henderson",
        ],
        "total_sales": [73774.44, 49429.38, 31053.83, 25284.14, 22804.21, 18948.79, 18097.20, 14796.85, 14219.96, 13428.74],
        "total_quantity": [280, 199, 134, 113, 154, 12, 114, 7, 31, 27],
    }
)

state_df = pd.DataFrame(
    {
        "state": [
            "California", "New York", "Texas", "Washington", "Indiana", "Virginia",
            "North Carolina", "Pennsylvania", "Florida", "Michigan", "Kentucky", "Ohio",
            "Wisconsin", "Illinois", "Massachusetts", "Rhode Island", "Colorado", "Minnesota",
            "Georgia", "Maryland", "Tennessee", "Arizona", "Vermont", "Delaware", "Oregon",
            "Arkansas", "Connecticut", "Oklahoma", "Utah", "Nevada", "Nebraska", "Missouri",
            "Mississippi", "New Jersey", "Wyoming", "New Hampshire", "Alabama", "South Carolina",
            "New Mexico", "Iowa", "Idaho", "Louisiana", "West Virginia", "Maine", "Kansas",
            "District of Columbia",
        ],
        "total_sales": [
            122989.25, 91708.18, 59888.85, 33278.68, 28937.85, 26156.82, 25788.60, 23283.41,
            21656.10, 18245.24, 17050.67, 14883.67, 14284.47, 13040.06, 11107.83, 9736.71,
            8219.27, 8068.96, 7962.24, 7549.57, 6896.98, 6857.07, 6619.88, 4977.75, 4805.37,
            4229.78, 4012.65, 4004.65, 3942.41, 3058.15, 3036.87, 2068.13, 1725.92, 1689.73,
            1603.14, 1539.23, 1459.51, 1384.18, 1003.06, 874.20, 806.78, 699.33, 673.34,
            617.12, 175.07, 33.92,
        ],
        "total_quantity": [
            530, 340, 301, 136, 44, 68, 96, 159, 108, 76, 55, 122, 30, 114, 44, 16, 53, 31,
            42, 28, 45, 50, 4, 32, 31, 19, 19, 14, 13, 7, 9, 17, 9, 19, 1, 7, 6, 8, 4, 7, 6,
            8, 1, 3, 6, 1,
        ],
    }
)

region_df = pd.DataFrame(
    {
        "region": ["West", "East", "Central", "South"],
        "total_sales": [186563.18, 178432.99, 152624.35, 115010.13],
        "total_quantity": [831, 795, 649, 464],
    }
)

CATEGORY_COLORS = {"Technology": "#4C78A8", "Furniture": "#F58518", "Office Supplies": "#54A24B"}


def money(x):
    return f"${x:,.2f}"


def fmt_pct(x):
    sign = "+" if x > 0 else ""
    return f"{sign}{x:.2f}%"


# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.title("📊 Sales Insights")
    st.caption("Superstore-style sales analytics dashboard")

    st.markdown("---")
    st.subheader("Filters")

    years = st.multiselect(
        "Year",
        options=year_sales_df["year"].tolist(),
        default=year_sales_df["year"].tolist(),
    )
    categories = st.multiselect(
        "Category",
        options=category_df["category"].tolist(),
        default=category_df["category"].tolist(),
    )

    st.markdown("---")
    st.subheader("Dataset Info")
    st.caption(f"**Records:** {DATASET_META['records']:,}")
    st.caption(f"**Order dates:** {DATASET_META['order_start']} → {DATASET_META['order_end']}")
    st.caption(f"**Ship dates:** {DATASET_META['ship_start']} → {DATASET_META['ship_end']}")
    st.caption(f"**Dataset size:** {DATASET_META['size_kb']:,} KB")

if not years:
    years = year_sales_df["year"].tolist()
if not categories:
    categories = category_df["category"].tolist()

_year_mask = year_sales_df["year"].isin(years)
_cat_mask = category_df["category"].isin(categories)
_sub_mask = subcategory_df["category"].isin(categories)

filtered_year_sales = year_sales_df[_year_mask]
filtered_category = category_df[_cat_mask]
filtered_subcategory = subcategory_df[_sub_mask]

# ----------------------------------------------------------------------------
# HEADER + KPIs
# ----------------------------------------------------------------------------
st.title("Sales Performance Dashboard")
st.caption(
    f"Order period {DATASET_META['order_start']} — {DATASET_META['order_end']} · "
    f"{DATASET_META['records']:,} orders"
)

total_sales = filtered_category["total_sales"].sum() if len(categories) < 3 else 632630.65
total_profit_known = 50753.99 + 8025.58  # tech + furniture profit known
total_quantity = filtered_category["total_quantity"].sum() if len(categories) < 3 else (520 + 577 + 1642)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Sales", money(total_sales))
k2.metric("Total Quantity", f"{total_quantity:,}")
k3.metric("Avg Order Sales", money(DATASET_META["sales_avg"]))
k4.metric("Median Sales", money(DATASET_META["sales_median"]))
k5.metric("Total Records", f"{DATASET_META['records']:,}")

st.markdown("")

# ----------------------------------------------------------------------------
# TABS
# ----------------------------------------------------------------------------
tab_overview, tab_products, tab_time, tab_geo, tab_ops = st.tabs(
    ["🏠 Overview", "📦 Products", "📅 Time Trends", "🗺️ Geography", "🚚 Operations"]
)

# ============================== OVERVIEW TAB =================================
with tab_overview:
    c1, c2 = st.columns((1, 1))

    with c1:
        st.subheader("Sales by Category")
        fig = px.pie(
            filtered_category,
            names="category",
            values="total_sales",
            color="category",
            color_discrete_map=CATEGORY_COLORS,
            hole=0.45,
        )
        fig.update_traces(textinfo="label+percent", pull=[0.02] * len(filtered_category))
        fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=380)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Category: Sales vs Quantity")
        fig = go.Figure()
        fig.add_bar(
            x=filtered_category["category"], y=filtered_category["total_sales"],
            name="Total Sales", marker_color=[CATEGORY_COLORS[c] for c in filtered_category["category"]],
            yaxis="y1",
        )
        fig.add_trace(
            go.Scatter(
                x=filtered_category["category"], y=filtered_category["total_quantity"],
                name="Total Quantity", yaxis="y2", mode="lines+markers",
                line=dict(color="#B279A2", width=3),
            )
        )
        fig.update_layout(
            yaxis=dict(title="Total Sales"),
            yaxis2=dict(title="Total Quantity", overlaying="y", side="right"),
            margin=dict(t=10, b=10, l=10, r=10), height=380,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sub-Category Contribution to Sales")
    sub_sorted = filtered_subcategory.sort_values("total_sales", ascending=True)
    fig = px.bar(
        sub_sorted, x="total_sales", y="sub_category", orientation="h",
        color="category", color_discrete_map=CATEGORY_COLORS,
        text=sub_sorted["total_sales"].map(lambda v: f"${v:,.0f}"),
        labels={"total_sales": "Total Sales", "sub_category": "Sub-Category"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(height=520, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Top 5 Sub-Categories: Sales & Profit")
        fig = go.Figure()
        fig.add_bar(x=subcategory_profit_df["sub_category"], y=subcategory_profit_df["total_sales"], name="Sales", marker_color="#4C78A8")
        fig.add_bar(x=subcategory_profit_df["sub_category"], y=subcategory_profit_df["total_profit"], name="Profit", marker_color="#54A24B")
        fig.update_layout(barmode="group", height=380, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("⚠️ Tables sub-category shows a **negative profit** (-$3,456.94) despite $53,592.58 in sales.")

    with c4:
        st.subheader("Bottom 5 Sub-Categories by Sales")
        low_sub = subcategory_df.nsmallest(5, "total_sales")
        fig = px.bar(
            low_sub.sort_values("total_sales"), x="total_sales", y="sub_category",
            orientation="h", color_discrete_sequence=["#E45756"],
            text=low_sub.sort_values("total_sales")["total_sales"].map(lambda v: f"${v:,.2f}"),
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(height=380, margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.info(
        f"**Most frequent product:** {DATASET_META['most_frequent_product']} "
        f"(ordered {DATASET_META['most_frequent_product_qty']} times) · "
        f"**Top category:** {DATASET_META['top_category']} · "
        f"**Top sub-category:** {DATASET_META['top_subcategory']}"
    )

# ============================== PRODUCTS TAB ==================================
with tab_products:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🏆 Top 5 Products by Sales")
        fig = px.bar(
            top_products_df.sort_values("total_sales"), x="total_sales", y="product_name",
            orientation="h", color_discrete_sequence=["#4C78A8"],
            text=top_products_df.sort_values("total_sales")["total_sales"].map(lambda v: f"${v:,.2f}"),
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(height=420, margin=dict(t=10, b=10, l=10, r=10), yaxis_title="", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("📉 Bottom 5 Products by Sales")
        fig = px.bar(
            lowest_products_df.sort_values("total_sales"), x="total_sales", y="product_name",
            orientation="h", color_discrete_sequence=["#E45756"],
            text=lowest_products_df.sort_values("total_sales")["total_sales"].map(lambda v: f"${v:,.2f}"),
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(height=420, margin=dict(t=10, b=10, l=10, r=10), yaxis_title="", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 3 Highest-Value Transactions per Category")
    fig = px.bar(
        top_transactions_df, x="customer_id", y="sales", color="category",
        color_discrete_map=CATEGORY_COLORS, barmode="group",
        text=top_transactions_df["sales"].map(lambda v: f"${v:,.2f}"),
        facet_col="category",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(height=420, margin=dict(t=40, b=10, l=10, r=10))
    fig.update_xaxes(matches=None, showticklabels=True)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        top_transactions_df.rename(
            columns={"customer_id": "Customer ID", "category": "Category", "sales": "Sales ($)", "rank": "Rank"}
        ),
        use_container_width=True, hide_index=True,
    )

# ============================== TIME TRENDS TAB ================================
with tab_time:
    st.subheader("Yearly Sales & Growth")
    c1, c2 = st.columns((2, 1))
    with c1:
        fig = go.Figure()
        fig.add_bar(x=filtered_year_sales["year"], y=filtered_year_sales["total_sales"], name="Total Sales", marker_color="#4C78A8")
        fig.add_trace(go.Scatter(x=filtered_year_sales["year"], y=filtered_year_sales["growth_pct"], name="YoY Growth %", yaxis="y2", mode="lines+markers", line=dict(color="#F58518", width=3)))
        fig.update_layout(
            yaxis=dict(title="Total Sales"), yaxis2=dict(title="Growth %", overlaying="y", side="right"),
            height=380, margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.dataframe(
            year_sales_df.assign(total_sales=lambda d: d["total_sales"].map(money), growth_pct=lambda d: d["growth_pct"].map(fmt_pct))
            .rename(columns={"year": "Year", "total_sales": "Sales", "growth_pct": "YoY Growth"}),
            use_container_width=True, hide_index=True,
        )

    st.subheader("Yearly Profit & Growth")
    c1, c2 = st.columns((2, 1))
    with c1:
        fig = go.Figure()
        fig.add_bar(x=year_profit_df["year"], y=year_profit_df["total_profit"], name="Total Profit", marker_color="#54A24B")
        fig.add_trace(go.Scatter(x=year_profit_df["year"], y=year_profit_df["growth_pct"], name="YoY Profit Growth %", yaxis="y2", mode="lines+markers", line=dict(color="#E45756", width=3)))
        fig.update_layout(
            yaxis=dict(title="Total Profit"), yaxis2=dict(title="Growth %", overlaying="y", side="right"),
            height=380, margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.dataframe(
            year_profit_df.assign(total_profit=lambda d: d["total_profit"].map(money), growth_pct=lambda d: d["growth_pct"].map(fmt_pct))
            .rename(columns={"year": "Year", "total_quantity": "Qty", "total_profit": "Profit", "growth_pct": "YoY Growth"}),
            use_container_width=True, hide_index=True,
        )

    st.subheader("Quarterly Sales")
    fig = px.bar(quarter_df, x="quarter", y="total_sales", color_discrete_sequence=["#4C78A8"])
    fig.update_layout(height=350, margin=dict(t=10, b=10, l=10, r=10), xaxis_title="", yaxis_title="Total Sales")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Sales & Profit Trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=month_sales_df["month"], y=month_sales_df["total_sales"], name="Sales", mode="lines+markers", line=dict(color="#4C78A8", width=3)))
    fig.add_trace(go.Scatter(x=month_profit_df["month"], y=month_profit_df["total_profit"], name="Profit", mode="lines+markers", line=dict(color="#54A24B", width=3), yaxis="y2"))
    fig.update_layout(
        yaxis=dict(title="Total Sales"), yaxis2=dict(title="Total Profit", overlaying="y", side="right"),
        height=400, margin=dict(t=10, b=10, l=10, r=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Sales by Day of Week")
        fig = px.bar(day_sales_df, x="day", y="total_sales", color_discrete_sequence=["#4C78A8"])
        fig.update_layout(height=350, margin=dict(t=10, b=10, l=10, r=10), xaxis_title="", yaxis_title="Total Sales")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Weekday vs Weekend")
        fig = px.pie(weekend_weekday_sales_df, names="day_type", values="total_sales", hole=0.5,
                     color="day_type", color_discrete_map={"Weekday": "#4C78A8", "Weekend": "#F58518"})
        fig.update_traces(textinfo="label+percent")
        fig.update_layout(height=350, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Note: Tuesday and Wednesday show the highest profit despite not having the highest sales — "
        "a sign of stronger margins mid-week."
    )

# ============================== GEOGRAPHY TAB ==================================
with tab_geo:
    c1, c2 = st.columns((1, 1))
    with c1:
        st.subheader("Sales by Region")
        fig = px.pie(region_df, names="region", values="total_sales", hole=0.45,
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(textinfo="label+percent")
        fig.update_layout(height=380, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Top 10 Cities by Sales")
        fig = px.bar(city_df.sort_values("total_sales"), x="total_sales", y="city", orientation="h",
                     color_discrete_sequence=["#4C78A8"])
        fig.update_layout(height=380, margin=dict(t=10, b=10, l=10, r=10), yaxis_title="", xaxis_title="Total Sales")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("State-wise Sales")
    top_n = st.slider("Show top N states", min_value=5, max_value=len(state_df), value=15, step=5)
    state_sorted = state_df.sort_values("total_sales", ascending=False).head(top_n)
    fig = px.bar(
        state_sorted.sort_values("total_sales"), x="total_sales", y="state", orientation="h",
        color="total_sales", color_continuous_scale="Blues",
    )
    fig.update_layout(height=max(400, top_n * 24), margin=dict(t=10, b=10, l=10, r=10), yaxis_title="", xaxis_title="Total Sales", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("View full state data table"):
        st.dataframe(
            state_df.sort_values("total_sales", ascending=False).assign(total_sales=lambda d: d["total_sales"].map(money))
            .rename(columns={"state": "State", "total_sales": "Sales", "total_quantity": "Quantity"}),
            use_container_width=True, hide_index=True,
        )

# ============================== OPERATIONS TAB ==================================
with tab_ops:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Sales by Ship Mode")
        fig = px.bar(ship_mode_df, x="ship_mode", y="total_sales", color="ship_mode",
                     color_discrete_sequence=px.colors.qualitative.Set2,
                     text=ship_mode_df["total_sales"].map(lambda v: f"${v:,.0f}"))
        fig.update_traces(textposition="outside")
        fig.update_layout(height=380, margin=dict(t=10, b=10, l=10, r=10), xaxis_title="", yaxis_title="Total Sales", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("**Standard Class** is the most frequently used and highest-revenue shipping mode.")

    with c2:
        st.subheader("Sales by Segment")
        fig = px.pie(segment_df, names="segment", values="total_sales", hole=0.45,
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(textinfo="label+percent")
        fig.update_layout(height=380, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Weekday vs Weekend Profit")
    fig = px.bar(weekend_weekday_profit_df, x="day_type", y="total_profit", color="day_type",
                 color_discrete_map={"Weekday": "#54A24B", "Weekend": "#E45756"},
                 text=weekend_weekday_profit_df["total_profit"].map(lambda v: f"${v:,.2f}"))
    fig.update_traces(textposition="outside")
    fig.update_layout(height=350, margin=dict(t=10, b=10, l=10, r=10), xaxis_title="", yaxis_title="Total Profit", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Profit by Day of Week")
    fig = px.bar(day_profit_df, x="day", y="total_profit", color_discrete_sequence=["#54A24B"])
    fig.update_layout(height=350, margin=dict(t=10, b=10, l=10, r=10), xaxis_title="", yaxis_title="Total Profit")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption(
    "Dashboard generated from precomputed sales analytics · "
    f"Grand total sales: {money(632630.65)} · Built with Streamlit + Plotly"
)