# regime_detection.py
import pandas as pd
import numpy as np
import logging
from models.hmm_model import build_hmm_model

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def prepare_features(df):
    """
    Prepares the feature matrix for HMM training using technical indicators.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing technical indicators. Expected columns include:
                           'daily_return' and 'volatility_20'.
    
    Returns:
        np.ndarray: 2D array with features for each observation.
    """
    # Select and fill missing values for required features
    features = df[['daily_return', 'volatility_20']].fillna(0).values
    return features

def train_hmm(df, n_components=3):
    """
    Trains the HMM using technical indicators and assigns regime classifications.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing technical indicators.
        n_components (int): Number of regimes (states) to model.
        
    Returns:
        pd.DataFrame: Original DataFrame with additional columns 'hmm_state' and 'regime_label'.
    """
    try:
        # Prepare feature matrix
        X = prepare_features(df)
        
        # Build and train HMM model
        model = build_hmm_model(n_components=n_components)
        model.fit(X)
        logging.info("HMM model trained successfully.")
        
        # Predict hidden states (market regimes)
        hidden_states = model.predict(X)
        
        # Map numeric states to regime labels (customize as needed)
        regime_mapping = {0: 'bullish', 1: 'bearish', 2: 'neutral'}
        df['hmm_state'] = hidden_states
        df['regime_label'] = [regime_mapping.get(state, 'unknown') for state in hidden_states]
        
        return df
    except Exception as e:
        logging.error(f"Error in training HMM: {e}")
        raise

if __name__ == "__main__":
    import os
    # Load the feature-engineered data
    file_path = os.path.join('data', 'processed', 'features_ohlcv_data.csv')
    df = pd.read_csv(file_path, parse_dates=['date'])
    
    # Train the HMM and get regime classifications
    df = train_hmm(df, n_components=3)
    
    # Save the updated DataFrame with regime information
    output_path = os.path.join('data', 'processed', 'regime_classifications.csv')
    df.to_csv(output_path, index=False)
    logging.info(f"Regime classifications saved to {output_path}")
