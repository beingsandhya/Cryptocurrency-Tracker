import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from openpyxl import Workbook


st.set_page_config(page_title="Live Crypto Tracker", layout="wide", page_icon="💰")


st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stApp {
            background-color: #1e1e1e;
        }
        .css-1d391kg {
            background-color: #1e1e1e !important;
        }
        .big-font {
            font-size:20px !important;
        }
        .stDataFrame {
            border-radius: 10px;
            background-color: #1e1e1e;
        }
    </style>
""", unsafe_allow_html=True)


st.title("📈 Live Cryptocurrency Tracker")
st.write("💡 **Get real-time prices, market cap, and trends for the Top 50 Cryptocurrencies.**")


st.sidebar.header("⚙️ Settings")
sort_option = st.sidebar.selectbox("Sort by:", ["Market Cap", "24h % Change", "Price (USD)"])
search_coin = st.sidebar.text_input("🔍 Search for a coin:", "")

@st.cache_data(ttl=300)  
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("⚠️ Error fetching data!")
        return None


data = fetch_crypto_data()

if data is not None:
   
    df = data[["name", "symbol", "current_price", "market_cap", "total_volume", "price_change_percentage_24h"]]
    df.columns = ["Name", "Symbol", "Price (USD)", "Market Cap", "24h Volume", "24h % Change"]

    
    if search_coin:
        df = df[df["Name"].str.contains(search_coin, case=False, na=False)]

  
    if sort_option == "Market Cap":
        df = df.sort_values(by="Market Cap", ascending=False)
    elif sort_option == "24h % Change":
        df = df.sort_values(by="24h % Change", ascending=False)
    elif sort_option == "Price (USD)":
        df = df.sort_values(by="Price (USD)", ascending=False)

   
    df.to_excel("crypto_data.xlsx", index=False, engine="openpyxl")

    st.dataframe(df.style.format({
    "Price (USD)": "${:.2f}", 
    "Market Cap": "${:,.0f}", 
    "24h Volume": "${:,.0f}", 
    "24h % Change": "{:.2f}%"
}))

    st.dataframe(df.style.format({
    "Price (USD)": "${:.2f}", 
    "Market Cap": "${:,.0f}", 
    "24h Volume": "${:,.0f}", 
    "24h % Change": "{:.2f}%"
}))


    
    st.download_button("📥 Download Data", data=open("crypto_data.xlsx", "rb"), file_name="crypto_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

   
    fig = px.bar(df.head(10), x="Name", y="Market Cap", color="Market Cap", title="🔝 Top 10 Cryptos by Market Cap")
    st.plotly_chart(fig, use_container_width=True)

   
    fig2 = px.line(df, x="Name", y="24h % Change", title="📉 24h Price Change (%)", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

    st.success("✅ Data updated! Next update in 5 minutes.")

else:
    st.error("No data available. Please try again later.")
























































