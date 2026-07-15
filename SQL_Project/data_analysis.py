import streamlit as st
import pandas as pd
import plotly.express as px
import io

# =====================================================================
# 1. PAGE CONFIGURATION
# =====================================================================
st.set_page_config(
    page_title="Superstore Sales Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================================
# 2. CUSTOM THEME & CSS (Light & Dark Mode Adaptive)
# =====================================================================
PRIMARY_COLOR = "#2E5EAA"
ACCENT_COLOR = "#F2994A"
PALETTE = ["#2E5EAA", "#F2994A", "#1E9E6C", "#9B59B6", "#D64545", "#17A2B8", "#6C757D"]

st.markdown(f"""
<style>
    /* Main Layout Tweaks */
    .block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1350px; }}
    
    /* 3 dots (MainMenu) ko wapas lane ke liye footer ko alag se hide kiya */
    footer {{ visibility: hidden; }}

    /* Metric Cards - Adapts to Streamlit's Theme */
    div[data-testid="stMetric"] {{
        background-color: var(--secondary-background-color);
        border: 1px solid var(--divider-color);
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.05);
    }}
    div[data-testid="stMetricLabel"] {{ font-weight: 600; font-size: 0.9rem; letter-spacing: 0.5px; }}
    div[data-testid="stMetricValue"] {{ font-weight: 700; color: {PRIMARY_COLOR}; }}

    /* Headers Styling */
    h1, h2, h3 {{ font-weight: 700 !important; }}

    /* Actionable Insight Box */
    .insight-box {{
        background-color: var(--secondary-background-color);
        border-left: 5px solid {PRIMARY_COLOR};
        padding: 15px 20px;
        border-radius: 8px;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 20px 0;
    }}
    
    /* Elegant Footer */
    .custom-footer {{
        text-align: center;
        padding: 20px 0;
        font-size: 0.8rem;
        color: var(--text-color-light);
        border-top: 1px solid var(--divider-color);
        margin-top: 50px;
    }}
</style>
""", unsafe_allow_html=True)

# Helper function to style Plotly figures beautifully
def apply_plotly_theme(fig, title=None, y_title=None, x_title=None, show_legend=False):
    fig.update_layout(
        font=dict(family="Inter, -apple-system, sans-serif", size=12),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=15, t=50, b=15),
        title=dict(text=title, font=dict(size=16, weight="bold")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1) if show_legend else None,
        showlegend=show_legend
    )
    fig.update_yaxes(title=y_title, gridcolor="var(--divider-color)", zeroline=False)
    fig.update_xaxes(title=x_title, gridcolor="rgba(0,0,0,0)")
    return fig


