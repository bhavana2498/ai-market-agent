import os
import requests
import pandas as pd
import logging
from google import genai
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Set up professional logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Load the API keys from the .env vault
load_dotenv()
FINANCE_KEY = os.getenv("FINANCE_API_KEY")
SENTIMENT_KEY = os.getenv("SENTIMENT_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Configure the AI Brain
client = genai.Client(api_key=GEMINI_KEY)
TICKER = "TSLA"

end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=10)).strftime('%Y-%m-%d')

def fetch_alphavantage_data():
    """Fetches daily stock prices from Alpha Vantage"""
    logging.info(f"Fetching stock data for {TICKER} from Alpha Vantage...")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={TICKER}&apikey={FINANCE_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if 'Time Series (Daily)' in data:
        df = pd.DataFrame(data['Time Series (Daily)']).T
        df = df.reset_index().rename(columns={'index': 'date', '4. close': 'close_price', '5. volume': 'volume'})
        df = df[['date', 'close_price', 'volume']]
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        return df
    else:
        logging.error("Alpha Vantage API error.")
        return pd.DataFrame()

def fetch_finnhub_data():
    """Fetches company news volume from Finnhub.io"""
    logging.info(f"Fetching news data for {TICKER} from Finnhub...")
    url = f"https://finnhub.io/api/v1/company-news?symbol={TICKER}&from={start_date}&to={end_date}&token={SENTIMENT_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['datetime'], unit='s').dt.strftime('%Y-%m-%d')
        daily_buzz = df.groupby('date').size().reset_index(name='news_article_count')
        return daily_buzz
    else:
        logging.error("Could not fetch sentiment data.")
        return pd.DataFrame()

def generate_ai_insights(csv_filename):
    """Passes the merged data to Gemini to generate business insights."""
    logging.info("Sending data to Gemini AI for analysis...")
    try:
        # Read the CSV we just made
        df = pd.read_csv(csv_filename)
        data_string = df.to_string(index=False)
        
        # The Senior-Level Prompt
        prompt = prompt = f"""
        You are a Senior Quantitative Investment Advisor. Your goal is to provide a "Decision Support" report for a TSLA shareholder.

        ### ANALYSIS FRAMEWORK:
        1. **Sentiment/Volume Ratio**: If news volume is >30% above the 10-day average without a 2% price increase, it indicates "Noise."
        2. **Price Action**: Analyze if price moves are "Supported" (high news volume) or "Speculative" (low news volume).

        ### DATA FOR ANALYSIS:
        {data_string}

        ### REQUIRED OUTPUT FORMAT:
        **CURRENT STANCE**: [HOLD, CAUTION, or WATCH]

        **LOGICAL JUSTIFICATION**: 
        - Explain the specific correlation found between the news volume and price volatility in the provided data.
        - State whether the current price action is "Supported" by news volume.

        **RISK THRESHOLDS**:
        - Provide one "Upside Trigger" (Price point where the user should consider taking profit).
        - Provide one "Downside Trigger" (Price point where the user should consider cutting losses).

        **DISCLAIMER**: This is an AI-generated data analysis for educational purposes only and does not constitute financial advice.
        """ 
        
        # Call the AI model
        response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
)
        
        # Save the AI's output to a text file
        with open("ai_business_report.txt", "w") as file:
            file.write(f"--- {TICKER} AI Market Analysis ---\n\n")
            file.write(response.text)
            
        logging.info("AI Analysis complete! Saved to ai_business_report.txt")
    except Exception as e:
        logging.error(f"AI Analysis failed: {e}")

def build_pipeline():
    """Extracts, Transforms, Loads, and Analyzes the data"""
    stocks_df = fetch_alphavantage_data()
    news_df = fetch_finnhub_data()
    
    if not stocks_df.empty and not news_df.empty:
        logging.info("Merging datasets by date...")
        merged_df = pd.merge(stocks_df, news_df, on='date', how='left')
        merged_df['news_article_count'] = merged_df['news_article_count'].fillna(0)
        merged_df = merged_df.sort_values(by='date')
        
        # Save the CSV
        merged_df.to_csv("ev_market_data.csv", index=False)
        logging.info("Success! Saved final dataset to ev_market_data.csv")
        
        # Execute Phase 2: Trigger the AI Brain
        generate_ai_insights("ev_market_data.csv")
    else:
        logging.error("Pipeline failed: Missing data from one or both APIs.")

if __name__ == "__main__":
    build_pipeline()