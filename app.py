import streamlit as st
from tradingview_ta import TA_Handler, Interval
import yfinance as yf
from datetime import datetime, timedelta
from newsapi import NewsApiClient

SCREENER = {
    "america": "United States",
    "forex": "Forex",
    "crypto": "Cryptocurrency",
    "indonesia": "Indonesia",
    "india": "India",
    "italy": "Italy",
    "cfd": "CFD",
    "uk": "United Kingdom",
    "brazil": "Brazil",
    "vietnam": "Vietnam",
    "rsa": "South Africa",
    "ksa": "Saudi Arabia",
    "australia": "Australia",
    "russia": "Russia",
    "thailand": "Thailand",
    "philippines": "Philippines",
    "taiwan": "Taiwan",
    "sweden": "Sweden",
    "france": "France",
    "turkey": "Turkey",
    "euronext": "Euronext",
    "germany": "Germany",
    "spain": "Spain",
    "hongkong": "Hong Kong",
    "korea": "South Korea",
    "malaysia": "Malaysia",
    "canada": "Canada",
    "crypto": "crypto",
}

def get_tradingview_analysis(symbol, exchange, screener, interval):
    try:
        stock = TA_Handler(
            symbol=symbol,
            screener=screener,
            exchange=exchange,
            interval=interval,
        )
        analysis_summary = stock.get_analysis()
        return analysis_summary
    except Exception as e:
        return {"error": str(e)}

def get_chart_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data['Close']

def get_latest_news(api_key, query, language='en', count=7):
    newsapi = NewsApiClient(api_key=api_key)
    news = newsapi.get_everything(q=query, language=language, sort_by='publishedAt', page_size=count)
    return news['articles']
def main():
    st.title("TradingView Analysis Summary")

    symbol = st.text_input("Enter Stock Symbol (e.g., TSLA):")
    exchange = st.text_input("Enter Exchange (e.g., NASDAQ):")
    screenerlist = list(SCREENER.values())
    screener = st.selectbox("Select Screener:", screenerlist)
    interval_options = [
        Interval.INTERVAL_1_MINUTE,
        Interval.INTERVAL_5_MINUTES,
        Interval.INTERVAL_15_MINUTES,
        Interval.INTERVAL_30_MINUTES,
        Interval.INTERVAL_1_HOUR,
        Interval.INTERVAL_4_HOURS,
        Interval.INTERVAL_1_DAY,
        Interval.INTERVAL_1_WEEK,
        Interval.INTERVAL_1_MONTH,
    ]
    interval = st.selectbox("Select Interval:", interval_options)

    if st.button("Get Analysis"):
        st.spinner("Fetching Analysis...")

        analysis_summary = get_tradingview_analysis(
            symbol=symbol,
            exchange=exchange,
            screener=screener,
            interval=interval,
        )

        st.success("Analysis Fetched Successfully!")

        st.title("Analysis Summary")
        st.dataframe(analysis_summary.summary)
        query = f"{symbol} stock"

        details = {
            "symbol": symbol,
            "exchange": exchange,
            "screener": screener,
            "interval": interval,
        }
        st.title("Details")
        st.dataframe(details)

        st.title("Oscillator Analysis")
        st.dataframe(analysis_summary.oscillators)

        st.title("Moving Averages")
        st.dataframe(analysis_summary.moving_averages)

        st.title("Summary")
        st.dataframe(analysis_summary.summary)

        st.title("Indicators")
        st.dataframe(analysis_summary.indicators)



       

        # Latest News
        st.title("Latest News")
        api_key = 'a697bf1b28974e6bbc0f3d4813d1cb3f'
        
        news = get_latest_news(api_key, query, count=7)

        for article in news:
            st.markdown(
                f"### [{article['title']}]({article['url']})\n"
                f" {article['description']}\n \n \n"
                f" Source: {article['source']['name']}\n \n \n"
                f" Published at: {article['publishedAt']}"
            )
            
            st.image(article['urlToImage'], caption=article['title'], use_column_width=True)

        
       

if __name__ == "__main__":
    main()
