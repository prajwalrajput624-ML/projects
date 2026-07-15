import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================================
# PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="Superstore Sales Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================================
# THEME / CSS
# =====================================================================
PRIMARY = "#2E5EAA"
ACCENT = "#F2994A"
BG_CARD = "#FFFFFF"
PALETTE = ["#2E5EAA", "#F2994A", "#1E9E6C", "#9B59B6", "#D64545",
           "#17A2B8", "#6C757D", "#E0A800"]

st.markdown(f"""
<style>
    .block-container {{ padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1300px; }}
    #MainMenu, footer {{ visibility: hidden; }}

    div[data-testid="stMetric"] {{
        background: {BG_CARD};
        border: 1px solid #E9ECEF;
        border-radius: 12px;
        padding: 16px 18px 12px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    div[data-testid="stMetricLabel"] {{ font-weight: 600; color: #555; }}
    div[data-testid="stMetricValue"] {{ color: {PRIMARY}; }}

    h2, h3 {{ color: #1B2733; }}

    section[data-testid="stSidebar"] {{
        background-color: #F7F9FC;
        border-right: 1px solid #E9ECEF;
    }}

    button[data-baseweb="tab"] {{ font-weight: 600; }}

    .insight-box {{
        background: #F0F5FF;
        border-left: 4px solid {PRIMARY};
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }}
    .caption-muted {{ color: #6C757D; font-size: 0.85rem; }}
</style>
""", unsafe_allow_html=True)

CHART_LAYOUT = dict(
    font=dict(family="Inter, -apple-system, sans-serif", size=13, color="#1B2733"),
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)


def style_fig(fig, title=None, y_title=None, x_title=None, show_legend=False):
    fig.update_layout(**CHART_LAYOUT, title=title, showlegend=show_legend)
    fig.update_yaxes(title=y_title, gridcolor="#EEF1F5", zeroline=False)
    fig.update_xaxes(title=x_title, gridcolor="white")
    return fig


# =====================================================================
# DATA (from SQL EDA outputs)
# =====================================================================
@st.cache_data
def load_data():
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
    quarterly_sales["year"] = quarterly_sales["quarter"].str[:4]

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


data = load_data()

DATASET_SIZE = "5,136 KB"
MEAN_MEDIAN_DIFF = 176.28
MOST_FREQUENT_CATEGORY = "Office Supplies"
MOST_FREQUENT_PRODUCT = "Staple Envelope"
ORDER_DATE_RANGE = "Jan 3, 2015 → Dec 30, 2018"
SHIP_DATE_RANGE = "Jan 7, 2015 → Jan 5, 2019"

