import yfinance as yf

def fetch_price_data(ticker, period="6mo"):
    data = yf.download(ticker, period=period)

    # FIX: flatten MultiIndex columns
    if isinstance(data.columns, tuple) or hasattr(data.columns, "levels"):
        data.columns = data.columns.get_level_values(0)

    data["Return"] = data["Close"].pct_change()
    return data.reset_index()
