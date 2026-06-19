import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# =====================================================================================
# Page Config
# =====================================================================================
st.set_page_config(
    page_title="Crop Recommendation System",
    page_icon="🌱",
    layout="centered"
)

# =====================================================================================
# Load Model & Encoder (cached so it loads only once)
# =====================================================================================
MODEL_PATH = "crop_best_rf_model.pkl"
ENCODER_PATH = "label_encoder.pkl"

@st.cache_resource
def load_artifacts():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH):
        return None, None
    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)
    return model, encoder

model, encoder = load_artifacts()

# =====================================================================================
# Header
# =====================================================================================
st.title("🌱 Crop Recommendation System")
if model is None or encoder is None:
    st.error(
        f"Model files not found `{MODEL_PATH}` aur `{ENCODER_PATH}`  "
    )
    st.stop()

st.divider()

# =====================================================================================
# Input Form
# =====================================================================================
st.subheader("📋 Soil & Climate Parameters")

col1, col2 = st.columns(2)

with col1:
    N = st.slider("Nitrogen (N)", min_value=0, max_value=140, value=50)
    P = st.slider("Phosphorus (P)", min_value=5, max_value=145, value=50)
    K = st.slider("Potassium (K)", min_value=5, max_value=205, value=50)
    temperature = st.slider("Temperature (°C)", min_value=8.0, max_value=44.0, value=25.0, step=0.1)

with col2:
    humidity = st.slider("Humidity (%)", min_value=14.0, max_value=100.0, value=70.0, step=0.1)
    ph = st.slider("Soil pH", min_value=3.5, max_value=10.0, value=6.5, step=0.1)
    rainfall = st.slider("Rainfall (mm)", min_value=20.0, max_value=300.0, value=100.0, step=0.1)

st.divider()

# =====================================================================================
# Prediction
# =====================================================================================
if st.button("🔍 Predict Best Crop", use_container_width=True):
    input_df = pd.DataFrame([{
        "temperature": temperature,
        "ph": ph,
        "N": N,
        "P": P,
        "K": K,
        "humidity": humidity,
        "rainfall": rainfall
    }])

    pred_encoded = model.predict(input_df)[0]
    pred_crop = encoder.inverse_transform([pred_encoded])[0]

    st.success(f"✅ Recommended Crop: **{pred_crop.upper()}**")

    # Show top-5 probabilities if the model supports it
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(input_df)[0]
        all_crops = encoder.inverse_transform(np.arange(len(proba)))
        proba_df = pd.DataFrame({"Crop": all_crops, "Probability": proba})
        proba_df = proba_df.sort_values("Probability", ascending=False).head(5).reset_index(drop=True)

        st.subheader("📊 Top 5 Likely Crops")
        st.bar_chart(proba_df.set_index("Crop")["Probability"])
        st.dataframe(proba_df, use_container_width=True, hide_index=True)

st.divider()
st.caption("Model: RandomForestClassifier (tuned) | Built with the Crop_recommendation dataset pipeline")