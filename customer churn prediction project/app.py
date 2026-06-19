import numpy as np
import pandas as pd
import streamlit as st
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title='Customer Churn Predictor AI',
    page_icon='📊',      
    layout='centered'   
)

st.title("📊 Customer Churn Prediction App")
st.markdown("Enter customer details below to evaluate their risk of churning in real-time.")
st.divider()

@st.cache_resource()
def load_my_model():
    try:
        return joblib.load('final_churn_model_lightgbm.pkl')
    except Exception as e:
        st.error(f"Model Path Error: {e}")
        return None

model = load_my_model()

st.sidebar.title('🧭 Navigation')
st.sidebar.header('System Info')
if model is not None:
    st.sidebar.success('✅ Model Ready')
else:
    st.sidebar.error('❌ Model Not Ready')

col1, col2 = st.columns(2)

with col1:
    age = st.number_input('Enter Your Age:', min_value=18, max_value=65, value=30)
    tenure = st.number_input('Enter Tenure (Months):', min_value=1, max_value=60, value=12)
    Usage_Frequency = st.number_input('Enter Usage Frequency:', min_value=1, max_value=30, value=10)
    Support_Calls = st.number_input('Enter Support Calls:', min_value=0, max_value=10, value=2)
    Payment_Delay = st.number_input('Enter Payment Delay (Days):', min_value=0, max_value=30, value=5)
    Monthly_Spend = st.number_input('Enter Monthly Spend ($):', min_value=10, max_value=1000, value=100)

with col2:
    gender = st.selectbox('Gender:', ['Male', 'Female'])
    Subscription_type = st.selectbox('Subscription Type:', ['Basic', 'Standard', 'Premium'])
    Contract_Length = st.selectbox('Contract Length:', ['Monthly', 'Annual', 'Quarterly'])

data = pd.DataFrame({
    "Gender": [gender],
    "Subscription Type": [Subscription_type],
    "Contract Length": [Contract_Length],
    "Age": [age],
    "Tenure": [tenure],
    "Usage Frequency": [Usage_Frequency],
    "Support Calls": [Support_Calls],
    "Payment Delay": [Payment_Delay],
    "Monthly Spend": [Monthly_Spend]
})

if st.button('Predict Churn', type='primary', use_container_width=True):
    if model is not None:
        with st.status("Analyzing Customer Behavioral Data...", expanded=True) as status:
            prediction = model.predict(data)
            prob_score = model.predict_proba(data)[0, 1] * 100
            
            status.update(label="Analysis Complete!", state="complete", expanded=False)
            
            st.markdown("### 🎯 Prediction Results")
            st.divider()
            
            if prediction[0] == 1:
                st.error(f"🚨 **Verdict:** The customer is highly likely to **CHURN**.")
                st.metric(label="Churn Risk Probability", value=f"{prob_score:.2f}%", delta="High Risk", delta_color="inverse")
            else:
                st.balloons()
                st.success(f"✅ **Verdict:** The customer is loyal and **WILL STAY**.")
                st.metric(label="Churn Risk Probability", value=f"{prob_score:.2f}%", delta="Safe / Low Risk", delta_color="normal")
            
            st.markdown("### 📈 Customer Metrics vs Churn Benchmarks")
            st.write("Comparing current inputs with high-risk baselines identified during EDA:")
            
            fig, ax = plt.subplots(1, 2, figsize=(10, 4))
            
            sns.barplot(x=['Current Input', 'Churn Avg Baseline'], y=[Support_Calls, 5.4], 
                        palette=['#1f77b4', '#d62728'], ax=ax[0])
            ax[0].set_title('Support Calls Friction')
            ax[0].set_ylabel('Number of Calls')
            
            sns.barplot(x=['Current Input', 'Churn Avg Baseline'], y=[Payment_Delay, 23.0], 
                        palette=['#1f77b4', '#d62728'], ax=ax[1])
            ax[1].set_title('Payment Delay Friction')
            ax[1].set_ylabel('Days Delayed')
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            if Support_Calls >= 6:
                st.warning("⚠️ **Friction Alert:** This customer has an exceptionally high number of support calls. Product or system integration issues require immediate engineering review.")
            if Payment_Delay >= 20:
                st.warning("⚠️ **Financial Alert:** Payment delay is in the critical red zone (>20 days). This is a strong behavioral signal of complete platform disengagement.")

            st.markdown("### 🧠 Model Decision Insights (Feature Importance)")
            st.write("This chart explains which features the LightGBM model relied on most to calculate this specific prediction:")
            
            try:
                lgb_model = model.named_steps[list(model.named_steps.keys())[-1]]
                feature_names = model.named_steps['Preprocessing Data'].get_feature_names_out()
                importances = lgb_model.feature_importances_
                
                feat_imp_df = pd.DataFrame({
                    'Feature': feature_names,
                    'Importance': importances
                }).sort_values(by='Importance', ascending=False)
                
                fig_imp, ax_imp = plt.subplots(figsize=(10, 5))
                sns.barplot(data=feat_imp_df, x='Importance', y='Feature', palette='viridis', ax=ax_imp)
                ax_imp.set_title('Global Feature Importance Breakdown', fontsize=12, fontweight='bold')
                ax_imp.set_xlabel('Relative Importance Weight')
                
                st.pyplot(fig_imp)
                plt.close()
                
                st.info("💡 **Data Science Insight:** If the risk shows 0.00% despite high support calls/delays, look at the top features above (like Contract Length or Tenure). Their strong positive retention weight overrides current operational friction.")
            except:
                pass