import streamlit as st
import pandas as pd
import requests
import altair as alt
from datetime import datetime

# ----------------------
# Load Data from API
# ----------------------
@st.cache_data(ttl=3600)
def load_data():
    url = "https://api.dune.com/api/v1/query/5720299/results?api_key=kmCBMTxWKBxn6CVgCXhwDvcFL1fBp6rO"
    r = requests.get(url)
    data = r.json()["result"]["rows"]
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"], utc=True)
    df = df.rename(columns={"Number of Txns": "txns"})
    return df

# ----------------------
# Aggregation Function
# ----------------------
def aggregate(df, timeframe):
    if timeframe == "day":
        df_agg = df.groupby("Date").agg({"txns": "sum"}).reset_index()
    elif timeframe == "week":
        df_agg = df.resample("W-Mon", on="Date").agg({"txns": "sum"}).reset_index().sort_values("Date")
    elif timeframe == "month":
        df_agg = df.resample("M", on="Date").agg({"txns": "sum"}).reset_index().sort_values("Date")
    else:
        df_agg = df.copy()
    
    df_agg["cumulative_txns"] = df_agg["txns"].cumsum()
    df_agg["tps"] = df_agg["txns"] / (24*60*60)  # تراکنش در ثانیه
    return df_agg

# ----------------------
# KPI Calculations
# ----------------------
def compute_kpis(df_day):
    total_txns = df_day["txns"].sum()
    avg_daily = df_day["txns"].mean()
    median_daily = df_day["txns"].median()
    max_daily = df_day["txns"].max()
    days_range = (df_day["Date"].max() - df_day["Date"].min()).days
    tps = total_txns / (days_range * 24 * 60 * 60) if days_range > 0 else 0
    
    # تغییرات روزانه به درصد
    df_day = df_day.sort_values("Date")
    df_day["pct_change"] = df_day["txns"].pct_change()
    avg_change_pct = df_day["pct_change"].mean() * 100
    
    return total_txns, avg_change_pct, tps, avg_daily, median_daily, max_daily

# ----------------------
# Streamlit UI
# ----------------------

df = load_data()

st.title("📊 Somnia Network Transactions Dashboard")

# Main page filters
st.subheader("Filters")
min_date, max_date = df["Date"].min().date(), df["Date"].max().date()
col_f1, col_f2, col_f3 = st.columns([1,1,1])
with col_f1:
    start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
with col_f2:
    end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)
with col_f3:
    timeframe = st.selectbox("Time Frame", ["day", "week", "month"], index=0)

# Convert inputs to tz-aware timestamps
start_ts = pd.to_datetime(start_date).tz_localize('UTC')
end_ts = pd.to_datetime(end_date).tz_localize('UTC') + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)

# Filter Data
mask = (df["Date"] >= start_ts) & (df["Date"] <= end_ts)
df_filtered = df.loc[mask]

# Aggregations
df_day = aggregate(df_filtered, "day")
df_tf = aggregate(df_filtered, timeframe)

# KPIs
total_txns, avg_change_pct, tps, avg_daily, median_daily, max_daily = compute_kpis(df_day)

# First Row KPIs
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Number of Transactions", f"{total_txns:,}")
col2.metric("Average Daily Transactions Change%", f"{avg_change_pct:.2f}%")
col3.metric("Transaction per Second (TPS)", f"{tps:.4f}")

# Second Row KPIs
col4, col5, col6 = st.columns(3)
col4.metric("Average Daily Transactions Count", f"{avg_daily:.2f}")
col5.metric("Median Daily Transactions Count", f"{median_daily:.2f}")
col6.metric("Max Daily Transactions", f"{max_daily:,}")

# Third Row Charts
col7, col8 = st.columns(2)

# Bar-Line Chart with adjusted bar width
bar = alt.Chart(df_tf).mark_bar(color="#4C78A8", size=20).encode(
    x=alt.X("Date:T", title="Date"),
    y=alt.Y("txns:Q", title="Transactions"),
)

line = alt.Chart(df_tf).mark_line(color="red", point=True).encode(
    x="Date:T",
    y=alt.Y("cumulative_txns:Q", title="Cumulative Transactions", axis=alt.Axis(titleColor="red"))
)

chart_bar_line = alt.layer(bar, line).resolve_scale(y="independent").properties(
    title="Number of Transactions Over Time",
    width=400,
    height=300
)

col7.altair_chart(chart_bar_line, use_container_width=True)

# TPS Line Chart
chart_tps = alt.Chart(df_tf).mark_line(color="#72B7B2", point=false).encode(
    x="Date:T",
    y=alt.Y("tps:Q", title="TPS")
).properties(
    title="Transaction per Second (TPS) Over Time",
    width=400,
    height=300
)

col8.altair_chart(chart_tps, use_container_width=True)
