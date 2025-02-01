# feature_engineering.py
import pandas as pd

def compute_moving_average(df, window=20):
    """
    Computes the simple moving average (SMA) for the 'close' column.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing OHLCV data.
        window (int): Number of periods for the moving average.
        
    Returns:
        pd.DataFrame: DataFrame with a new column 'sma_{window}' appended.
    """
    sma_column = f'sma_{window}'
    df[sma_column] = df['close'].rolling(window=window, min_periods=1).mean()
    return df

def compute_daily_return(df):
    """
    Computes daily returns based on the 'close' price.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing OHLCV data.
        
    Returns:
        pd.DataFrame: DataFrame with a new column 'daily_return' appended.
    """
    df['daily_return'] = df['close'].pct_change().fillna(0)
    return df

def compute_volatility(df, window=20):
    """
    Computes volatility as the rolling standard deviation of daily returns.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing OHLCV data.
        window (int): Number of periods for the rolling standard deviation.
        
    Returns:
        pd.DataFrame: DataFrame with a new column 'volatility_{window}' appended.
    """
    vol_column = f'volatility_{window}'
    # Ensure that 'daily_return' exists; compute if necessary.
    if 'daily_return' not in df.columns:
        df = compute_daily_return(df)
    df[vol_column] = df['daily_return'].rolling(window=window, min_periods=1).std()
    return df

if __name__ == "__main__":
    import os
    # Load cleaned data for feature engineering
    file_path = os.path.join('data', 'processed', 'cleaned_ohlcv_data.csv')
    df = pd.read_csv(file_path, parse_dates=['date'])
    
    # Compute technical indicators
    df = compute_moving_average(df, window=20)
    df = compute_moving_average(df, window=50)
    df = compute_daily_return(df)
    df = compute_volatility(df, window=20)
    
    # Save the resulting DataFrame with technical indicators
    output_path = os.path.join('data', 'processed', 'features_ohlcv_data.csv')
    df.to_csv(output_path, index=False)
