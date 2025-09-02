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
        Somnia is a fast and powerful blockchain designed to handle lots of transactions quickly, even when things get really busy. 
        Unlike other blockchains that try to split work across multiple computer cores (parallel execution), Somnia focuses on making 
        a single core work super fast. This makes it great for situations where many transactions are related, like during big NFT sales 
        or busy trading on decentralized exchanges (DEXs).

        Key features of Somnia:
        Works with Ethereum: Somnia can run Ethereum smart contracts, so it’s compatible with tools and apps built for Ethereum.
        Super-Fast Compiler: Somnia has a special tool that converts Ethereum code into instructions a computer can run much faster. 
        For example, it can process millions of token transfers per second, each taking just a fraction of a second.
        Smart Use of CPU Power: Somnia uses the computer’s ability to do multiple tasks at once within a single core. For example, when 
        swapping tokens, it can do some steps at the same time, cutting the time it takes in half.
        Handles Busy Moments: When lots of transactions are trying to update the same thing (like during a big NFT drop), Somnia keeps things 
        fast and smooth, unlike other blockchains that slow down.
        Saves Resources: Somnia only uses its fast compiler for contracts that get used a lot, and switches to a slower but cheaper method for less common ones.
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
