import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
import requests
import time
from streamlit_lottie import st_lottie

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 1rem;
}

.stMetric {
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOTTIE FUNCTION
# -------------------------------------------------
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------
@st.cache_resource
def load_model():
    try:
        model = joblib.load("best_model_House_price.pkl")
        return model, None
    except Exception as e:
        return None, str(e)

model, model_error = load_model()

# -------------------------------------------------
# HEADER
# -------------------------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    lottie = load_lottie_url(
        "https://assets9.lottiefiles.com/packages/lf20_xlmz9xwm.json"
    )

    if lottie:
        st_lottie(
            lottie,
            speed=1,
            height=220,
            key="house"
        )

with col2:
    st.title("🏠 House Price Prediction")
    st.markdown(
        """
        Predict California house prices using a trained
        Machine Learning model.
        """
    )

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
with st.sidebar:
    st.header("ℹ️ About")

    st.write("""
    Features:
    - House Price Prediction
    - Lottie Animation
    - Gauge Chart
    - Bar Chart
    - Download Results
    """)

# -------------------------------------------------
# MODEL LOAD ERROR
# -------------------------------------------------
if model_error:
    st.error(f"Model Load Error: {model_error}")

# -------------------------------------------------
# INPUT FORM
# -------------------------------------------------
with st.form("prediction_form"):

    st.subheader("📍 Location")

    c1, c2 = st.columns(2)

    longitude = c1.number_input(
        "Longitude",
        value=-122.23,
        format="%.4f"
    )

    latitude = c2.number_input(
        "Latitude",
        value=37.88,
        format="%.4f"
    )

    c3, c4, c5 = st.columns(3)

    ocean_proximity = c3.selectbox(
        "Ocean Proximity",
        [
            "<1h ocean",
            "inland",
            "near ocean",
            "near bay",
            "island"
        ]
    )

    lat_lon_cluster = c4.number_input(
        "Cluster ID",
        min_value=0,
        value=1
    )

    dist_to_sf = c5.number_input(
        "Distance to SF",
        value=10.0
    )

    dist_to_la = st.number_input(
        "Distance to LA",
        value=350.0
    )

    st.divider()

    st.subheader("🏡 Property Details")

    c6, c7 = st.columns(2)

    total_rooms = c6.number_input(
        "Total Rooms",
        min_value=1,
        value=1500
    )

    total_bedrooms = c7.number_input(
        "Total Bedrooms",
        min_value=1,
        value=300
    )

    housing_median_age = st.slider(
        "Housing Median Age",
        1,
        100,
        30
    )

    st.divider()

    st.subheader("👨‍👩‍👧 Demographics & Income")

    c8, c9 = st.columns(2)

    population = c8.number_input(
        "Population",
        min_value=1,
        value=1000
    )

    households = c9.number_input(
        "Households",
        min_value=1,
        value=400
    )

    c10, c11, c12 = st.columns(3)

    median_income = c10.number_input(
        "Median Income",
        value=4.5
    )

    rooms_per_bedrooms = c11.number_input(
        "Rooms / Bedroom",
        value=5.0
    )

    rooms_per_households = c12.number_input(
        "Rooms / Household",
        value=4.0
    )

    income_per_age = st.number_input(
        "Income / Age Ratio",
        value=0.15
    )

    submitted = st.form_submit_button(
        "🔮 Predict Price",
        use_container_width=True
    )

# -------------------------------------------------
# PREDICTION
# -------------------------------------------------
if submitted:

    if model is None:
        st.error("Model not loaded.")
        st.stop()

    input_df = pd.DataFrame([{
        "ocean_proximity": ocean_proximity,
        "housing_median_age": housing_median_age,
        "total_rooms": total_rooms,
        "total_bedrooms": total_bedrooms,
        "population": population,
        "households": households,
        "median_income": median_income,
        "rooms_per_bedrooms": rooms_per_bedrooms,
        "rooms_per_households": rooms_per_households,
        "income_per_age": income_per_age,
        "longitude": longitude,
        "latitude": latitude,
        "dist_to_sf": dist_to_sf,
        "dist_to_la": dist_to_la,
        "lat_lon_cluster": lat_lon_cluster
    }])

    try:

        with st.status(
            "Running Prediction...",
            expanded=True
        ) as status:

            st.write("Loading Model...")
            time.sleep(1)

            st.write("Processing Features...")
            time.sleep(1)

            st.write("Generating Prediction...")
            prediction = model.predict(input_df)

            time.sleep(1)

            status.update(
                label="Prediction Completed ✅",
                state="complete"
            )

        # Reverse Log Transform
        price = float(np.expm1(prediction[0]))

        st.balloons()

        # -----------------------------------------
        # CATEGORY
        # -----------------------------------------
        if price < 250000:
            category = "Budget House 🏠"
        elif price < 500000:
            category = "Mid Range House 🏡"
        elif price < 750000:
            category = "Premium House 🏘️"
        else:
            category = "Luxury House 🏰"

        st.success(
            f"Estimated Market Value: ${price:,.0f}"
        )

        st.info(f"Category: {category}")

        # -----------------------------------------
        # METRICS
        # -----------------------------------------
        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Predicted Price",
            f"${price:,.0f}"
        )

        m2.metric(
            "Median Income",
            median_income
        )

        m3.metric(
            "House Age",
            housing_median_age
        )

        # -----------------------------------------
        # GAUGE CHART
        # -----------------------------------------
        max_price = max(price * 1.2, 1000000)

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=price,
                number={"prefix": "$"},
                title={"text": "Predicted House Price"},
                gauge={
                    "axis": {
                        "range": [0, max_price]
                    },
                    "bar": {
                        "thickness": 0.3
                    },
                    "steps": [
                        {
                            "range": [0, max_price*0.25],
                            "color": "lightgray"
                        },
                        {
                            "range": [max_price*0.25, max_price*0.50],
                            "color": "gray"
                        },
                        {
                            "range": [max_price*0.50, max_price*0.75],
                            "color": "lightgreen"
                        },
                        {
                            "range": [max_price*0.75, max_price],
                            "color": "green"
                        }
                    ]
                }
            )
        )

        gauge.update_layout(height=450)

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

        # -----------------------------------------
        # BAR CHART
        # -----------------------------------------
        chart_df = pd.DataFrame({
            "Category": [
                "Budget",
                "Mid Range",
                "Premium",
                "Luxury",
                "Predicted"
            ],
            "Price": [
                250000,
                500000,
                750000,
                1000000,
                price
            ]
        })

        bar_chart = px.bar(
            chart_df,
            x="Category",
            y="Price",
            text="Price",
            title="Price Comparison Chart"
        )

        bar_chart.update_traces(
            texttemplate='$%{y:,.0f}',
            textposition='outside'
        )

        st.plotly_chart(
            bar_chart,
            use_container_width=True
        )

        # -----------------------------------------
        # INPUT SUMMARY
        # -----------------------------------------
        st.subheader("📋 Input Summary")

        st.dataframe(
            input_df,
            use_container_width=True
        )

        # -----------------------------------------
        # DOWNLOAD RESULT
        # -----------------------------------------
        result_df = pd.DataFrame({
            "Predicted Price": [price],
            "Category": [category]
        })

        csv = result_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Prediction CSV",
            data=csv,
            file_name="house_prediction.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Prediction Failed: {e}")