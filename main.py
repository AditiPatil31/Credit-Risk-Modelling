import streamlit as st
from prediction_helper import predict

if "sim_income" not in st.session_state:
    st.session_state.sim_income = 1200000

if "sim_loan_amount" not in st.session_state:
    st.session_state.sim_loan_amount = 2560000

if "sim_credit_util" not in st.session_state:
    st.session_state.sim_credit_util = 30
# -----------------------------
# Page Config
# -----------------------------
st.title("🏦 Lauki Finance")
st.markdown("### AI Powered Credit Risk Assessment System")

st.markdown("---")

# Sidebar Branding
st.sidebar.title("📊 Model Info")
st.sidebar.markdown("""
**Score Range:** 300 – 900  

**Risk Bands:**

🔴 **Poor** (300–499)  
🟠 **Average** (500–649)  
🟡 **Good** (650–749)  
🟢 **Excellent** (750–900)
""")

# ===============================
# APPLICANT PROFILE SECTION
# ===============================
st.markdown("## 👤 Applicant Profile")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input('Age', min_value=18, max_value=100, value=28)

with col2:
    income = st.number_input('Annual Income (₹)', min_value=0, value=1200000)

with col3:
    residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])

st.markdown("---")

# ===============================
# LOAN DETAILS SECTION
# ===============================
st.markdown("## 💰 Loan Details")

col4, col5, col6 = st.columns(3)

with col4:
    loan_amount = st.number_input('Loan Amount (₹)', min_value=0, value=2560000)

with col5:
    loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, value=36)

with col6:
    loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])

loan_to_income_ratio = loan_amount / income if income > 0 else 0
st.metric("📊 Loan to Income Ratio", f"{loan_to_income_ratio:.2f}")

st.markdown("---")

# ===============================
# CREDIT BEHAVIOUR SECTION
# ===============================
st.markdown("## 📈 Credit Behaviour")

col7, col8, col9 = st.columns(3)

with col7:
    avg_dpd_per_delinquency = st.number_input('Avg DPD', min_value=0, value=20)

with col8:
    delinquency_ratio = st.number_input('Delinquency Ratio (%)', 0, 100, 30)

with col9:
    credit_utilization_ratio = st.number_input('Credit Utilization Ratio (%)', 0, 100, 30)

col10, col11 = st.columns(2)

with col10:
    num_open_accounts = st.number_input('Open Loan Accounts', 1, 10, 2)

with col11:
    loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])

st.markdown(" ")
st.markdown("---")

# -----------------------------
# Calculate Risk Button (UNCHANGED)
# -----------------------------
if st.button('Calculate Risk'):
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure_months,
        avg_dpd_per_delinquency,
        delinquency_ratio, credit_utilization_ratio,
        num_open_accounts,
        residence_type, loan_purpose, loan_type
    )

    # Store in session state
    st.session_state.base_probability = probability
    st.session_state.base_credit_score = credit_score
    st.session_state.base_rating = rating

    # Store latest inputs for What-If defaults
    st.session_state.sim_income = income
    st.session_state.sim_loan_amount = loan_amount
    st.session_state.sim_credit_util = credit_utilization_ratio

# -----------------------------
# Show Base Result (if exists)
# -----------------------------
if "base_credit_score" in st.session_state:

    probability = st.session_state.base_probability
    credit_score = st.session_state.base_credit_score
    rating = st.session_state.base_rating

    st.subheader("📊 Risk Assessment Result")

    if rating == "Poor":
        st.error(f"🔴 Rating: {rating}")
    elif rating == "Average":
        st.warning(f"🟠 Rating: {rating}")
    elif rating == "Good":
        st.info(f"🟡 Rating: {rating}")
    elif rating == "Excellent":
        st.success(f"🟢 Rating: {rating}")

    col1, col2 = st.columns(2)
    col1.metric("Default Probability", f"{probability:.2%}")
    col2.metric("Credit Score", credit_score)

    st.progress(int((credit_score - 300) / 600 * 100))

    st.divider()

    # -----------------------------
    # WHAT IF SIMULATOR (LIVE)
    # -----------------------------
    st.subheader("🔮 What-If Simulator")

    # Store latest inputs for What-If defaults
    sim_income = st.slider(
        "Simulated Income (₹)",
        100000, 5000000,
        key="sim_income"
    )

    sim_loan_amount = st.slider(
        "Simulated Loan Amount (₹)",
        100000, 10000000,
        key="sim_loan_amount"
    )

    sim_credit_util = st.slider(
        "Simulated Credit Utilization (%)",
        0, 100,
        key="sim_credit_util"
    )
    # LIVE recalculation (no button needed)
    sim_probability, sim_credit_score, sim_rating = predict(
        age, sim_income, sim_loan_amount, loan_tenure_months,
        avg_dpd_per_delinquency,
        delinquency_ratio, sim_credit_util,
        num_open_accounts,
        residence_type, loan_purpose, loan_type
    )

    col3, col4 = st.columns(2)
    col3.metric(
        "New Credit Score",
        sim_credit_score,
        sim_credit_score - credit_score
    )
    col4.metric(
        "New Default Probability",
        f"{sim_probability:.2%}"
    )

    if sim_credit_score > credit_score:
        st.success("✅ Risk Improved")
    elif sim_credit_score < credit_score:
        st.error("⚠ Risk Increased")



