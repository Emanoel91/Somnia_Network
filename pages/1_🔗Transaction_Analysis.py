import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime

# --- Page Config: Tab Title & Icon ---
st.set_page_config(
    page_title="Somnia Network Performance Analysis",
    page_icon="https://somnia.network/images/branding/somnia_logo_color.png",
    layout="wide"
)

# --- Title with Logo ---
st.title("🔗Transaction Analysis")

# --- Sidebar Footer Slightly Left-Aligned ---------------------------------------------------------------------------------------------------------
st.sidebar.markdown(
    """
    <style>
    .sidebar-footer {
        position: fixed;
        bottom: 20px;
        width: 250px;
        font-size: 13px;
        color: gray;
        margin-left: 5px; # -- MOVE LEFT
        text-align: left;  
    }
    .sidebar-footer img {
        width: 16px;
        height: 16px;
        vertical-align: middle;
        border-radius: 50%;
        margin-right: 5px;
    }
    .sidebar-footer a {
        color: gray;
        text-decoration: none;
    }
    </style>

    <div class="sidebar-footer">
        <div>
            <a href="https://x.com/Somnia_Network" target="_blank">
                <img src="https://somnia.network/images/branding/somnia_logo_color.png" alt="Somnia Logo">
                Powered by Somnia
            </a>
        </div>
        <div style="margin-top: 5px;">
            <a href="https://x.com/0xeman_raz" target="_blank">
                <img src="https://pbs.twimg.com/profile_images/1841479747332608000/bindDGZQ_400x400.jpg" alt="Eman Raz">
                Built by Eman Raz
            </a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================
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
agg_rate = agg_sf.groupby("Date").apply(lambda x: x.loc[x["Txn Success"]==True, "Txns"].sum()/x["Txns"].sum() if x["Txns"].sum()>0 else 0).reset_index(name="Success Rate")
fig = px.scatter(agg_rate, x="Date", y="Success Rate", size="Success Rate", title="Transaction Success Rate Over Time")
fig.update_yaxes(tickformat="%")
st.plotly_chart(fig, use_container_width=True)
