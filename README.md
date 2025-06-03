# QuantView

QuantView is a modular Python-based toolkit for fetching, enriching, and visualizing financial market data using technical indicators.

## Features

- 📈 Fetch historical price data from Yahoo Finance  
- 🧮 Enrich data with indicators like:
  - Simple & Exponential Moving Averages (SMA/EMA)
  - Relative Strength Index (RSI)
  - Moving Average Convergence Divergence (MACD)
  - Average True Range (ATR)
  - Volatility (Rolling Std Dev)
- 📊 Plot individual indicators or a combined dashboard
- 🖥️ CLI interface for quick symbol analysis

## Requirements

- Python 3.9+
- `pandas`
- `matplotlib`
- `yfinance`

## Usage

### CLI

```bash
python main.py --symbol AAPL --fetch --indicators sma rsi macd --save
