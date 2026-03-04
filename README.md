# 📈 AI Market Agent: Automated ETL & Sentiment Pipeline

## Project Overview
This project is a fully automated, cloud-based data pipeline that extracts live financial and sentiment data, transforms it into actionable insights, and leverages Generative AI to produce daily business intelligence reports. 

## 🛠️ Architecture & Technologies Used
* **Data Extraction:** RESTful APIs (Alpha Vantage for stock prices, Finnhub for news sentiment volume).
* **Data Transformation:** Python & Pandas for cleaning, time-series alignment, and merging complex JSON structures into CSVs.
* **Artificial Intelligence:** Google GenAI (Gemini 2.5 Flash) for automated financial reasoning and insight generation.
* **Cloud Automation:** GitHub Actions (CI/CD) to execute the pipeline automatically every weekday via cron jobs.
* **Security:** Environment variables (`.env`) and GitHub Encrypted Secrets for secure API key management.

## ⚙️ How It Works
1. **Extract:** The script pulls the last 10 days of TSLA market data and financial news volume.
2. **Transform:** It merges the financial metrics and sentiment buzz by date, handling missing values and formatting.
3. **Analyze:** The merged dataset is passed to Gemini, which acts as an AI Financial Analyst to find correlations between news spikes and price action.
4. **Automate:** GitHub Actions runs this entire process securely in the cloud without human intervention.