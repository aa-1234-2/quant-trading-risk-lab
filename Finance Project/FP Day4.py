import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# ── Part 1: The Normal Distribution ─────────────────────────────────────────
# Pull real Apple returns
ticker = yf.Ticker("AAPL")
hist = ticker.history(period="1y")
hist['log_return'] = np.log(hist['Close'] / hist['Close'].shift(1)).dropna()
real_returns = hist['log_return'].dropna()

# Calculate mean and std of real returns
mu = real_returns.mean()
sigma = real_returns.std()
print(f"Daily mean return:  {mu:.6f} ({mu*100:.4f}%)")
print(f"Daily volatility:   {sigma:.6f} ({sigma*100:.4f}%)")

# Plot real returns vs a normal distribution
x = np.linspace(real_returns.min(), real_returns.max(), 100)
normal_curve = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

plt.figure(figsize=(12, 5))
plt.hist(real_returns, bins=50, density=True, alpha=0.6, color='steelblue', label='Real AAPL Returns')
plt.plot(x, normal_curve, color='red', linewidth=2, label='Normal Distribution')
plt.title('AAPL Daily Log Returns vs Normal Distribution')
plt.xlabel('Daily Log Return')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ── Part 2: Simulating a Random Walk ────────────────────────────────────────
# Starting price
S0 = hist['Close'].iloc[-1]
days = 252          # one trading year
n_paths = 10       # simulate 10 possible futures

plt.figure(figsize=(12, 6))

for i in range(n_paths):
    # Each day: draw a random return from a normal distribution
    daily_returns = np.random.normal(mu, sigma, days)
    
    # Chain them together: each price = previous price * e^(return)
    price_path = [S0]
    for r in daily_returns:
        price_path.append(price_path[-1] * np.exp(r))
    
    plt.plot(price_path, alpha=0.7, linewidth=1)

# Plot the real historical price for comparison
plt.axhline(y=S0, color='black', linestyle='--', linewidth=1.5, label=f'Current Price ${S0:.2f}')
plt.title(f'10 Simulated AAPL Price Paths Over 252 Days (Random Walk)')
plt.xlabel('Trading Days')
plt.ylabel('Stock Price ($)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ── Part 3: The Log-Normal Distribution ─────────────────────────────────────
# Simulate 1000 final prices after 252 days
n_simulations = 1000
final_prices = []

for _ in range(n_simulations):
    daily_returns = np.random.normal(mu, sigma, days)
    final_price = S0 * np.exp(np.sum(daily_returns))
    final_prices.append(final_price)

plt.figure(figsize=(12, 5))
plt.hist(final_prices, bins=50, color='teal', alpha=0.7, edgecolor='white')
plt.axvline(x=S0, color='red', linestyle='--', linewidth=2, label=f'Current Price ${S0:.2f}')
plt.axvline(x=np.mean(final_prices), color='orange', linestyle='--', linewidth=2, label=f'Mean Simulated Price ${np.mean(final_prices):.2f}')
plt.title('Distribution of 1000 Simulated AAPL Prices After 1 Year')
plt.xlabel('Final Stock Price ($)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"\nCurrent price:         ${S0:.2f}")
print(f"Mean simulated price:  ${np.mean(final_prices):.2f}")
print(f"Min simulated price:   ${min(final_prices):.2f}")
print(f"Max simulated price:   ${max(final_prices):.2f}")