# =====================================================================
# SIDEBAR
# =====================================================================
with st.sidebar:
    st.markdown("### 🛒 Superstore Sales")
    st.caption("SQL-driven analytics dashboard")
    st.markdown("---")

    page = st.radio(
        "Section",
        ["📌 Overview", "🗂️ Category Analysis", "📅 Time Trends",
         "🏆 Top Products", "📆 Weekday vs Weekend"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**Dataset Coverage**")
    st.caption(f"📅 Orders: {ORDER_DATE_RANGE}")
    st.caption(f"🚚 Shipping: {SHIP_DATE_RANGE}")
    st.caption(f"💾 Size: {DATASET_SIZE}")

    with st.expander("ℹ️ About this dashboard"):
        st.write(
            "Built on a SQL EDA pipeline over Superstore sales data: "
            "cleaning, deduplication, and business analysis using window "
            "functions (running totals, YoY/MoM growth, ranking) in PostgreSQL."
        )

# =====================================================================
# HEADER
# =====================================================================
st.title("Superstore Sales Intelligence")
st.markdown(
    '<p class="caption-muted">Four years of sales performance — cleaned, '
    'analyzed, and visualized from raw transaction data.</p>',
    unsafe_allow_html=True,
)

# =====================================================================
# OVERVIEW
# =====================================================================
if page == "📌 Overview":
    total_sales = data["yearly"]["total_sales"].sum()
    total_orders = data["yearly"]["total_quantity"].sum()
    latest_growth = data["yearly"]["yoy_growth_%"].iloc[-1]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sales (2015–18)", f"${total_sales:,.0f}")
    c2.metric("Total Orders", f"{total_orders:,}")
    c3.metric("2018 YoY Growth", f"{latest_growth:+.1f}%", delta=f"{latest_growth:.1f}%")
    c4.metric("Top Category", MOST_FREQUENT_CATEGORY)

    st.markdown("")
    col_left, col_right = st.columns([1.4, 1])

    with col_left:
        st.subheader("Yearly Sales Trend")
        fig = px.bar(data["yearly"], x="year", y="total_sales",
                     text=data["yearly"]["total_sales"].apply(lambda v: f"${v:,.0f}"),
                     color_discrete_sequence=[PRIMARY])
        fig.update_traces(textposition="outside", marker_line_width=0)
        style_fig(fig, y_title="Sales ($)", x_title="")
        fig.update_xaxes(type="category")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Category Mix")
        fig = px.pie(data["category"], names="category", values="percentage_share",
                     hole=0.55, color="category", color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="label+percent", textposition="outside")
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Cumulative Sales Growth (Monthly Running Total)")
    fig = px.area(data["monthly"], x="month_label", y="running_total",
                  color_discrete_sequence=[ACCENT])
    fig.update_traces(line=dict(width=2, color=ACCENT), fillcolor="rgba(242,153,74,0.15)")
    style_fig(fig, y_title="Cumulative Sales ($)", x_title="")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f'<div class="insight-box">🏆 <b>Most frequently purchased product:</b> '
        f'{MOST_FREQUENT_PRODUCT} &nbsp;|&nbsp; '
        f'📊 <b>Mean vs. median sales gap:</b> ${MEAN_MEDIAN_DIFF} '
        f'(right-skewed distribution — a small number of large orders pull the average up)</div>',
        unsafe_allow_html=True,
    )

# =====================================================================
# CATEGORY ANALYSIS
# =====================================================================
elif page == "🗂️ Category Analysis":
    st.subheader("Sales by Category")
    c1, c2 = st.columns([1.3, 1])

    with c1:
        fig = px.bar(data["category"].sort_values("sales"), x="sales", y="category",
                     orientation="h", text=data["category"]["percentage_share"].apply(lambda v: f"{v:.1f}%"),
                     color_discrete_sequence=[PRIMARY])
        fig.update_traces(textposition="outside", marker_line_width=0)
        style_fig(fig, x_title="Sales ($)", y_title="")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(data["category"], names="category", values="percentage_share",
                     hole=0.45, color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="percent+label")
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Sub-Category Breakdown")

    cat_filter = st.multiselect(
        "Filter by category",
        options=sorted(data["cat_subcat"]["category"].unique()),
        default=sorted(data["cat_subcat"]["category"].unique()),
    )
    filtered = data["cat_subcat"][data["cat_subcat"]["category"].isin(cat_filter)].sort_values("sales", ascending=False)

    fig = px.bar(filtered, x="sub_category", y="sales", color="category",
                 text=filtered["percentage_share"].apply(lambda v: f"{v:.1f}%"),
                 color_discrete_sequence=PALETTE)
    fig.update_traces(textposition="outside", marker_line_width=0)
    style_fig(fig, y_title="Sales ($)", x_title="", show_legend=True)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 View detailed table"):
        st.dataframe(
            filtered.style.format({"sales": "${:,.2f}", "percentage_share": "{:.2f}%"}),
            use_container_width=True, hide_index=True,
        )

    st.markdown(
        '<div class="insight-box">💡 <b>Insight:</b> Technology (36.6%) and Furniture (32.2%) '
        'drive the majority of revenue. Phones and Chairs alone account for nearly 29% of '
        'total sales across all 17 sub-categories.</div>',
        unsafe_allow_html=True,
    )

# =====================================================================
# TIME TRENDS
# =====================================================================
elif page == "📅 Time Trends":
    tab1, tab2, tab3 = st.tabs(["Yearly", "Quarterly", "Monthly"])

    with tab1:
        c1, c2 = st.columns([1.5, 1])
        with c1:
            fig = px.bar(data["yearly"], x="year", y="total_sales",
                         text=data["yearly"]["total_sales"].apply(lambda v: f"${v:,.0f}"),
                         color_discrete_sequence=[PRIMARY])
            fig.update_traces(textposition="outside", marker_line_width=0)
            style_fig(fig, y_title="Sales ($)", x_title="")
            fig.update_xaxes(type="category")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("##### Year-over-Year Growth")
            st.dataframe(
                data["yearly"][["year", "total_sales", "yoy_growth_%"]]
                    .style.format({"total_sales": "${:,.0f}", "yoy_growth_%": "{:+.2f}%"})
                    .background_gradient(subset=["yoy_growth_%"], cmap="RdYlGn"),
                use_container_width=True, hide_index=True,
            )

    with tab2:
        fig = px.bar(data["quarterly"], x="quarter", y="total_sales", color="year",
                     color_discrete_sequence=PALETTE)
        fig.update_traces(marker_line_width=0)
        style_fig(fig, y_title="Sales ($)", x_title="", show_legend=True)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("2017-Q4 and 2018-Q4 are the strongest quarters on record — holiday-season demand.")

    with tab3:
        fig = px.bar(data["monthly"], x="month_label", y="total_sales",
                     color_discrete_sequence=[PRIMARY])
        fig.update_traces(marker_line_width=0)
        style_fig(fig, y_title="Sales ($)", x_title="")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            '<div class="insight-box">🔥 <b>Peak months:</b> November & December &nbsp;|&nbsp; '
            '📉 <b>Slowest months:</b> January & February</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.subheader("Sales by Day of Week")
    fig = px.bar(data["day"], x="day_label", y="total_sales", color="type",
                 color_discrete_map={"Weekday": PRIMARY, "Weekend": ACCENT})
    fig.update_traces(marker_line_width=0)
    style_fig(fig, y_title="Sales ($)", x_title="", show_legend=True)
    fig.update_xaxes(categoryorder="array", categoryarray=[d.capitalize() for d in data["day_order"]])
    st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# TOP PRODUCTS
# =====================================================================
elif page == "🏆 Top Products":
    st.subheader("Top 5 Products by Sales")

    c1, c2 = st.columns([1.4, 1])
    with c1:
        df = data["top_products"].sort_values("sales")
        fig = px.bar(df, x="sales", y="product_name", orientation="h",
                     text=df["percentage_share"].apply(lambda v: f"{v:.2f}%"),
                     color="category", color_discrete_sequence=PALETTE)
        fig.update_traces(textposition="outside", marker_line_width=0)
        style_fig(fig, x_title="Sales ($)", y_title="", show_legend=True)
        fig.update_yaxes(tickfont=dict(size=11))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(data["top_products"], names="product_name", values="sales",
                     hole=0.4, color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="percent", showlegend=False)
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        data["top_products"].style.format({"sales": "${:,.2f}", "percentage_share": "{:.2f}%"}),
        use_container_width=True, hide_index=True,
    )

    st.markdown(
        f'<div class="insight-box">🏆 <b>Best-seller by frequency:</b> {MOST_FREQUENT_PRODUCT} '
        f'&nbsp;|&nbsp; 💰 <b>Best-seller by revenue:</b> Canon imageCLASS 2200 Advanced Copier '
        f'(${data["top_products"]["sales"].iloc[0]:,.0f})</div>',
        unsafe_allow_html=True,
    )

