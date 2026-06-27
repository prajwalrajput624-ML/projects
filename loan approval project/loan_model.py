
import pandas as pd
import numpy as np
import streamlit as st
import joblib
import time
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title='Loan Approval System',
    page_icon='💰',
    layout='wide'
)

# ─────────────────────────────────────────────
# MODEL LOADING 
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
@st.cache_resource()
def load_my_model():
    try:
        return joblib.load(os.path.join(BASE_DIR, 'final_loan_model_GB.pkl'))
    except Exception as e:
        st.error(f"Model Path Error: {e}")
        return None
    
model = load_my_model()

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
    <style>
    /* Main predict button */
    div.stButton > button {
        font-size: 18px !important;
        font-weight: bold !important;
        height: 55px !important;
        width: 260px !important;
        border-radius: 10px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    /* Result card styling */
    .result-approved {
        background: linear-gradient(135deg, #1a7a4a, #2ecc71);
        border-radius: 14px;
        padding: 24px 32px;
        color: white;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        margin-top: 16px;
    }
    .result-rejected {
        background: linear-gradient(135deg, #922b21, #e74c3c);
        border-radius: 14px;
        padding: 24px 32px;
        color: white;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        margin-top: 16px;
    }
    .metric-card {
        background: #1e2130;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.title('💻 Navigation')
st.sidebar.divider()

st.sidebar.header('⚙️ Risk Controls')
risk_threshold = st.sidebar.slider(
    label="Max Acceptable Default Risk (%)",
    min_value=5.0,
    max_value=95.0,
    value=50.0,
    step=1.0,
    help="Applications exceeding this risk percentage will be flagged for rejection."
)

st.sidebar.divider()
st.sidebar.header('System Info')
if model is not None:
    st.sidebar.success("Model: Ready 🟢")
    try:
        st.sidebar.caption(f"Model type: `{type(model).__name__}`")
    except Exception:
        pass
else:
    st.sidebar.error("Model: Offline 🔴")
    st.sidebar.warning("Ensure 'final_loan_model_GB.pkl' is placed in /app (root directory).")

st.sidebar.divider()
st.sidebar.caption("Risk threshold controls when a loan is auto-rejected. Lower = stricter.")

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("💰 Loan Approval System")
st.caption("AI-powered underwriting engine using Gradient Boosting. Adjust the risk threshold in the sidebar.")
st.divider()

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
mode_tab1, mode_tab2, mode_tab3 = st.tabs([
    "👤 Single Application",
    "📁 Bulk CSV Processing",
    "📊 Risk Insights"
])

# ─────────────────────────────────────────────
# TAB 1 — MANUAL SINGLE ENTRY
# ─────────────────────────────────────────────
with mode_tab1:
    st.subheader("Applicant Profile")
    st.caption("Fill in the applicant's details and click Predict.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Personal Details**")
        age = st.number_input("Age", min_value=18, max_value=65, value=25)
        income = st.number_input("Annual Income (₹)", min_value=10000, max_value=250000, value=50000, step=1000)
        experience = st.number_input("Employment Experience (years)", min_value=0, max_value=25, value=3)

    with col2:
        st.markdown("**Profile Details**")
        # Fixed: match training data encoding exactly
        home_ownership = st.selectbox(
            "Home Ownership",
            ['RENT', 'MORTGAGE', 'OWN', 'OTHER'],
            format_func=lambda x: x.title()
        )
        loan_intent = st.selectbox(
            "Loan Purpose",
            ['EDUCATION', 'MEDICAL', 'VENTURE', 'PERSONAL', 'DEBTCONSOLIDATION', 'HOMEIMPROVEMENT'],
            format_func=lambda x: x.replace('DEBTCONSOLIDATION', 'Debt Consolidation')
                                    .replace('HOMEIMPROVEMENT', 'Home Improvement')
                                    .title()
        )
        age_category = st.selectbox(
            'Age Category',
            ['18-25', '26-35', '36-45', '46-60', '60+']
        )

    with col3:
        st.markdown("**Loan Details**")
        loan_amount = st.number_input("Loan Amount (₹)", min_value=1000, max_value=200000, value=10000, step=500)
        loan_percent_income = st.number_input(
            "Loan as % of Income (0.0–1.0)",
            min_value=0.0, max_value=1.0, step=0.01, value=0.2,
            help="E.g. 0.2 means the loan is 20% of annual income"
        )
        credit_history_length = st.number_input("Credit History Length (years)", min_value=0, max_value=40, value=5)

    st.markdown("---")
    col4, col5 = st.columns(2)
    with col4:
        loan_int_rate = st.slider("Loan Interest Rate (%)", min_value=5.0, max_value=25.0, step=0.1, value=11.0)
    with col5:
        credit_score = st.slider("Credit Score", min_value=300, max_value=850, value=650)

    credit_score_category = st.selectbox(
        "Credit Score Category",
        ['Low', 'Moderate', 'High'],
        help="Low: 300–579 | Moderate: 580–669 | High: 670+"
    )

    # Build input DataFrame
    input_data = pd.DataFrame({
        'person_age': [age],
        'person_income': [income],
        'person_emp_exp': [experience],
        'loan_amnt': [loan_amount],
        'loan_percent_income': [loan_percent_income],
        'cb_person_cred_hist_length': [credit_history_length],
        'credit_score': [credit_score],
        'person_home_ownership': [home_ownership],
        'loan_intent': [loan_intent],
        'person_age_category': [age_category],
        'credit_score_category': [credit_score_category],
        'loan_int_rate': [loan_int_rate]
    })

    st.markdown("---")

    btn_col, _ = st.columns([1, 3])
    with btn_col:
        predict_clicked = st.button('🔍 Predict', type='primary', use_container_width=True)

    if predict_clicked:
        if model is None:
            st.error("Model is not loaded. Cannot make predictions.")
        else:
            with st.status("Analyzing applicant profile...", expanded=True) as status:
                st.write("🔄 Running risk assessment...")
                time.sleep(0.8)
                st.write("📊 Calculating default probability...")
                time.sleep(0.6)

                try:
                    probabilities = model.predict_proba(input_data)
                    prob_rejected = probabilities[0][1] * 100
                    prob_approved = probabilities[0][0] * 100
                    final_decision = 1 if prob_rejected >= risk_threshold else 0
                    status.update(label="Analysis Complete!", state='complete', expanded=False)
                except Exception as pred_err:
                    status.update(label="Prediction Failed", state='error', expanded=False)
                    st.error(f"Prediction error: {pred_err}")
                    st.stop()

            # ── Result Card ──
            if final_decision == 0:
                st.balloons()
                st.markdown(f"""
                    <div class="result-approved">
                        🎉 Loan Approved!<br>
                        <span style="font-size:16px;font-weight:normal;">
                            Approval Confidence: {prob_approved:.1f}% &nbsp;|&nbsp; Default Risk: {prob_rejected:.1f}%
                        </span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="result-rejected">
                        ❌ Loan Rejected<br>
                        <span style="font-size:16px;font-weight:normal;">
                            Default Risk: {prob_rejected:.1f}% &nbsp;|&nbsp; Threshold: {risk_threshold:.0f}%
                        </span>
                    </div>
                """, unsafe_allow_html=True)

            # ── Probability Metrics ──
            st.markdown("### 📊 Probability Breakdown")
            m1, m2, m3 = st.columns(3)
            m1.metric("✅ Approval Probability", f"{prob_approved:.1f}%")
            m2.metric("⚠️ Default Risk", f"{prob_rejected:.1f}%")
            m3.metric("🎯 Risk Threshold", f"{risk_threshold:.0f}%")

            # ── Risk Bar ──
            st.markdown("**Default Risk Level**")
            st.progress(min(prob_rejected / 100, 1.0))

            # ── Input Summary ──
            with st.expander("📋 View Submitted Application Data"):
                st.dataframe(input_data, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# TAB 2 — BULK CSV PROCESSING
# ─────────────────────────────────────────────
with mode_tab2:
    st.subheader("Batch Loan Evaluation")
    st.caption("Upload a CSV file with multiple applicant records for bulk underwriting decisions.")

    with st.expander("📌 Required CSV Column Format"):
        required_cols = [
            'person_age', 'person_income', 'person_emp_exp', 'loan_amnt',
            'loan_percent_income', 'cb_person_cred_hist_length', 'credit_score',
            'person_home_ownership', 'loan_intent', 'person_age_category',
            'credit_score_category', 'loan_int_rate'
        ]
        st.code(", ".join(required_cols))
        st.caption("Column names must match exactly. `person_home_ownership` values: RENT / MORTGAGE / OWN / OTHER")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            raw_csv_data = pd.read_csv(uploaded_file)
        except Exception as read_err:
            st.error(f"Failed to read CSV: {read_err}")
            st.stop()

        st.success(f"✅ File uploaded: **{uploaded_file.name}** — {len(raw_csv_data):,} records found")

        # ── Show CSV columns for debugging ──
        with st.expander("🔍 Detected CSV Columns (click to verify)"):
            st.write(list(raw_csv_data.columns))
            st.dataframe(raw_csv_data.head(3), use_container_width=True)

        required_features = [
            'person_age', 'person_income', 'person_emp_exp', 'loan_amnt',
            'loan_percent_income', 'cb_person_cred_hist_length', 'credit_score',
            'person_home_ownership', 'loan_intent', 'person_age_category',
            'credit_score_category', 'loan_int_rate'
        ]

        # ── Auto-fix: strip whitespace from column names ──
        raw_csv_data.columns = raw_csv_data.columns.str.strip()

        # ── Auto-fix: uppercase categorical columns ──
        for cat_col in ['person_home_ownership', 'loan_intent']:
            if cat_col in raw_csv_data.columns:
                raw_csv_data[cat_col] = raw_csv_data[cat_col].astype(str).str.strip().str.upper()

        # ── Auto-fix: loan_intent common variations ──
        intent_map = {
            'DEBT CONSOLIDATION': 'DEBTCONSOLIDATION',
            'DEBT_CONSOLIDATION': 'DEBTCONSOLIDATION',
            'HOME IMPROVEMENT': 'HOMEIMPROVEMENT',
            'HOME_IMPROVEMENT': 'HOMEIMPROVEMENT',
        }
        if 'loan_intent' in raw_csv_data.columns:
            raw_csv_data['loan_intent'] = raw_csv_data['loan_intent'].replace(intent_map)

        # ── Check missing columns ──
        missing_cols = [c for c in required_features if c not in raw_csv_data.columns]
        if missing_cols:
            st.error(f"❌ Missing columns in CSV: `{', '.join(missing_cols)}`")
            st.info("💡 Make sure your CSV has exactly these column names (case-sensitive).")
        else:
            st.info(f"✅ All required columns found. Ready to process **{len(raw_csv_data):,}** records.")

            if st.button("🚀 Run Bulk Predictions", type="primary", key="bulk_btn"):
                if model is None:
                    st.error("Model is not loaded. Cannot process predictions.")
                else:
                    with st.status("Processing batch records...", expanded=True) as status:
                        st.write(f"🔄 Evaluating {len(raw_csv_data):,} applications...")
                        try:
                            input_batch = raw_csv_data[required_features].copy()

                            # Show sample of what's going into model
                            st.write("📋 Sample input (first row):")
                            st.json(input_batch.iloc[0].to_dict())

                            bulk_probabilities = model.predict_proba(input_batch)

                            raw_csv_data['Default_Risk_%'] = (bulk_probabilities[:, 1] * 100).round(2)
                            raw_csv_data['Approval_Probability_%'] = (bulk_probabilities[:, 0] * 100).round(2)
                            raw_csv_data['Decision'] = np.where(
                                bulk_probabilities[:, 1] * 100 >= risk_threshold,
                                '❌ Rejected',
                                '✅ Approved'
                            )

                            time.sleep(0.5)
                            status.update(label="Bulk Processing Complete!", state='complete', expanded=False)

                        except ValueError as val_err:
                            status.update(label="Processing Failed", state='error', expanded=False)
                            st.error(f"❌ Value Error: {val_err}")
                            st.warning("This usually means a categorical column has unexpected values. Check `person_home_ownership` and `loan_intent` columns.")
                            st.stop()
                        except Exception as csv_err:
                            status.update(label="Processing Failed", state='error', expanded=False)
                            st.error(f"❌ Prediction Error: {csv_err}")
                            st.stop()

                    # ── Summary metrics ──
                    approved_count = (raw_csv_data['Decision'] == '✅ Approved').sum()
                    rejected_count = (raw_csv_data['Decision'] == '❌ Rejected').sum()

                    st.markdown("### 📊 Batch Results Summary")
                    s1, s2, s3, s4 = st.columns(4)
                    s1.metric("Total Applications", f"{len(raw_csv_data):,}")
                    s2.metric("✅ Approved", f"{approved_count:,}")
                    s3.metric("❌ Rejected", f"{rejected_count:,}")
                    s4.metric("Approval Rate", f"{approved_count / len(raw_csv_data) * 100:.1f}%")

                    st.dataframe(raw_csv_data, use_container_width=True)

                    output_csv = raw_csv_data.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Results CSV",
                        data=output_csv,
                        file_name="loan_batch_predictions.csv",
                        mime="text/csv"
                    )

# ─────────────────────────────────────────────
# TAB 3 — RISK INSIGHTS
# ─────────────────────────────────────────────
with mode_tab3:
    st.subheader("📊 Loan Risk Insights Dashboard")
    st.caption("Analysis based on 7,987 loan defaulters from the Credit Risk Dataset.")
    st.divider()

    # KPIs
    st.markdown("#### 🔢 Key Metrics")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Defaulters", "7,987")
    k2.metric("Average Age", "26.4 yrs")
    k3.metric("Avg Debt-to-Income", "20%")
    k4.metric("Avg Interest Rate", "12.75%")

    st.divider()

    # Demographics
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 👤 Gender Distribution")
        gender_data = pd.DataFrame({"Gender": ["Male", "Female"], "Count": [4377, 3610]})
        st.bar_chart(gender_data.set_index("Gender"))

    with col_b:
        st.markdown("#### 🎂 Age Bracket Breakdown")
        age_data = pd.DataFrame({"Age Group": ["18–25", "26–35", "36–45"], "Defaulters": [4134, 3561, 292]})
        st.bar_chart(age_data.set_index("Age Group"))

    st.divider()

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("#### 🏠 Home Ownership")
        housing_data = pd.DataFrame({
            "Type": ["Rent", "Mortgage", "Own", "Other"],
            "Count": [6168, 1614, 177, 28]
        })
        st.bar_chart(housing_data.set_index("Type"))

    with col_d:
        st.markdown("#### 🎓 Education Level")
        edu_data = pd.DataFrame({
            "Degree": ["Bachelor's", "High School", "Associate", "Master's", "Doctorate"],
            "Count": [2496, 2092, 2056, 1247, 96]
        })
        st.bar_chart(edu_data.set_index("Degree"))

    st.divider()

    st.markdown("#### 📋 Loan Intent Distribution")
    intent_data = pd.DataFrame({
        "Intent": ["Medical", "Debt Consolidation", "Education", "Personal", "Home Improvement", "Venture"],
        "Accounts": [1901, 1714, 1241, 1219, 1022, 890]
    })
    st.bar_chart(intent_data.set_index("Intent"))

    st.divider()

    st.markdown("#### 🎯 Credit Score Distribution Among Defaulters")
    credit_data = pd.DataFrame({
        "Score Range": ["400–600 (Poor/Fair)", "600–800 (Good/Excellent)"],
        "Defaulters": [1995, 5992]
    })
    st.bar_chart(credit_data.set_index("Score Range"))
    st.info("💡 **Insight:** ~75% of defaulters had a 'Good/Excellent' credit score — credit score alone is NOT a reliable risk filter.")

    st.divider()

    st.markdown("#### 📈 Top Correlations with Default Risk")
    corr_data = pd.DataFrame({
        "Feature": ["Loan Percent Income", "Loan Interest Rate", "Loan Amount"],
        "Correlation": [0.38, 0.33, 0.11],
        "Risk Level": ["🚨 Highest", "🚨 High", "⚠️ Medium"],
        "Key Insight": [
            "Debt exceeding 20% of income leads to cash flow collapse",
            "Avg 12.8% rate; high rates crush early-career borrowers",
            "Large loans are only risky when paired with low income"
        ]
    })
    st.dataframe(corr_data, use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("#### 🔍 The Clean Sheet Paradox")
    st.warning("⚠️ **100% of the 7,987 defaulters had NO previous loan defaults on file.** "
               "Every default was a first-time event — a spotless history gave a false sense of security.")
