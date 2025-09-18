# 100 Backtesting Trading Strategic Bot

This project automates the process of backtesting trading strategies by simulating 100 test trades per signal using webhook alerts from TradingView. It is designed to help traders validate the effectiveness of strategies like BOS (Break of Structure), FBO (False Breakout), RSI divergence, and more.

> 🔁 Run 100 backtests in seconds. Automate, validate, and optimize your strategy before going live.

---

## 📌 Features

- 🔗 **Webhook Integration** with TradingView
- ⚙️ **Automated 100 backtest runs** per alert
- 📊 **Google Sheets logging** or Excel support
- 🧠 Strategy Logic:
  - M2 (BOS + Liquidity Grab)
  - FBO (False Breakout + RSI divergence)
  - S1 (Momentum & RSI + ATR SL/TP)
- 💡 Custom SL/TP calculations based on ATR and volatility
- 🕒 Timestamps auto-generated for realistic simulation
- 🌐 Easy deployment using Flask + Ngrok or cloud server

---

## 🛠️ Tech Stack

- **Python** (Flask)
- **Google Sheets API** / Excel
- **Ngrok / LocalTunnel**
- **TradingView Webhooks**
- Optional: **Backtrader** for advanced backtesting engine

---

## 🚀 How It Works

1. Set your strategy rules in `app.py`.
2. Send alerts from TradingView → Webhook triggers the bot.
3. The bot runs 100 simulated backtests using randomized or structured mock data.
4. Logs results (entry, SL, TP, returns, win/loss) to Google Sheets or CSV.
5. Review win rate and optimize your strategy.

---

## 📂 Project Structure

📁 100-backtesting-trading-strategic-bot/
│
├── app.py # Flask server to handle webhooks
├── strategy.py # Strategy logic and validation
├── mock_generator.py # Generates fake 100-entry dataset per alert
├── logger.py # Logs to Google Sheets or Excel
├── config.py # API keys, strategy params
├── requirements.txt # Python dependencies
└── README.md # Project overview
---

## 🧪 Example Use Case

- You design an FBO strategy with RSI divergence and BB re-entry.
- You configure your rules in `strategy.py`.
- On every alert from TradingView, the bot:
  - Validates the entry
  - Simulates 100 trades with variations
  - Calculates returns
  - Sends data to your Google Sheet