# =====================================================================
# 3. HIGH-PERFORMANCE DATA LOADER (Cached)
# =====================================================================
@st.cache_data
def load_superstore_data():
    yearly_sales = pd.DataFrame({
        "year": [2015, 2016, 2017, 2018],
        "total_quantity": [1952, 2055, 2534, 3258],
        "total_sales": [479574.90, 459435.94, 600192.80, 722051.96],
    })
    yearly_sales["yoy_growth_%"] = yearly_sales["total_sales"].pct_change().mul(100).round(2)

    quarterly_sales = pd.DataFrame({
        "quarter": ["2015-Q1","2015-Q2","2015-Q3","2015-Q4",
                    "2016-Q1","2016-Q2","2016-Q3","2016-Q4",
                    "2017-Q1","2017-Q2","2017-Q3","2017-Q4",
                    "2018-Q1","2018-Q2","2018-Q3","2018-Q4"],
        "total_quantity": [277,381,555,739, 249,431,579,796, 333,585,720,896, 484,675,890,1209],
        "total_sales": [73931.46,85592.73,142522.57,177528.14,
                         62357.68,87713.46,128560.14,180804.66,
                         92686.38,135061.19,138056.43,234388.80,
                         122260.86,127558.58,193815.83,278416.69],
    })
    quarterly_sales["year"] = quarterly_sales["quarter"].str[:4].astype(int)

    month_order = ["january","february","march","april","may","june",
                   "july","august","september","october","november","december"]
    monthly_sales = pd.DataFrame({
        "month": month_order,
        "total_quantity": [366,297,680,656,725,691,697,693,1354,809,1449,1382],
        "total_sales": [94291.66,59371.12,197573.60,136001.67,154086.74,145837.55,
                         145535.70,157315.85,300103.42,199496.34,350161.74,321480.21],
    })
    monthly_sales["running_total"] = monthly_sales["total_sales"].cumsum()
    monthly_sales["month_label"] = monthly_sales["month"].str.capitalize()

    day_order = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    day_sales = pd.DataFrame({
        "day": day_order,
        "total_quantity": [1593,1889,1229,540,1067,1786,1695],
        "total_sales": [348791.49,420535.92,315888.99,142557.86,234710.89,420901.57,377868.88],
    })
    day_sales["day_label"] = day_sales["day"].str.capitalize()
    day_sales["type"] = day_sales["day"].apply(lambda d: "Weekend" if d in ("saturday","sunday") else "Weekday")

    category_sales = pd.DataFrame({
        "category": ["Technology", "Furniture", "Office Supplies"],
        "sales": [832000, 727000, 706000],
        "percentage_share": [36.59, 32.21, 31.20],
    })

    cat_subcat = pd.DataFrame([
        ("Technology","Phones",327782.49,14.50),
        ("Technology","Machines",189238.68,8.37),
        ("Technology","Accessories",164186.70,7.26),
        ("Technology","Copiers",146248.07,6.47),
        ("Furniture","Chairs",322541.38,14.26),
        ("Furniture","Tables",202810.77,8.97),
        ("Furniture","Bookcases",113813.25,5.03),
        ("Furniture","Furnishings",89211.98,3.95),
        ("Office Supplies","Storage",219343.37,9.70),
        ("Office Supplies","Binders",200028.82,8.85),
        ("Office Supplies","Appliances",104618.38,4.63),
        ("Office Supplies","Paper",76828.34,3.40),
        ("Office Supplies","Supplies",46420.29,2.05),
        ("Office Supplies","Art",26705.42,1.18),
        ("Office Supplies","Envelopes",16128.02,0.71),
        ("Office Supplies","Labels",12347.71,0.55),
        ("Office Supplies","Fasteners",3001.93,0.13),
    ], columns=["category","sub_category","sales","percentage_share"])

    top_products = pd.DataFrame({
        "product_name": [
            "Canon imageCLASS 2200 Advanced Copier",
            "Fellowes PB500 Electric Punch Plastic Comb Binding Machine",
            "Cisco TelePresence System EX90 Videoconferencing Unit",
            "HON 5400 Series Task Chairs for Big and Tall",
            "GBC DocuBind TL300 Electric Binding System",
        ],
        "category": ["Technology","Office Supplies","Technology","Furniture","Office Supplies"],
        "sub_category": ["Copiers","Binders","Machines","Chairs","Binders"],
        "sales": [61599.83, 27453.38, 22638.48, 21870.57, 19823.48],
        "percentage_share": [2.72, 1.21, 1.00, 0.97, 0.88],
    })

    weekday_total = day_sales.loc[day_sales["type"] == "Weekday", "total_sales"].sum()
    weekend_total = day_sales.loc[day_sales["type"] == "Weekend", "total_sales"].sum()
    weekday_weekend = pd.DataFrame({
        "day_type": ["Weekday", "Weekend"],
        "total_sales": [weekday_total, weekend_total],
    })

    return {
        "yearly": yearly_sales,
        "quarterly": quarterly_sales,
        "monthly": monthly_sales,
        "day": day_sales,
        "category": category_sales,
        "cat_subcat": cat_subcat,
        "top_products": top_products,
        "weekday_weekend": weekday_weekend,
        "month_order": month_order,
        "day_order": day_order,
    }

# Load App Data
data = load_superstore_data()

# Constant Metadata Variables
DATASET_SIZE = "5,136 KB"
MEAN_MEDIAN_DIFF = 176.28
MOST_FREQUENT_CATEGORY = "Office Supplies"
MOST_FREQUENT_PRODUCT = "Staple Envelope"
ORDER_DATE_RANGE = "Jan 3, 2015 → Dec 30, 2018"
SHIP_DATE_RANGE = "Jan 7, 2015 → Jan 5, 2019"


