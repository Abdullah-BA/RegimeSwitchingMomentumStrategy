# signal_generation.py
import pandas as pd

def generate_signals(df, momentum_threshold=0.01):
    """
    Generates trading signals based on momentum indicators and regime classifications.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing technical indicators and regime labels.
                           Expected columns: 'daily_return', 'sma_20', 'sma_50', 'regime_label'.
        momentum_threshold (float): Threshold for daily return to consider as strong momentum.
    
    Returns:
        pd.DataFrame: DataFrame with a new column 'signal' containing 'buy', 'sell', or 'hold'.
    """
    signals = []
    
    for _, row in df.iterrows():
        regime = row.get('regime_label', 'neutral')
        daily_return = row.get('daily_return', 0)
        sma_20 = row.get('sma_20', 0)
        sma_50 = row.get('sma_50', 0)
        
        # Example logic: adjust thresholds based on the current market regime
        if regime == 'bullish':
            # In bullish regimes, a modest positive return may signal a buy
            if daily_return > momentum_threshold:
                signal = 'buy'
            elif daily_return < -momentum_threshold:
                signal = 'sell'
            else:
                signal = 'hold'
        elif regime == 'bearish':
            # In bearish regimes, use stricter thresholds for decision making
            if daily_return > momentum_threshold * 1.5:
                signal = 'buy'
            elif daily_return < -momentum_threshold * 1.5:
                signal = 'sell'
            else:
                signal = 'hold'
        else:
            # In neutral regimes, use a simple moving average crossover strategy
            if sma_20 > sma_50:
                signal = 'buy'
            elif sma_20 < sma_50:
                signal = 'sell'
            else:
                signal = 'hold'
        
        signals.append(signal)
    
    df['signal'] = signals
    return df

if __name__ == "__main__":
    import os
    # Load the data with regime classifications and technical indicators
    file_path = os.path.join('data', 'processed', 'regime_classifications.csv')
    df = pd.read_csv(file_path, parse_dates=['date'])
    
    # Generate trading signals
    df = generate_signals(df, momentum_threshold=0.01)
    
    # Save the generated signals to a CSV file
    output_path = os.path.join('data', 'processed', 'trading_signals.csv')
    df.to_csv(output_path, index=False)
    print(f"Trading signals saved to {output_path}")
    
    # Example call:
    # signals_df = generate_signals(your_dataframe, momentum_threshold=0.01)
