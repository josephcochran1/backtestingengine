import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

#download historical price data
def download_data(ticker, start_date, end_date):
    """Download historical OHLCY dta from yfinance"""
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    return data

#Calculating moving averages
def calculate_moving_averages(data, short_window=50, long_window=200):
    """Calculate short and long moving averages"""
    data['MA_short'] = data['Close'].rolling(window=short_window).mean()
    data['MA_long'] = data['Close'].rolling(window=long_window).mean()
    return data

#Generate trading signals
def generate_signals(data):
    """Generate buy/sell singals based on MA crossover"""
    data['Signal'] = 0 #No position

    #Buy singal: MA_short crosses above MA_long
    data.loc[data['MA_short'] > data['MA_long'], 'Signal'] = 1

    #Buy singal: MA_short crosses below MA_long
    data.loc[data['MA_short'] < data['MA_long'], 'Signal'] = -1

    #calculate position changes (actual buy/sell events)
    data['Position'] = data['Signal'].diff()

    return data

# Simulate trades and calculate returns
def calculate_returns(data):
    """Calculate trade returns and cumulative P&L"""
    # Daily returns
    data['Daily_Return'] = data['Close'].pct_change()
    
    # Strategy return: only apply daily return when holding position (Signal == 1)
    data['Strategy_Return'] = data['Signal'].shift(1) * data['Daily_Return']
    
    # Cumulative returns
    data['Cumulative_Market_Return'] = (1 + data['Daily_Return']).cumprod() - 1
    data['Cumulative_Strategy_Return'] = (1 + data['Strategy_Return']).cumprod() - 1
    
    return data

# Calculate performance metrics
def calculate_metrics(data):
    """Calculate Sharpe ratio, max drawdown, win rate, and other metrics"""
    
    # Remove NaN values for calculations
    strategy_returns = data['Strategy_Return'].dropna()
    
    # Sharpe ratio (annualized, assuming 252 trading days)
    sharpe_ratio = (strategy_returns.mean() / strategy_returns.std()) * np.sqrt(252)
    
    # Max drawdown
    cumulative = (1 + strategy_returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # Win rate (percentage of positive days)
    win_rate = (strategy_returns > 0).sum() / len(strategy_returns) * 100
    
    # Total return
    total_return = data['Cumulative_Strategy_Return'].iloc[-1] * 100
    
    metrics = {
        'Total Return (%)': total_return,
        'Sharpe Ratio': sharpe_ratio,
        'Max Drawdown (%)': max_drawdown * 100,
        'Win Rate (%)': win_rate
    }
    
    return metrics

# Visualize results
def plot_results(data, ticker):
    """Plot price, moving averages, and strategy performance"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: Price and moving averages
    ax1.plot(data.index, data['Close'], label='Close Price', linewidth=2)
    ax1.plot(data.index, data['MA_short'], label='MA 50', linewidth=1.5, alpha=0.7)
    ax1.plot(data.index, data['MA_long'], label='MA 200', linewidth=1.5, alpha=0.7)
    ax1.set_title(f'{ticker} Price and Moving Averages', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Price ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Cumulative returns comparison
    ax2.plot(data.index, data['Cumulative_Market_Return'] * 100, label='Buy & Hold', linewidth=2)
    ax2.plot(data.index, data['Cumulative_Strategy_Return'] * 100, label='MA Crossover Strategy', linewidth=2)
    ax2.set_title('Strategy vs Buy & Hold Returns', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Return (%)')
    ax2.set_xlabel('Date')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'/Users/joe/Desktop/black scholes model stuff/backtest_{ticker}.png', dpi=300), plt.show()

    # Main execution
if __name__ == "__main__":
    # Parameters
    ticker = "BTC-USD"  # Bitcoin in USD
    start_date = "2023-01-01"
    end_date = "2024-06-26"
    
    print(f"Backtesting MA Crossover Strategy on {ticker}")
    print("=" * 50)
    
    # Run backtest
    data = download_data(ticker, start_date, end_date)
    data = calculate_moving_averages(data)
    data = generate_signals(data)
    data = calculate_returns(data)
    metrics = calculate_metrics(data)
    
    # Print metrics
    print("\nPerformance Metrics:")
    print("-" * 50)
    for key, value in metrics.items():
        print(f"{key}: {value:.2f}")
    
    # Plot results
    plot_results(data, ticker)

    
