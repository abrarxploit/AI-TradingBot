# Binance Futures Testnet Trading Bot

A clean, modular Python trading bot for Binance USDT-M Futures **Testnet**.
Supports MARKET, LIMIT, and STOP_MARKET orders with RSI-based AI signals,
structured logging, and full input validation.

---

## Features

* ✅ Place **MARKET** and **LIMIT** orders
* ✅ Supports **BUY** and **SELL** sides
* ✅ Command-line interface (CLI) using Click
* ✅ Input validation and error handling
* ✅ Structured logging (requests, responses, errors)
* ✅ Modular code design (client, orders, validators)
* 🤖 **AI Signal Integration (RSI-based trading)**

---

## AI Signal Logic

RSI (Relative Strength Index) is calculated from the last 100 candles:

| RSI Value | Signal |
|-----------|--------|
| Below 30  | BUY (oversold) |
| Above 70  | SELL (overbought) |
| 30 – 70   | HOLD (no trade) |

Use `--use-ai` flag to activate. If the AI signal differs from your `--side`,
the bot will ask for confirmation before overriding.


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

##  Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/abrarxploit/AI-TradingBot
cd AI-TradingBot
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

## Usage

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

### ✅ AI SIGNAL Usage (RSI)


```
python cli.py place --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.002 --use-ai

```
<img width="1864" height="131" alt="Screenshot 2026-04-03 134035" src="https://github.com/user-attachments/assets/ee1070e8-449e-4692-a3d9-c7fe2a1b890f" />

---
### Help
```bash
python cli.py --help
python cli.py place --help
```
---
## 📁 Logging

Logs are saved to `logs/bot.log` automatically.
- File captures **DEBUG and above** (full request/response detail)
- Console shows **WARNING and above** (clean output)
- Rotating: 5 MB max, 3 backups kept

View logs:
```bash
cat logs/bot.log
```


---

## 🛡️ Security

- Credentials stored in `.env` only — never hardcoded
- `.env` excluded via `.gitignore`.
- Testnet only. No real funds involved.

---
## Notes

* This bot uses **Binance Futures Testnet** (no real money involved).
* Minimum order notional must be ≥ 100 USDT.
* LIMIT orders may remain unfilled, depending on market conditions.

---

## Key Highlights

* Clean and modular architecture.
* Real-world API handling and error management.
* AI-enhanced decision-making using technical indicators.

---

##  Future Improvements

- Automated trading loop with configurable interval.
- Additional indicators (MACD, Bollinger Bands).
- Web dashboard for order monitoring.
- Stop-Limit / OCO order support.
- Backtesting module.
---

## Author

abrarxploit

---
