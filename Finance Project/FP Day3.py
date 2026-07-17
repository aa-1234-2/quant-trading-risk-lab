import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ── S: Current stock price ───────────────────────────────────────────────────
ticker = yf.Ticker("AAPL")
S = ticker.info['currentPrice']
print(f"S (stock price):        ${S}")

# ── K: Strike price ──────────────────────────────────────────────────────────
# Pick an at-the-money strike (closest to current price)
chain = ticker.option_chain("2026-07-17")
calls = chain.calls.copy()

# Find the strike closest to current price
calls['distance'] = abs(calls['strike'] - S)
atm_option = calls.loc[calls['distance'].idxmin()]
K = atm_option['strike']
print(f"K (strike price):       ${K}")
print(f"Market price of option: ${atm_option['lastPrice']}")

# ── T: Time to expiry in years ───────────────────────────────────────────────
expiry_date = datetime(2026, 7, 17)
today = datetime.today()
T = (expiry_date - today).days / 365
print(f"T (time to expiry):     {T:.4f} years ({(expiry_date - today).days} days)")

# ── r: Risk-free interest rate ───────────────────────────────────────────────
# Pull 10-year US Treasury yield (^TNX gives yield as a percentage)
treasury = yf.Ticker("^TNX")
r = treasury.info['previousClose'] / 100   # convert from % to decimal
print(f"r (risk-free rate):     {r:.4f} ({r*100:.2f}%)")

# ── σ: Historical volatility ─────────────────────────────────────────────────
# Pull 1 year of daily prices
hist = ticker.history(period="1y")

# Calculate daily log returns
hist['log_return'] = np.log(hist['Close'] / hist['Close'].shift(1))

# Annualise the standard deviation (multiply by sqrt of 252 trading days)
sigma = hist['log_return'].std() * np.sqrt(252)
print(f"σ (historical vol):     {sigma:.4f} ({sigma*100:.2f}%)")

# ── Summary ──────────────────────────────────────────────────────────────────
print("\n── Black-Scholes Inputs ──")
print(f"  S = ${S}       (stock price)")
print(f"  K = ${K}       (strike price)")
print(f"  T = {T:.4f}    (years to expiry)")
print(f"  r = {r:.4f}    (risk-free rate)")
print(f"  σ = {sigma:.4f}    (historical volatility)")