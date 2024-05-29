# filename: fetch_stock_news.py

import yfinance as yf
import pandas as pd

# list of tickers
tickers = ["NVDA", "TSLA"]

# collect news data for each ticker
news_data = []
for ticker in tickers:
    ticker_obj = yf.Ticker(ticker)
    news = ticker_obj.get_news()
    for item in news:
        item['ticker'] = ticker
    news_data.extend(news)

df = pd.DataFrame(news_data)

# Print recent 5 news for each ticker
for ticker in tickers:
    print(f"Recent news for {ticker}:")
    print(df[df['ticker'] == ticker].head(5))
    print('\n\n')