# =====================================================================
# 4. SIDEBAR NAVIGATION & FILTERS
# =====================================================================
with st.sidebar:
    st.markdown("### 🛒 Navigation Panel")
    st.caption("Operational Sales Intelligence")
    st.markdown("---")

    page = st.radio(
        "Select Dashboard Section",
        ["📌 Overview", "🗂️ Category Analysis", "📅 Time Trends",
         "🏆 Top Products", "📆 Weekday vs Weekend"],
    )

    st.markdown("---")
    st.markdown("**Global Timeline Filter**")
    
    # Multiselect Filter for Years
    available_years = sorted(list(data["yearly"]["year"].unique()))
    selected_years = st.multiselect(
        "Filter Data by Year",
        options=available_years,
        default=available_years,
    )

    st.markdown("---")
    st.markdown("**Core Dataset Metadata**")
    st.caption(f"📅 Orders: {ORDER_DATE_RANGE}")
    st.caption(f"🚚 Shipping: {SHIP_DATE_RANGE}")
    st.caption(f"💾 Footprint: {DATASET_SIZE}")


# =====================================================================
# 5. DATASET EXPORTER UTILITY
# =====================================================================
def create_download_button(df, filename="sales_data_export.csv"):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return st.download_button(
        label="📥 Export Table as CSV",
        data=csv_buffer.getvalue(),
        file_name=filename,
        mime="text/csv",
    )


# =====================================================================
# HEADER
# =====================================================================
st.title("Superstore Sales Intelligence")
st.markdown(
    f'<p style="color: gray; font-size: 0.95rem; margin-top: -15px;">'
    f'Interactive performance dashboard built on cleaned transaction pipelines.'
    f'</p>',
    unsafe_allow_html=True,
)
st.markdown("---")


# =====================================================================
# PAGE: OVERVIEW
# =====================================================================
if page == "📌 Overview":
    # Filter Yearly Data
    filtered_yearly = data["yearly"][data["yearly"]["year"].isin(selected_years)] if selected_years else data["yearly"]
    
    total_sales = filtered_yearly["total_sales"].sum()
    total_orders = filtered_yearly["total_quantity"].sum()
    latest_growth = data["yearly"]["yoy_growth_%"].iloc[-1]

    # Metrics Layout
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Selected Period Sales", f"${total_sales:,.0f}")
    c2.metric("Total Order Quantity", f"{total_orders:,}")
    c3.metric("Terminal YoY Growth (2018)", f"{latest_growth:+.1f}%", delta=f"{latest_growth:.1f}%")
    c4.metric("Dominant Category", MOST_FREQUENT_CATEGORY)

    st.markdown("### Executive Performance Dashboard")
    col_left, col_right = st.columns([1.4, 1])

    with col_left:
        fig = px.bar(filtered_yearly, x="year", y="total_sales",
                     text=filtered_yearly["total_sales"].apply(lambda v: f"${v:,.0f}"),
                     color_discrete_sequence=[PRIMARY_COLOR])
        fig.update_traces(textposition="outside", marker_line_width=0)
        apply_plotly_theme(fig, title="Annual Sales Trajectory ($)", y_title="Sales ($)", x_title="")
        fig.update_xaxes(type="category")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        fig = px.pie(data["category"], names="category", values="percentage_share",
                     hole=0.55, color="category", color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="label+percent", textposition="outside")
        apply_plotly_theme(fig, title="Product Category Revenue Mix")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Aggregate Growth Pipeline")
    fig = px.area(data["monthly"], x="month_label", y="running_total",
                  color_discrete_sequence=[ACCENT_COLOR])
    fig.update_traces(line=dict(width=2.5, color=ACCENT_COLOR), fillcolor="rgba(242,153,74,0.12)")
    apply_plotly_theme(fig, title="Running Cumulative Sales Track", y_title="Cumulative Sales ($)", x_title="")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f'<div class="insight-box">🏆 <b>Top Velocity SKU:</b> '
        f'{MOST_FREQUENT_PRODUCT} &nbsp;|&nbsp; '
        f'📊 <b>Statistical Deviation Warning:</b> The gap between mean and median order sizes is ${MEAN_MEDIAN_DIFF}. '
        f'This indicates a high density of wholesale bulk-orders driving overall revenue spikes rather than baseline retail volume.</div>',
        unsafe_allow_html=True,
    )


