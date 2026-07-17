import numpy as np
from scipy.stats import norm
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# ── Black-Scholes function ───────────────────────────────────────────────────
def black_scholes(S, K, T, r, sigma):
    """
    Calculate Black-Scholes price for a European call option.
    S: current stock price
    K: strike price
    T: time to expiry in years
    r: risk-free interest rate (decimal)
    sigma: annual volatility (decimal)
    Returns: call option price
    """
    if T <= 0 or sigma <= 0:
        return max(S - K, 0)  # if expired, return intrinsic value only
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# ── Pull inputs ──────────────────────────────────────────────────────────────
ticker = yf.Ticker("AAPL")
S = ticker.info['currentPrice']

# Use a longer-dated expiry for more reliable pricing
chain = ticker.option_chain("2026-09-18")
calls = chain.calls.copy()

expiry_date = datetime(2026, 9, 18)
T = (expiry_date - datetime.today()).days / 365

treasury = yf.Ticker("^TNX")
r = treasury.info['previousClose'] / 100

hist = ticker.history(period="1y")
hist['log_return'] = np.log(hist['Close'] / hist['Close'].shift(1))
sigma = hist['log_return'].std() * np.sqrt(252)

print(f"Current price: ${S}")
print(f"T = {T:.4f} years ({(expiry_date - datetime.today()).days} days)")
print(f"r = {r:.4f}, σ = {sigma:.4f}")
print()

# ── Run Black-Scholes on every strike ───────────────────────────────────────
calls['bs_price'] = calls['strike'].apply(
    lambda K: black_scholes(S, K, T, r, sigma)
)

# Calculate difference and percentage difference
calls['difference'] = calls['lastPrice'] - calls['bs_price']
calls['pct_difference'] = (calls['difference'] / calls['bs_price']) * 100

# Filter out illiquid options (zero last price or zero volume)
liquid_calls = calls[calls['lastPrice'] > 0].copy()

# Print summary table
summary = liquid_calls[[
    'strike', 'lastPrice', 'bs_price', 
    'difference', 'pct_difference', 'inTheMoney'
]].round(2)
print(summary.to_string(index=False))

# ── Plot model vs market ─────────────────────────────────────────────────────
plt.figure(figsize=(12, 6))
plt.plot(liquid_calls['strike'], liquid_calls['lastPrice'], 
         label='Market Price', color='blue', linewidth=2)
plt.plot(liquid_calls['strike'], liquid_calls['bs_price'],  
         label='Black-Scholes Price', color='red', linewidth=2, linestyle='--')
plt.axvline(x=S, color='green', linestyle=':', linewidth=1.5, 
            label=f'Current Price ${S:.2f}')
plt.title('AAPL Call Options — Black-Scholes vs Market Price')
plt.xlabel('Strike Price ($)')
plt.ylabel('Option Price ($)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ── Plot the difference ──────────────────────────────────────────────────────
plt.figure(figsize=(12, 5))
plt.bar(liquid_calls['strike'], liquid_calls['difference'], 
        color=['red' if x < 0 else 'green' for x in liquid_calls['difference']],
        alpha=0.7, width=2)
plt.axhline(y=0, color='black', linewidth=1)
plt.axvline(x=S, color='blue', linestyle=':', linewidth=1.5,
            label=f'Current Price ${S:.2f}')
plt.title('Difference: Market Price minus Black-Scholes Price')
plt.xlabel('Strike Price ($)')
plt.ylabel('Difference ($)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ── Find the biggest divergences ─────────────────────────────────────────────
print("\n── Top 5 options where market charges most above model ──")
print(liquid_calls.nlargest(5, 'difference')[
    ['strike', 'lastPrice', 'bs_price', 'difference', 'pct_difference']
].round(2).to_string(index=False))

print("\n── Top 5 options where model is above market ──")
print(liquid_calls.nsmallest(5, 'difference')[
    ['strike', 'lastPrice', 'bs_price', 'difference', 'pct_difference']
].round(2).to_string(index=False))