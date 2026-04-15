import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(page_title="Expense Tracker Pro", layout="wide")

# --------------------------
# SESSION STATE (LOGIN + THEME)
# --------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# --------------------------
# LOGIN SYSTEM
# --------------------------
if not st.session_state.logged_in:
    st.title("🔐 Login to Expense Tracker")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful!")
        else:
            st.error("Invalid Credentials")

    st.stop()

# --------------------------
# DARK / LIGHT MODE
# --------------------------
toggle = st.sidebar.toggle("🌙 Dark Mode")

if toggle:
    st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(120deg, #f6d365, #fda085, #a1c4fd);
    }
    </style>
    """, unsafe_allow_html=True)

# --------------------------
# LOAD DATA
# --------------------------
df = pd.read_csv("data/processed_expenses.csv")
df['date'] = pd.to_datetime(df['date'])

# --------------------------
# SIDEBAR FILTERS
# --------------------------
st.sidebar.title("🎛️ Filters")

category_filter = st.sidebar.multiselect(
    "Category",
    df['category'].unique(),
    default=df['category'].unique()
)

type_filter = st.sidebar.selectbox(
    "Type",
    ["All", "Expense", "Income"]
)

filtered_df = df[df['category'].isin(category_filter)]

if type_filter != "All":
    filtered_df = filtered_df[filtered_df['type'] == type_filter]

# --------------------------
# HEADER
# --------------------------
st.title("💰 Expense Tracker Pro Dashboard")

# --------------------------
# METRICS
# --------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Transactions", len(filtered_df))
col2.metric("Total ₹", f"{filtered_df['amount'].sum():,.2f}")
col3.metric("Avg ₹", f"{filtered_df['amount'].mean():,.2f}")

# --------------------------
# BUDGET ALERT SYSTEM
# --------------------------
st.sidebar.subheader("💸 Budget Tracker")

budget = st.sidebar.number_input("Set Monthly Budget", value=50000)

total_spent = filtered_df['amount'].sum()

if total_spent > budget:
    st.sidebar.error("🚨 Budget Exceeded!")
else:
    st.sidebar.success("✅ Within Budget")

# --------------------------
# CHARTS
# --------------------------
col1, col2 = st.columns(2)

with col1:
    cat_data = filtered_df.groupby('category')['amount'].sum().reset_index()
    fig = px.bar(cat_data, x='category', y='amount', color='category')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    monthly = filtered_df.groupby('month')['amount'].sum().reset_index()
    fig2 = px.line(monthly, x='month', y='amount', markers=True)
    st.plotly_chart(fig2, use_container_width=True)

# --------------------------
# PIE + INSIGHTS
# --------------------------
col1, col2 = st.columns([2,1])

with col1:
    pie = filtered_df[filtered_df['type']=="Expense"]
    pie_data = pie.groupby('category')['amount'].sum().reset_index()
    fig3 = px.pie(pie_data, names='category', values='amount', hole=0.4)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("💡 Smart Insights")

    if not filtered_df.empty:
        top_cat = cat_data.sort_values(by='amount', ascending=False).iloc[0]['category']
        avg = filtered_df['amount'].mean()

        st.write(f"👉 Top Category: {top_cat}")
        st.write(f"👉 Avg Spend: ₹{avg:.2f}")

        if avg > 3000:
            st.warning("⚠️ High spending behavior detected!")
        else:
            st.success("✅ Healthy spending habits!")

# --------------------------
# DOWNLOAD REPORT
# --------------------------
st.subheader("📄 Download Report")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="expense_report.csv",
    mime="text/csv",
)

# --------------------------
# TOP TRANSACTIONS
# --------------------------
st.subheader("🏆 Top Transactions")

top = filtered_df.sort_values(by='amount', ascending=False).head(5)
st.dataframe(top)

# --------------------------
# FOOTER
# --------------------------
st.markdown("---")
st.markdown("🚀 Built by You | Advanced FinTech Dashboard")