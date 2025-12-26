import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Financial Analyst Copilot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- DARK THEME + CARDS --------------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: #FAFAFA;
}
.stApp {
    background-color: #0E1117;
}
.card {
    background-color: #161B22;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    text-align: center;
}
.card h4 {
    margin-bottom: 6px;
    color: #9BA3AF;
}
.card h2 {
    margin: 0;
    color: #FFFFFF;
}
hr {
    border: 1px solid #2A2F3A;
}
</style>
""", unsafe_allow_html=True)

# -------------------- MOCK DATA (Replace with your backend later) --------------------
def fetch_price_data(etf):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=120)
    prices = np.cumsum(np.random.normal(0.1, 1.2, 120)) + (140 if etf == "IWP" else 135)
    return pd.DataFrame({"Date": dates, "Close": prices})

def compute_kpis(df):
    last_price = df["Close"].iloc[-1]
    ret_1m = (df["Close"].iloc[-1] / df["Close"].iloc[-22] - 1) * 100
    volatility = df["Close"].pct_change().std() * np.sqrt(252)
    return last_price, ret_1m, volatility

def volatility_label(v):
    if v < 0.15:
        return "LOW"
    elif v < 0.25:
        return "MEDIUM"
    return "HIGH"

def sentiment_label(score):
    if score > 0.1:
        return "Bullish 🟢"
    elif score < -0.1:
        return "Bearish 🔴"
    return "Neutral 🟡"

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("## 📊 ETF Controls")
    etf_a = st.selectbox("ETF A", ["IWP", "IWS"])
    etf_b = st.selectbox("ETF B", ["IWS", "IWP"])
    run = st.button("Compare ETFs")

# -------------------- MAIN TITLE --------------------
st.markdown("## 🤖 AI Financial Analyst Copilot")
st.markdown("Professional ETF comparison dashboard")

# -------------------- RUN DASHBOARD --------------------
if run:
    data_a = fetch_price_data(etf_a)
    data_b = fetch_price_data(etf_b)

    price_a, ret_a, vol_a = compute_kpis(data_a)
    price_b, ret_b, vol_b = compute_kpis(data_b)

    sentiment_a = -0.33
    sentiment_b = -0.33

    # -------------------- KPI SNAPSHOT --------------------
    st.markdown("### 📌 ETF Snapshot")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="card">
            <h4>{etf_a} Price</h4>
            <h2>${price_a:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="card">
            <h4>1M Return</h4>
            <h2>{ret_a:.2f}%</h2>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="card">
            <h4>Volatility</h4>
            <h2>{volatility_label(vol_a)}</h2>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="card">
            <h4>Sentiment</h4>
            <h2>{sentiment_label(sentiment_a)}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # -------------------- RISK VS RETURN --------------------
    st.markdown("### 📐 Risk vs Return Analysis")

    rr_df = pd.DataFrame({
        "ETF": [etf_a, etf_b],
        "Return (%)": [ret_a, ret_b],
        "Volatility": [vol_a, vol_b],
        "Sentiment Strength": [abs(sentiment_a), abs(sentiment_b)]
    })

    rr_fig = px.scatter(
        rr_df,
        x="Volatility",
        y="Return (%)",
        size="Sentiment Strength",
        color="ETF",
        size_max=60,
        template="plotly_dark",
        title="Higher Return & Lower Risk is Better"
    )

    st.plotly_chart(rr_fig, use_container_width=True)

    # -------------------- TABS (NO SCROLL) --------------------
    tab1, tab2, tab3 = st.tabs(["📈 Price Charts", "📰 Sentiment", "🤖 AI Explanation"])

    with tab1:
        c1, c2 = st.columns(2)

        with c1:
            fig_a = px.line(
                data_a,
                x="Date",
                y="Close",
                title=f"{etf_a} Close Price",
                template="plotly_dark"
            )
            fig_a.update_layout(height=350)
            st.plotly_chart(fig_a, use_container_width=True)

        with c2:
            fig_b = px.line(
                data_b,
                x="Date",
                y="Close",
                title=f"{etf_b} Close Price",
                template="plotly_dark"
            )
            fig_b.update_layout(height=350)
            st.plotly_chart(fig_b, use_container_width=True)

    with tab2:
        st.metric(f"{etf_a} Sentiment Score", sentiment_a)
        st.metric(f"{etf_b} Sentiment Score", sentiment_b)

    with tab3:
        st.info(
            f"""
            **Summary Insight**
            
            • {etf_b} shows higher 1-month return  
            • {etf_a} has lower volatility  
            • Both ETFs currently show bearish sentiment  

            **Interpretation:**  
            Risk-adjusted investors may prefer **{etf_b}**, while conservative investors may lean toward **{etf_a}**.
            """
        )


