import streamlit as st

# --- Page Config: Tab Title & Icon ---
st.set_page_config(
    page_title="Somnia Network Performance Analysis",
    page_icon="https://somnia.network/images/branding/somnia_logo_color.png",
    layout="wide"
)

# --- Title with Logo ---
st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 15px;">
        <img src="https://somnia.network/images/branding/somnia_logo_color.png" alt="Somnia" style="width:60px; height:60px;">
        <h1 style="margin: 0;">Somnia Network Performance Analysis</h1>
    </div>
    """,
    unsafe_allow_html=True
)

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

# --- Reference and Rebuild Info ---
st.markdown(
    """
    <div style="margin-top: 20px; margin-bottom: 20px; font-size: 16px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://pbs.twimg.com/profile_images/1841479747332608000/bindDGZQ_400x400.jpg" alt="Eman Raz" style="width:25px; height:25px; border-radius: 50%;">
            <span>Built by: <a href="https://x.com/0xeman_raz" target="_blank">Eman Raz</a></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Info Box ---
st.markdown(
    """
    <div style="background-color: #b3ffc8; padding: 15px; border-radius: 10px; border: 1px solid #000000;">
        <p>
        <strong>Somnia</strong> is a fast and powerful blockchain built to process a very high volume of transactions, even under heavy load. 
        Unlike many blockchains that rely on parallel execution across multiple cores, 
        <strong>Somnia</strong> focuses on making a single core run extremely fast. 
        This makes it especially effective for scenarios with highly related transactions, such as <strong>large NFT drops</strong> 
        or <strong>busy decentralized exchange (DEX) trading</strong>.
        </p>
        <h4><strong>Key Features of Somnia:</strong></h4>
        <ul>
            <li><strong>Ethereum Compatibility:</strong> Runs Ethereum smart contracts, making it fully compatible with Ethereum tools and applications.</li>
            <li><strong>Super-Fast Compiler:</strong> Translates Ethereum code into ultra-efficient instructions, enabling millions of token transfers per second with sub-second execution.</li>
            <li><strong>Smart CPU Utilization:</strong> Optimizes single-core multitasking—for example, overlapping steps in token swaps to cut processing time in half.</li>
            <li><strong>High-Load Resilience:</strong> Maintains speed and smooth performance during network spikes, such as major NFT sales.</li>
            <li><strong>Resource Efficiency:</strong> Uses its fast compiler only for frequently executed contracts, while defaulting to a lighter method for less common ones.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Links with Logos ---
st.markdown(
    """
    <div style="font-size: 16px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://somnia.network/images/branding/somnia_logo_color.png" alt="Somnia" style="width:20px; height:20px;">
            <a href="https://somnia.network/" target="_blank">Somnia Network Website</a>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://somnia.network/images/branding/somnia_logo_color.png" alt="X" style="width:20px; height:20px;">
            <a href="https://x.com/Somnia_Network" target="_blank">Somnia Network X Account</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
