Backtesting Engine: Moving Average Crossover Strategy

Overview

A Python backtesting framework that simulates a moving average crossover trading strategy on live market data. The engine downloads historical price data (crypto, forex, stocks), generates buy/sell signals, tracks returns, and computes performance metrics.


Strategy

Moving Average Crossover: Buy when the 50-day MA crosses above the 200-day MA; sell when it crosses below.


Simple trend-following approach
Historically effective on trending assets
Easy to extend and optimize



How It Works


Download Data: Fetch historical OHLCV data using yfinance
Calculate MAs: Compute 50-day and 200-day moving averages
Generate Signals: Buy (MA50 > MA200), Sell (MA50 < MA200)
Simulate Trades: Track entry/exit prices and position returns
Calculate Metrics: Sharpe ratio, max drawdown, win rate, total return
Visualize: Plot price action, MAs, and cumulative returns



Performance Metrics

MetricMeaningTotal ReturnCumulative profit/loss over backtest periodSharpe RatioRisk-adjusted return (higher is better; >1.0 is good)Max DrawdownWorst peak-to-trough decline (risk measure)Win Rate% of days with positive returns


Usage

Run the Backtest

bashpython3 backtesting_engine.py

Customize

Open backtesting_engine.py and change:

pythonticker = "BTC-USD"          # Any yfinance ticker
start_date = "2023-01-01"
end_date = "2024-06-26"


Results

Example Output:

Backtesting MA Crossover Strategy on BTC-USD
==================================================

Performance Metrics:
--------------------------------------------------
Total Return (%): 85.32
Sharpe Ratio: 1.24
Max Drawdown (%): -18.45
Win Rate (%): 52.30

Chart:

Show Image

The chart shows:


Top panel: Bitcoin price (black), 50-day MA (blue), 200-day MA (orange)
Bottom panel: Strategy cumulative return (blue) vs buy-and-hold (orange)



Dependencies

bashpip3 install pandas numpy matplotlib yfinance


Next Steps


Test on other cryptocurrencies (ETH, SOL, etc.)
Optimize MA periods for different assets
Add stop-loss and risk management
Track individual trades and trade statistics
Combine with other indicators (RSI, MACD, etc.)



Key Concepts Demonstrated


Signal generation from market data
Position tracking and return attribution
Vectorized backtesting (efficient, no loops)
Risk-adjusted performance metrics
Data visualization
