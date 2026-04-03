# 🚀 Binance Futures Testnet Trading Bot

A clean, modular Python trading bot for Binance USDT-M Futures **Testnet**.
Supports MARKET, LIMIT, and STOP_MARKET orders with RSI-based AI signals,
structured logging, and full input validation.

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
├── bot/
│   ├── __init__.py
│   ├── ai_signal.py       # RSI-based BUY/SELL/HOLD signal
│   ├── client.py          # Binance client wrapper
│   ├── logging_config.py  # Rotating file + console logging
│   ├── orders.py          # Order logic + OrderResult dataclass
│   └── validators.py      # Input validation
├── logs/
│   └── bot.log            # Auto-created on first run
├── cli.py                 # CLI entry point (Click)
├── .env                   # API credentials (never commit)
├── .gitignore
├── requirements.txt
└── README.md
```
<img width="230" height="364" alt="Screenshot 2026-04-03 122120" src="https://github.com/user-attachments/assets/4ae3ab86-a52c-462a-8714-7b5db23970cf" />

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone <https://github.com/abrarxploit/AI-TradingBot>
cd trading_bot
```

---

### 2️⃣Create virtual environment
```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

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
<img width="1756" height="631" alt="Screenshot 2026-04-03 133803" src="https://github.com/user-attachments/assets/2034ce43-7bb0-437c-aad2-1aaa9993c4fc" />


---

### ✅ LIMIT Order

```
python cli.py --symbol BTCUSDT --side SELL --order_type LIMIT --quantity 0.002 --price 65000
```
<img width="1471" height="552" alt="Screenshot 2026-04-03 133848" src="https://github.com/user-attachments/assets/09df05a0-652f-4367-9735-d1945ebd1a66" />

---

### AI SIGNAL Usage


```
🤖 AI Signal: HOLD
⚡ Using AI Signal → New Side: HOLD

🔹 Order Request Summary
Symbol: BTCUSDT
Side: HOLD
Type: MARKET
Quantity: 0.002

✅ Order Placed Successfully!
Order ID: XXXXX
Status: NEW
```
<img width="1864" height="131" alt="Screenshot 2026-04-03 134035" src="https://github.com/user-attachments/assets/ee1070e8-449e-4692-a3d9-c7fe2a1b890f" />


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