# =====================================================================
# WEEKDAY VS WEEKEND
# =====================================================================
elif page == "📆 Weekday vs Weekend":
    st.subheader("Weekday vs Weekend Performance")

    wd = data["weekday_weekend"]
    total = wd["total_sales"].sum()
    weekday_val = wd.loc[wd.day_type == "Weekday", "total_sales"].values[0]
    weekend_val = wd.loc[wd.day_type == "Weekend", "total_sales"].values[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Weekday Sales", f"${weekday_val:,.0f}", f"{weekday_val/total*100:.1f}% of total")
    c2.metric("Weekend Sales", f"${weekend_val:,.0f}", f"{weekend_val/total*100:.1f}% of total")
    c3.metric("Weekday Advantage", f"{(weekday_val/weekend_val - 1)*100:.0f}% higher")

    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(wd, names="day_type", values="total_sales", hole=0.5,
                     color="day_type", color_discrete_map={"Weekday": PRIMARY, "Weekend": ACCENT})
        fig.update_traces(textinfo="label+percent")
        style_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(data["day"], x="day_label", y="total_sales", color="type",
                     color_discrete_map={"Weekday": PRIMARY, "Weekend": ACCENT})
        fig.update_traces(marker_line_width=0)
        style_fig(fig, y_title="Sales ($)", x_title="", show_legend=True)
        fig.update_xaxes(categoryorder="array", categoryarray=[d.capitalize() for d in data["day_order"]])
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="insight-box">💡 <b>Insight:</b> Weekdays generate the majority of revenue, '
        'led by Saturday and Tuesday individually — Thursday is consistently the weakest day.</div>',
        unsafe_allow_html=True,
    )

# =====================================================================
# FOOTER
# =====================================================================
st.markdown("---")
st.caption(
    "Superstore Sales Intelligence Dashboard · Built with Streamlit & Plotly · "
    "Data pipeline: PostgreSQL (cleaning, dedup, window-function analysis)"
)