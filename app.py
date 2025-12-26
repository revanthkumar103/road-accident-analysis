import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="Road Accident Analysis", layout="wide")

# ---------------------------
# Session State for Login
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------
# LOGIN PAGE
# ---------------------------
# ---------------------------
# LOGIN PAGE
# ---------------------------
def login_page():
    st.markdown("<h2 style='text-align:center;'>🚦 eDAR – Road Accident Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>Sign In</h4>", unsafe_allow_html=True)
    st.write("")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        department = st.selectbox(
            "Department",
            ["Select Department", "Transport Department", "Police Department", "Road Safety Authority"]
        )

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        captcha = st.text_input("Captcha", placeholder="Enter P173Ha")

        st.caption("Demo Captcha: **P173Ha**")

        if st.button("Sign In"):
            if (
                department.strip() == "Transport Department"
                and username.strip() == "admin"
                and password.strip() == "admin123"
                and captcha.strip() == "P173Ha"
            ):
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid login details")



# ---------------------------
# DASHBOARD PAGE
# ---------------------------
def dashboard_page():
    st.title("🚦 Road Accident Analysis Dashboard (India)")
    st.caption("Demo dashboard for analytics & policy insights")

    # Load data
    data = pd.read_csv("cleaned_accidents.csv")

    # Safety filter
    data = data[~data["state/ut/city"].str.contains("Total", case=False, na=False)]

    # Convert numeric columns
    cols = [
        "total_traffic_accidents_-_cases",
        "total_traffic_accidents_-_injured",
        "total_traffic_accidents_-_died"
    ]
    for col in cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    # Sidebar
    st.sidebar.header("Filters")
    top_n = st.sidebar.slider("Select Top N States", 5, 15, 10)

    # Top accident states
    top_states = data.sort_values(
        "total_traffic_accidents_-_cases", ascending=False
    ).head(top_n)

    st.subheader("Top States by Total Road Accidents")
    fig1, ax1 = plt.subplots()
    ax1.bar(top_states["state/ut/city"], top_states["total_traffic_accidents_-_cases"])
    ax1.set_xticklabels(top_states["state/ut/city"], rotation=45)
    ax1.set_ylabel("Number of Accidents")
    st.pyplot(fig1)

    # Death rate
    data["death_rate"] = data["total_traffic_accidents_-_died"] / data["total_traffic_accidents_-_cases"]
    top_death = data.sort_values("death_rate", ascending=False).head(top_n)

    st.subheader("Top States by Death Rate per Accident")
    fig2, ax2 = plt.subplots()
    ax2.bar(top_death["state/ut/city"], top_death["death_rate"])
    ax2.set_xticklabels(top_death["state/ut/city"], rotation=45)
    ax2.set_ylabel("Death Rate")
    st.pyplot(fig2)

    # Table
    st.subheader("📊 Data Table")
    st.dataframe(data[[
        "state/ut/city",
        "total_traffic_accidents_-_cases",
        "total_traffic_accidents_-_injured",
        "total_traffic_accidents_-_died",
        "death_rate"
    ]])

    # Logout
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()


# ---------------------------
# MAIN APP LOGIC
# ---------------------------
if st.session_state.logged_in:
    dashboard_page()
else:
    login_page()

