Backtesting Engine: Moving Average Crossover Strategy

Overview

A Python-based backtesting framework that simulates a moving average (MA) crossover trading strategy on historical price data. The engine downloads live market data (crypto and forex), generates buy/sell signals based on MA crossovers, tracks P&L, and computes performance metrics including Sharpe ratio, maximum drawdown, and win rate.

This project demonstrates core quantitative finance concepts: signal generation, position tracking, return attribution, and risk-adjusted performance measurement.


Strategy: Moving Average Crossover

Logic

The MA crossover strategy is a trend-following approach that generates trades based on the relationship between two exponential moving averages:


Short MA (50-day): Captures recent price momentum
Long MA (200-day): Captures longer-term trend direction


Buy Signal: When MA_short crosses above MA_long → market is entering an uptrend
Sell Signal: When MA_short crosses below MA_long → market is exiting the trend

Why This Strategy?


- It is simple and interpretable (ideal for demonstrating backtesting mechanics)
- Historically effective on trending assets (cryptocurrencies, forex pairs)
- Easily extensible (can swap MA periods, add filters, test multiple timeframes)



Technical Implementation

Data Pipeline


Download Historical Data (download_data)

Uses yfinance to fetch OHLCV (Open, High, Low, Close, Volume) data
Default: Bitcoin/USD (BTC-USD) from 2023-01-01 to 2024-06-26
Easily configurable for any yfinance-supported ticker



Calculate Moving Averages (calculate_moving_averages)

MA_short = Close.rolling(50).mean()
MA_long = Close.rolling(200).mean()
Uses pandas rolling window—efficient and vectorized



Generate Signals (generate_signals)

Signal = 1 when MA_short > MA_long (in position)
Signal = -1 when MA_short < MA_long (flat)
Position = diff(Signal) captures actual crossover events (0, +1, -1)



Calculate Returns (calculate_returns)

Daily returns: pct_change() of closing price
Strategy return = Signal(t-1) × Daily_Return(t)

Only earns return while holding a position
Naturally accounts for entry/exit timing



Cumulative returns: (1 + returns).cumprod() - 1



Compute Metrics (calculate_metrics)

See Performance Metrics section below






Performance Metrics

Sharpe Ratio (Annualized)

Sharpe = (Mean Return / Std Dev) × √252


Measures risk-adjusted return (return per unit of volatility)
Higher is better (typical range: 0.5–2.0 is good, >2.0 is excellent)
252 = trading days in a year


Maximum Drawdown

Drawdown(t) = (Cumulative Return(t) - Running Peak) / Running Peak
Max Drawdown = min(Drawdown)


Worst peak-to-trough decline
Indicates downside risk and psychological stress
Expressed as percentage (e.g., -25% means 25% loss from peak)


Win Rate

Win Rate = (# Positive Return Days / Total Days) × 100


Percentage of days with positive strategy returns
Does NOT measure profit per trade (a few large winners can offset many small losers)


Total Return

Total Return = (Final Value - Initial Value) / Initial Value × 100


Cumulative return over the entire backtest period
Benchmark: compare to buy-and-hold return



How to Use

Basic Usage

bashpython3 backtesting_engine.py

This runs the default configuration:


Ticker: BTC-USD (Bitcoin)
Period: 2023-01-01 to 2024-06-26
MA Periods: 50 and 200 days


Customize Parameters

Open backtesting_engine.py and modify the if __name__ == "__main__" section:

pythonticker = "BTC-USD"          # Change ticker (e.g., "ETH-USD", "EURUSD=X")
start_date = "2023-01-01"   # Change start date
end_date = "2024-06-26"     # Change end date

Then rerun the script.

Example Output

Terminal Output:

Backtesting MA Crossover Strategy on BTC-USD
==================================================

Performance Metrics:
--------------------------------------------------
Total Return (%): 85.32
Sharpe Ratio: 1.24
Max Drawdown (%): -18.45
Win Rate (%): 52.30

Saved Files:

backtest_BTC-USD.png: Chart with price, MAs, and cumulative returns

Interpretation Guide

What Good Metrics Look Like

MetricGood RangeInterpretationTotal ReturnPositiveStrategy profitable over periodSharpe Ratio> 1.0Good risk-adjusted returnsMax Drawdown> -30%Acceptable downside riskWin Rate> 50%More winning days than losing

Example Scenario

Suppose the backtest returns:

Total Return: 85% (strategy) vs 60% (buy-and-hold)
Sharpe Ratio: 1.24
Max Drawdown: -18%
Win Rate: 52%

Interpretation: The strategy outperformed buy-and-hold by 25% while maintaining reasonable risk metrics. The 1.24 Sharpe ratio indicates solid risk-adjusted returns. The -18% max drawdown is acceptable for a trend-following strategy.

Extensions & Next Steps

Immediate Enhancements

Multiple Tickers

Loop over a list of cryptocurrencies or forex pairs
Compare performance across assets

Parameter Optimization

Test different MA periods (e.g., 20/50, 100/200)
Find optimal parameters for different timeframes

Trade-Level Analysis

Track individual trades (entry price, exit price, duration, P&L)
Calculate trade-by-trade metrics (avg win, avg loss, trade duration)

Risk Management

Add stop-loss logic
Add position sizing based on volatility

Advanced Extensions
Combine with other indicators (RSI, MACD, Bollinger Bands)
Machine learning signal generation
Portfolio-level backtesting (multiple correlated assets)
Transaction costs and slippage modeling

Dependencies
pandas: Data manipulation and time-series analysis
numpy: Numerical computations
matplotlib: Static visualization
yfinance: Download historical market data

Install all:
bashpip3 install pandas numpy matplotlib yfinance

Key Learnings
This backtesting engine demonstrates:
- Signal Generation: How to convert market data into trading rules
- Position Tracking: Maintaining entry/exit state and computing returns correctly
- Performance Attribution: Isolating strategy return from market return
- Risk Metrics: Quantifying downside risk and consistency
- Vectorized Computation: Using pandas for efficient backtesting (no loops over bars)

Limitations & Considerations
- Survivorship Bias: Using current tickers (excludes delisted assets)
- Look-Ahead Bias: None in this implementation (uses only past data)
- Transaction Costs: Not modeled (real trading incurs commissions/slippage)
- Overfitting: MA periods are fixed; true optimization requires walk-forward testing
- Regime Changes: Past performance on 2023-2024 crypto may not repeat

Author & Purpose

Built as part of a quantitative finance portfolio to demonstrate:
- Python proficiency (pandas, numpy, matplotlib)
- Understanding of trading strategy mechanics
- Ability to translate financial concepts into working code



Contact & Further Work

For questions, enhancements, or alternative strategies, see the main GitHub repository.
