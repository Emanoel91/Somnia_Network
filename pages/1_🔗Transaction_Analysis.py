import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# --- Page Config: Tab Title & Icon ---
st.set_page_config(
    page_title="Somnia Network Performance Analysis",
    page_icon="https://somnia.network/images/branding/somnia_logo_color.png",
    layout="wide"
)

# ============================
# API URLs
# ============================
API_TXNS = "https://api.dune.com/api/v1/query/5720299/results?api_key=kmCBMTxWKBxn6CVgCXhwDvcFL1fBp6rO"
API_TXNS_SUCCESS = "https://api.dune.com/api/v1/query/5720665/results?api_key=kmCBMTxWKBxn6CVgCXhwDvcFL1fBp6rO"

# ============================
# Load data from API
# ============================
@st.cache_data(ttl=3600)
def load_data(url):
    r = requests.get(url)
    data = r.json()["result"]["rows"]
    return pd.DataFrame(data)

# Transactions data
transactions = load_data(API_TXNS)
transactions["Date"] = pd.to_datetime(transactions["Date"])  # Already tz-aware from API
transactions = transactions.rename(columns={"Number of Txns": "Txns"})

# Success/Fail data
transactions_sf = load_data(API_TXNS_SUCCESS)
transactions_sf["Date"] = pd.to_datetime(transactions_sf["Date"])  # Already tz-aware from API
transactions_sf = transactions_sf.rename(columns={"Number of Txns": "Txns"})

# ============================
# Filters
# ============================
st.title("Somnia Network Transactions Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    start_date = st.date_input("Start Date", transactions["Date"].min().date())
with col2:
    end_date = st.date_input("End Date", transactions["Date"].max().date())
with col3:
    time_frame = st.selectbox("Time Frame", ["day", "week", "month"])

# Convert filter dates to UTC-aware
start_ts = pd.to_datetime(start_date).tz_localize('UTC')
end_ts = pd.to_datetime(end_date).tz_localize('UTC') + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)

mask = (transactions["Date"] >= start_ts) & (transactions["Date"] <= end_ts)
transactions = transactions.loc[mask]

mask_sf = (transactions_sf["Date"] >= start_ts) & (transactions_sf["Date"] <= end_ts)
transactions_sf = transactions_sf.loc[mask_sf]

# ============================
# Resample data by timeframe
# ============================
def resample_data(df, time_frame, value_col="Txns", group_col=None):
    if time_frame == "day":
        rule = "D"
    elif time_frame == "week":
        rule = "W"
    else:
        rule = "M"

    if group_col:
        df = df.set_index("Date").groupby(group_col)[value_col].resample(rule).sum().reset_index()
    else:
        df = df.set_index("Date").resample(rule)[value_col].sum().reset_index()
    return df

# ============================
# Charts & KPIs - API 1
# ============================
agg = resample_data(transactions, time_frame)
agg["Cumulative"] = agg["Txns"].cumsum()
agg["TPS"] = agg["Txns"] / (24*60*60)

# KPIs row 1
col1, col2, col3 = st.columns(3)
col1.metric("Total Number of Transactions", f"{transactions['Txns'].sum():,}")
daily_diff = transactions.set_index("Date")["Txns"].diff().mean()
col2.metric("Average Daily Transactions Change%", f"{daily_diff:.2f}")
col3.metric("Transaction per Second (TPS)", f"{transactions['Txns'].sum()/(len(transactions)*24*60*60):.4f}")

# KPIs row 2
col1, col2, col3 = st.columns(3)
col1.metric("Average Daily Transactions Count", f"{transactions['Txns'].mean():.2f}")
col2.metric("Median Daily Transactions Count", f"{transactions['Txns'].median():.2f}")
col3.metric("Max Daily Transactions", f"{transactions['Txns'].max():,}")

# Charts row 3
col1, col2 = st.columns(2)
with col1:
    fig = go.Figure()
    fig.add_bar(x=agg["Date"], y=agg["Txns"], name="Transactions", marker_color="#636EFA")
    fig.add_trace(go.Scatter(x=agg["Date"], y=agg["Cumulative"], name="Cumulative Txns", yaxis="y2", mode="lines", line=dict(color="red")))
    fig.update_layout(title="Number of Transactions Over Time",
                      yaxis=dict(title="Transactions"),
                      yaxis2=dict(title="Cumulative", overlaying="y", side="right"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.line(agg, x="Date", y="TPS", title="Transaction per Second (TPS) Over Time")
    st.plotly_chart(fig, use_container_width=True)

# ============================
# Charts & KPIs - API 2 (Txn Success)
# ============================
agg_sf = resample_data(transactions_sf, time_frame, value_col="Txns", group_col="Txn Success")

# Row: stacked bar charts
col1, col2 = st.columns(2)
with col1:
    fig = px.bar(agg_sf, x="Date", y="Txns", color="Txn Success", title="Number of Transactions by Success Over Time", barmode="stack")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(agg_sf, x="Date", y="Txns", color="Txn Success", title="Normalized Transactions by Success Over Time", barmode="relative")
    fig.update_layout(yaxis=dict(tickformat="%"))
    st.plotly_chart(fig, use_container_width=True)

# Row: KPIs for success/fail
agg_daily = resample_data(transactions_sf, "day", value_col="Txns", group_col="Txn Success")
mean_success = agg_daily[agg_daily["Txn Success"]==True]["Txns"].mean()
mean_fail = agg_daily[agg_daily["Txn Success"]==False]["Txns"].mean()
total_success = transactions_sf[transactions_sf["Txn Success"]==True]["Txns"].sum()
total_all = transactions_sf["Txns"].sum()
success_rate = total_success / total_all * 100 if total_all > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Average Daily Succeeded Transactions Count", f"{mean_success:.2f}")
col2.metric("Average Daily Failed Transactions Count", f"{mean_fail:.2f}")
col3.metric("Success Rate%", f"{success_rate:.2f}%")

# Row: pie chart + bubble chart
col1, col2 = st.columns(2)
with col1:
    fig = px.pie(transactions_sf, values="Txns", names="Txn Success", title="Total Number of Transactions by Success")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    agg_rate = agg_sf.groupby("Date").apply(
    lambda x: x.loc[x["Txn Success"]==True, "Txns"].sum()/x["Txns"].sum() 
    if x["Txns"].sum()>0 else 0
).reset_index(name="Success Rate")

# تغییر به نمودار خطی
fig = px.line(
    agg_rate, 
    x="Date", 
    y="Success Rate", 
    title="Transaction Success Rate Over Time",
    markers=True  # اگر میخوای نقاط هم روی خط نمایش داده بشه
)

fig.update_yaxes(tickformat="%")
st.plotly_chart(fig, use_container_width=True)
