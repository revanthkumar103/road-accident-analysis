import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Road Accident Analysis", layout="wide")

st.title("🚦 Road Accident Analysis Dashboard (India)")

# Load data
data = pd.read_csv("cleaned_accidents.csv")

# Remove total rows (safety)
data = data[~data["state/ut/city"].str.contains("Total", case=False, na=False)]

# Convert numeric columns
cols = [
    "total_traffic_accidents_-_cases",
    "total_traffic_accidents_-_injured",
    "total_traffic_accidents_-_died"
]

for col in cols:
    data[col] = pd.to_numeric(data[col], errors="coerce")

# Sidebar selection
st.sidebar.header("Filters")
top_n = st.sidebar.slider("Select Top N States", 5, 15, 10)

# Top states by accidents
top_states = data.sort_values(
    "total_traffic_accidents_-_cases", ascending=False
).head(top_n)

st.subheader("Top States by Total Road Accidents")

fig1, ax1 = plt.subplots()
ax1.bar(top_states["state/ut/city"], top_states["total_traffic_accidents_-_cases"])
ax1.set_xticklabels(top_states["state/ut/city"], rotation=45)
ax1.set_ylabel("Number of Accidents")
st.pyplot(fig1)

# Death rate calculation
data["death_rate"] = data["total_traffic_accidents_-_died"] / data["total_traffic_accidents_-_cases"]

top_death = data.sort_values("death_rate", ascending=False).head(top_n)

st.subheader("Top States by Death Rate per Accident")

fig2, ax2 = plt.subplots()
ax2.bar(top_death["state/ut/city"], top_death["death_rate"])
ax2.set_xticklabels(top_death["state/ut/city"], rotation=45)
ax2.set_ylabel("Death Rate")
st.pyplot(fig2)

# Data table
st.subheader("📊 Data Table")
st.dataframe(data[[
    "state/ut/city",
    "total_traffic_accidents_-_cases",
    "total_traffic_accidents_-_injured",
    "total_traffic_accidents_-_died",
    "death_rate"
]])
