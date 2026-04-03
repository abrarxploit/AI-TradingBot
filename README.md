# 🚀 Binance Futures Trading Bot (Testnet)

A simplified Python-based trading bot that interacts with the Binance Futures Testnet (USDT-M).
The bot supports MARKET and LIMIT orders, includes structured logging, input validation, and an AI-based trading signal using RSI.

---

## 📌 Features

* ✅ Place **MARKET** and **LIMIT** orders
* ✅ Supports **BUY** and **SELL** sides
* ✅ Command-line interface (CLI) using Click
* ✅ Input validation and error handling
* ✅ Structured logging (requests, responses, errors)
* ✅ Modular code design (client, orders, validators)
* 🤖 **AI Signal Integration (RSI-based trading)**

---

## 🧠 AI Signal Logic

The bot includes a basic AI-driven signal using **RSI (Relative Strength Index)**:

* RSI < 30 → **BUY**
* RSI > 70 → **SELL**
* Otherwise → **HOLD**

The bot fetches real-time market data (klines), calculates RSI, and dynamically adjusts the trade direction.

---

## 📁 Project Structure

```
trading_bot/
│
├── bot/
│   ├── client.py        # Binance client wrapper
│   ├── orders.py        # Order execution logic
│   ├── validators.py    # Input validation
│   ├── logging_config.py
│   ├── ai_signal.py     # RSI-based AI signal
│
├── logs/
│   └── bot.log
│
├── cli.py               # CLI entry point
├── requirements.txt
├── README.md
└── .env (not included)
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone <https://github.com/abrarxploit/AI-TradingBot>
cd trading_bot
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_secret_key
```

> ⚠️ Do NOT share or upload this file.

---

### 5️⃣ Binance Testnet Setup

* Register at: https://testnet.binancefuture.com
* Generate API keys under API Management
* Ensure Futures trading permissions are enabled

---

## ▶️ Usage

### ✅ MARKET Order

```
python cli.py --symbol BTCUSDT --side BUY --order_type MARKET --quantity 0.002
```

---

### ✅ LIMIT Order

```
python cli.py --symbol BTCUSDT --side SELL --order_type LIMIT --quantity 0.002 --price 65000
```

---

## 📊 Sample Output

```
🤖 AI Signal: SELL
⚡ Using AI Signal → New Side: SELL

🔹 Order Request Summary
Symbol: BTCUSDT
Side: SELL
Type: MARKET
Quantity: 0.002

✅ Order Placed Successfully!
Order ID: XXXXX
Status: NEW
```

---

## 📁 Logging
The log file captures:
- API request payloads
- API responses
- Error scenarios (invalid keys, timestamp issues, etc.)


Logs are stored in:

```
logs/bot.log
```



---

## 🛡️ Security

* API keys are stored using environment variables (`.env`)
* Sensitive data is excluded via `.gitignore`
* No credentials are hardcoded

---

## ⚠️ Notes

* This bot uses **Binance Futures Testnet** (no real money involved)
* Minimum order notional must be ≥ 100 USDT
* LIMIT orders may remain unfilled depending on market conditions

---

## 🎯 Key Highlights

* Clean and modular architecture
* Real-world API handling and error management
* AI-enhanced decision-making using technical indicators
* Ready for extension (Stop-Limit, automation, etc.)

---

## 🚀 Future Improvements

* Add Stop-Limit / OCO orders
* Implement automated trading loop
* Integrate advanced ML models
* Add web-based dashboard

---

## 👨‍💻 Author

abrarxploit

---