# =====================================================================
# PAGE: CATEGORY ANALYSIS
# =====================================================================
elif page == "🗂️ Category Analysis":
    st.subheader("Major Product Divisions")
    c1, c2 = st.columns([1.3, 1])

    with c1:
        fig = px.bar(data["category"].sort_values("sales"), x="sales", y="category",
                     orientation="h", text=data["category"]["percentage_share"].apply(lambda v: f"{v:.1f}%"),
                     color_discrete_sequence=[PRIMARY_COLOR])
        fig.update_traces(textposition="outside", marker_line_width=0)
        apply_plotly_theme(fig, title="Consolidated Sales Volume", x_title="Sales ($)", y_title="")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(data["category"], names="category", values="percentage_share",
                     hole=0.45, color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="percent+label")
        apply_plotly_theme(fig, title="Relative Market Shares")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Sub-Category Breakdown")

    # Interactive Multiselect Filter (Departmental Level)
    cat_filter = st.multiselect(
        "Choose Category to Explode",
        options=sorted(data["cat_subcat"]["category"].unique()),
        default=sorted(data["cat_subcat"]["category"].unique()),
    )
    
    filtered_df = data["cat_subcat"][data["cat_subcat"]["category"].isin(cat_filter)].sort_values("sales", ascending=False)

    fig = px.bar(filtered_df, x="sub_category", y="sales", color="category",
                 text=filtered_df["percentage_share"].apply(lambda v: f"{v:.1f}%"),
                 color_discrete_sequence=PALETTE)
    fig.update_traces(textposition="outside", marker_line_width=0)
    apply_plotly_theme(fig, title="Sub-Category Performance Metrics", y_title="Sales ($)", x_title="", show_legend=True)
    st.plotly_chart(fig, use_container_width=True)

    # Data Table Integration with easy exporter
    with st.expander("📋 Click to View and Download Detailed Sub-Category Data"):
        st.dataframe(
            filtered_df.style.format({"sales": "${:,.2f}", "percentage_share": "{:.2f}%"}),
            use_container_width=True, hide_index=True,
        )
        create_download_button(filtered_df, "subcategory_sales_data.csv")

    st.markdown(
        '<div class="insight-box">💡 <b>Executive Action Item:</b> Phones and Chairs are key pillars, '
        'contributing nearly 29% of company-wide sales across all 17 sub-categories. '
        'Prioritize supply chain agreements and active stock monitoring for these lines to protect gross margins.</div>',
        unsafe_allow_html=True,
    )


# =====================================================================
# PAGE: TIME TRENDS
# =====================================================================
elif page == "📅 Time Trends":
    st.subheader("Chronological Sales Analytics")
    tab1, tab2, tab3 = st.tabs(["📊 Year-over-Year Progression", "📈 Quarterly Patterns", "📅 Seasonal Fluctuations"])

    # Filtered Datasets based on Sidebar year selector
    filtered_years_list = selected_years if selected_years else available_years
    filtered_yearly = data["yearly"][data["yearly"]["year"].isin(filtered_years_list)]
    filtered_quarterly = data["quarterly"][data["quarterly"]["year"].isin(filtered_years_list)]

    with tab1:
        c1, c2 = st.columns([1.5, 1])
        with c1:
            fig = px.bar(filtered_yearly, x="year", y="total_sales",
                         text=filtered_yearly["total_sales"].apply(lambda v: f"${v:,.0f}"),
                         color_discrete_sequence=[PRIMARY_COLOR])
            fig.update_traces(textposition="outside", marker_line_width=0)
            apply_plotly_theme(fig, title="YoY Billing Trajectory", y_title="Sales ($)", x_title="")
            fig.update_xaxes(type="category")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("##### Year-over-Year Data Matrix")
            st.dataframe(
                filtered_yearly[["year", "total_sales", "yoy_growth_%"]]
                    .style.format({"total_sales": "${:,.0f}", "yoy_growth_%": "{:+.2f}%"})
                    .background_gradient(subset=["yoy_growth_%"], cmap="RdYlGn"),
                use_container_width=True, hide_index=True,
            )
            create_download_button(filtered_yearly, "yearly_performance.csv")

    with tab2:
        fig = px.bar(filtered_quarterly, x="quarter", y="total_sales", color="year",
                     color_discrete_sequence=PALETTE)
        fig.update_traces(marker_line_width=0)
        apply_plotly_theme(fig, title="Quarterly Distribution Breakdown", y_title="Sales ($)", x_title="", show_legend=True)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("📊 Note: Q4 in both 2017 & 2018 represents historic fiscal highs due to seasonal end-of-year enterprise contracts.")

    with tab3:
        fig = px.bar(data["monthly"], x="month_label", y="total_sales", color_discrete_sequence=[PRIMARY_COLOR])
        fig.update_traces(marker_line_width=0)
        apply_plotly_theme(fig, title="Consolidated Monthly Demand Profile", y_title="Sales ($)", x_title="")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            '<div class="insight-box">🔥 <b>Seasonal Trends:</b> November and December alone pull '
            'over 30% of baseline annual billing. We strongly suggest aligning logistics and warehouse staffing limits '
            'to peak and contract around early October.</div>',
            unsafe_allow_html=True,
        )


