# 📈 AI Quant Agent: Automated Investment Decision Support System

## 🚀 Project Overview
This is a production-grade, cloud-native data pipeline that automates the role of a Quantitative Financial Analyst. The system extracts live market data and news volume for Tesla (TSLA), merges them into a unified time-series dataset, and leverages a Generative AI "Reasoning Engine" to provide daily investment stances (HOLD/CAUTION).

Unlike standard sentiment trackers, this agent uses a **Decision Matrix** to distinguish between market "Noise" and "Supported" price action, delivering actionable risk thresholds entirely in the cloud.

## 🧠 The Decision Framework (Logic)
The AI is programmed with a custom quantitative framework:
* **Volume/Sentiment Ratio:** If news volume spikes >30% above the 8-day average without a corresponding 2% price move, the system flags the activity as "Speculative Noise."
* **Supported Growth:** If price action exceeds 2% on high news volume, the system validates the move as "Fundamental Support."
* **Risk Triggers:** Automates the calculation of Upside (Profit taking) and Downside (Loss cutting) price targets based on current volatility.

## 🛠️ Tech Stack & Architecture
* **Language:** Python 3.x
* **Data Orchestration:** Pandas (Time-series alignment & JSON transformation)
* **AI Engine:** Google Gemini (via Generative AI SDK)
* **Data Sources:** Alpha Vantage (Market Data) & Finnhub (Sentiment News Volume)
* **Cloud Infrastructure:** GitHub Actions (CI/CD) for automated daily execution
* **Security:** GitHub Encrypted Secrets & Python-Dotenv for API key rotation

## ⚙️ How It Works
1.  **Extract:** A Python script fetches the last 10 days of TSLA closing prices and daily news article counts.
2.  **Transform:** Data is cleaned and merged into a structured DataFrame, removing indices to optimize AI token consumption.
3.  **Analyze:** The data is processed through the "Quantitative Advisor" persona, which applies the decision matrix to generate a structured report.
4.  **Automate:** A YAML workflow wakes up a GitHub virtual machine every morning to run the analysis and save the output as a downloadable artifact.

## 📄 Sample AI Output
> **CURRENT STANCE:** HOLD  
> **LOGICAL JUSTIFICATION:** Price increased 3.44% on 2x news volume. Move is "Supported" by market interest, not just speculative buzz.  
> **UPSIDE TRIGGER:** $420.00 | **DOWNSIDE TRIGGER:** $390.00

---
*Disclaimer: This project is for educational purposes only. It is not financial advice.*