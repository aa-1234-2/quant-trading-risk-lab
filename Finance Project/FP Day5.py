import numpy as np
from scipy.stats import norm
import yfinance as yf
from datetime import datetime

# ── Pull your five inputs ────────────────────────────────────────────────────
ticker = yf.Ticker("AAPL")

S = ticker.info['currentPrice']

chain = ticker.option_chain("2026-07-17")
calls = chain.calls.copy()
calls['distance'] = abs(calls['strike'] - S)
atm_option = calls.loc[calls['distance'].idxmin()]
K = atm_option['strike']

expiry_date = datetime(2026, 7, 17)
T = (expiry_date - datetime.today()).days / 365

treasury = yf.Ticker("^TNX")
r = treasury.info['previousClose'] / 100

hist = ticker.history(period="1y")
hist['log_return'] = np.log(hist['Close'] / hist['Close'].shift(1))
sigma = hist['log_return'].std() * np.sqrt(252)

print(f"S = ${S}")
print(f"K = ${K}")
print(f"T = {T:.4f} years")
print(f"r = {r:.4f}")
print(f"σ = {sigma:.4f}")
print()

# ── The Black-Scholes formula ────────────────────────────────────────────────
# Step 1: calculate d1 and d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

print(f"d1 = {d1:.4f}")
print(f"d2 = {d2:.4f}")

# Step 2: N(d1) and N(d2) — probabilities from the normal distribution
N_d1 = norm.cdf(d1)
N_d2 = norm.cdf(d2)

print(f"N(d1) = {N_d1:.4f}")
print(f"N(d2) = {N_d2:.4f}")

# Step 3: the full formula
C = S * N_d1 - K * np.exp(-r * T) * N_d2

print(f"\nBlack-Scholes call price: ${C:.2f}")
print(f"Market price of option:   ${atm_option['lastPrice']:.2f}")
print(f"Difference:               ${abs(C - atm_option['lastPrice']):.2f}")