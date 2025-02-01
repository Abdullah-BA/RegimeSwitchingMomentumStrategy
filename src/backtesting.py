# backtesting.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_performance_metrics(df):
    """
    Calculates performance metrics such as cumulative returns, Sharpe ratio, and maximum drawdown.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing OHLCV data and trading signals.
                           Expected columns: 'date', 'close', 'signal'.
    
    Returns:
        tuple: (metrics (dict), df (pd.DataFrame) updated with performance columns)
    """
    # Calculate daily returns from closing prices
    df['daily_return'] = df['close'].pct_change().fillna(0)
    
    # Compute strategy returns based on generated signals.
    # Assumption:
    #   'buy'  -> take a long position (strategy_return = daily_return)
    #   'sell' -> take a short position (strategy_return = -daily_return)
    #   'hold' -> no position (strategy_return = 0)
    def signal_return(row):
        if row['signal'] == 'buy':
            return row['daily_return']
        elif row['signal'] == 'sell':
            return -row['daily_return']
        else:
            return 0
    
    df['strategy_return'] = df.apply(signal_return, axis=1)
    df['cumulative_return'] = (1 + df['strategy_return']).cumprod()
    
    # Calculate Sharpe Ratio (assume a risk-free rate of 0)
    sharpe_ratio = np.mean(df['strategy_return']) / np.std(df['strategy_return']) * np.sqrt(252)
    
    # Calculate maximum drawdown
    cumulative = df['cumulative_return']
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    
    metrics = {
        'cumulative_return': df['cumulative_return'].iloc[-1],
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown
    }
    
    return metrics, df

def plot_performance(df, metrics):
    """
    Plots performance charts including cumulative returns and drawdown.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'date' and 'cumulative_return'.
        metrics (dict): Dictionary containing performance metrics.
    """
    plt.figure(figsize=(14, 7))
    
    # Plot cumulative returns
    plt.subplot(2, 1, 1)
    plt.plot(df['date'], df['cumulative_return'], label='Cumulative Return', color='blue')
    plt.title('Cumulative Returns')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    
    # Plot drawdown
    rolling_max = df['cumulative_return'].cummax()
    drawdown = (df['cumulative_return'] - rolling_max) / rolling_max
    plt.subplot(2, 1, 2)
    plt.plot(df['date'], drawdown, label='Drawdown', color='red')
    plt.title('Drawdown')
    plt.xlabel('Date')
    plt.ylabel('Drawdown')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def run_backtest(ohlcv_file, signals_file):
    """
    Runs the backtesting process by merging OHLCV data with trading signals,
    calculating performance metrics, and plotting the performance charts.
    
    Parameters:
        ohlcv_file (str): Path to the CSV file containing OHLCV data.
        signals_file (str): Path to the CSV file containing trading signals.
    
    Returns:
        dict: Performance metrics.
    """
    try:
        # Load OHLCV data and trading signals
        df_ohlcv = pd.read_csv(ohlcv_file, parse_dates=['date'])
        df_signals = pd.read_csv(signals_file, parse_dates=['date'])
        
        # Merge data on the 'date' column; modify merge key if necessary (e.g., ticker)
        df = pd.merge(df_ohlcv, df_signals[['date', 'signal']], on='date', how='inner')
        
        # Calculate performance metrics and augment DataFrame with performance metrics
        metrics, df = calculate_performance_metrics(df)
        logging.info(f"Backtesting metrics: {metrics}")
        
        # Plot performance charts
        plot_performance(df, metrics)
        
        return metrics
    except Exception as e:
        logging.error(f"Error in backtesting: {e}")
        raise

if __name__ == "__main__":
    import os
    # Example file paths for OHLCV data and trading signals
    ohlcv_file = os.path.join('data', 'processed', 'cleaned_ohlcv_data.csv')
    signals_file = os.path.join('data', 'processed', 'trading_signals.csv')
    
    # Run the backtesting process
    metrics = run_backtest(ohlcv_file, signals_file)
    print("Backtesting Metrics:")
    print(metrics)
