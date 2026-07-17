# Quant Trading & Risk Lab

A 9-week summer project building a quantitative finance system from scratch.
Covers options pricing, algorithmic trading backtesting, and macroeconomic
regime filtering — all running on real market data.

## Tech Stack
Python · yfinance · pandas · numpy · scipy · matplotlib

## Project Structure
- **Phase 1 (Weeks 1-3):** Options Pricing Engine
- **Phase 2 (Weeks 4-6):** Algorithmic Trading Backtester  
- **Phase 3 (Weeks 7-9):** Macroeconomic Regime Filter

## Phase 1 — Options Pricing Engine

Built a Black-Scholes options pricer from scratch and tested it against
real Apple options data.

### Key Findings
- Black-Scholes inputs extracted from live market data: S, K, T, r, σ
- Historical volatility (AAPL): ~24% annualised
- Ran model across full September 2026 options chain
- Result: model consistently overpriced options vs market, suggesting
  historical volatility is above current implied volatility
- Next step: back-calculate implied volatility from market prices (Week 2)

## How to Run
1. Install dependencies: `pip install yfinance pandas numpy scipy matplotlib`
2. Run any day's script: `python day1.py`