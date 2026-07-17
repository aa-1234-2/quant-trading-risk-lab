import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# ── Pull data ────────────────────────────────────────────────────────────────
ticker = yf.Ticker("AAPL")
current_price = ticker.info['currentPrice']
print(f"Apple current price: ${current_price}")

chain = ticker.option_chain("2026-07-17")
calls = chain.calls.copy()

# ── Calculate intrinsic and time value ──────────────────────────────────────
# Intrinsic value: how much in-the-money the option is (floor at 0)
calls['intrinsic_value'] = (current_price - calls['strike']).clip(lower=0)

# Time value: whatever is left over after intrinsic value
calls['time_value'] = calls['lastPrice'] - calls['intrinsic_value']

# Print a clean summary table
summary = calls[['strike', 'lastPrice', 'intrinsic_value', 'time_value', 'inTheMoney']].copy()
print(summary.to_string(index=False))

# ── Plot premium vs strike price ─────────────────────────────────────────────
plt.figure(figsize=(12, 6))
plt.plot(calls['strike'], calls['lastPrice'],    label='Total Premium',   color='blue')
plt.plot(calls['strike'], calls['intrinsic_value'], label='Intrinsic Value', color='green', linestyle='--')
plt.plot(calls['strike'], calls['time_value'],   label='Time Value',      color='orange', linestyle='--')

# Mark current stock price
plt.axvline(x=current_price, color='red', linestyle=':', label=f'Current Price ${current_price}')

plt.title('AAPL Call Options — Premium Breakdown by Strike Price')
plt.xlabel('Strike Price ($)')
plt.ylabel('Option Premium ($)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()