# =====================================================================
# PAGE: TOP PRODUCTS
# =====================================================================
elif page == "🏆 Top Products":
    st.subheader("Gross-Revenue Superstars")

    c1, c2 = st.columns([1.4, 1])
    with c1:
        df_sorted = data["top_products"].sort_values("sales")
        fig = px.bar(df_sorted, x="sales", y="product_name", orientation="h",
                     text=df_sorted["percentage_share"].apply(lambda v: f"{v:.2f}%"),
                     color="category", color_discrete_sequence=PALETTE)
                     
        fig.update_traces(textposition="outside", marker_line_width=0)
        apply_plotly_theme(fig, title="Top 5 Individual SKUs (Gross Revenue)", x_title="Sales ($)", y_title="", show_legend=True)
        fig.update_yaxes(tickfont=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(data["top_products"], names="product_name", values="sales",
                     hole=0.4, color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="percent", showlegend=False)
        apply_plotly_theme(fig, title="Relative Revenue Spread (Top 5)")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("##### Performance Registry")
    st.dataframe(
        data["top_products"].style.format({"sales": "${:,.2f}", "percentage_share": "{:.2f}%"}),
        use_container_width=True, hide_index=True,
    )
    create_download_button(data["top_products"], "top_performing_products.csv")


# =====================================================================
# PAGE: WEEKDAY VS WEEKEND
# =====================================================================
elif page == "📆 Weekday vs Weekend":
    st.subheader("Transactional Velocity Profiles")

    wd = data["weekday_weekend"]
    total = wd["total_sales"].sum()
    weekday_val = wd.loc[wd.day_type == "Weekday", "total_sales"].values[0]
    weekend_val = wd.loc[wd.day_type == "Weekend", "total_sales"].values[0]

    # Quick Metrics Layout
    c1, c2, c3 = st.columns(3)
    c1.metric("Weekday Gross Sales", f"${weekday_val:,.0f}", f"{weekday_val/total*100:.1f}% Share")
    c2.metric("Weekend Gross Sales", f"${weekend_val:,.0f}", f"{weekend_val/total*100:.1f}% Share")
    c3.metric("Weekday Volume Shift", f"{(weekday_val/weekend_val - 1)*100:.0f}% Higher Velocity")

    st.markdown("")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(wd, names="day_type", values="total_sales", hole=0.5,
                     color="day_type", color_discrete_map={"Weekday": PRIMARY_COLOR, "Weekend": ACCENT_COLOR})
        fig.update_traces(textinfo="label+percent")
        apply_plotly_theme(fig, title="Revenue Composition")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(data["day"], x="day_label", y="total_sales", color="type",
                     color_discrete_map={"Weekday": PRIMARY_COLOR, "Weekend": ACCENT_COLOR})
        fig.update_traces(marker_line_width=0)
        apply_plotly_theme(fig, title="Dynamic Daily Performance", y_title="Sales ($)", x_title="", show_legend=True)
        fig.update_xaxes(categoryorder="array", categoryarray=[d.capitalize() for d in data["day_order"]])
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="insight-box">💡 <b>Executive Recommendation:</b> Tuesdays and Saturdays are '
        'individually top-performing days, while Thursdays are historically weak. We recommend executing marketing push '
        'notifications or midweek sales campaigns on Thursdays to level out demand peaks.</div>',
        unsafe_allow_html=True,
    )


# =====================================================================
# 6. FOOTER
# =====================================================================
st.markdown(
    '<div class="custom-footer">'
    'Superstore Sales Intelligence Dashboard • Operational Analytics Core • Built with Streamlit & Plotly'
    '</div>',
    unsafe_allow_html=True,
)
