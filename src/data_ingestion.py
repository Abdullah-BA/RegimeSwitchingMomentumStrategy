# data_ingestion.py
import pandas as pd
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_data(file_path):
    """
    Reads OHLCV data from a CSV file.
    
    Parameters:
        file_path (str): The path to the CSV file.
        
    Returns:
        pd.DataFrame: DataFrame containing the raw OHLCV data.
    """
    try:
        data = pd.read_csv(file_path, parse_dates=['date'])
        logging.info(f"Successfully read data from {file_path}")
        return data
    except Exception as e:
        logging.error(f"Error reading data from {file_path}: {e}")
        raise

def clean_data(df):
    """
    Cleans the OHLCV data by handling missing values and adjusting for splits/dividends.
    
    Parameters:
        df (pd.DataFrame): Raw OHLCV data.
        
    Returns:
        pd.DataFrame: Cleaned OHLCV data.
    """
    try:
        # Drop rows with missing essential values
        df.dropna(subset=['open', 'high', 'low', 'close', 'volume'], inplace=True)
        
        # Sort by date to ensure time series order
        df.sort_values('date', inplace=True)
        
        # Example: Adjust for splits/dividends if an 'adj_close' column exists.
        if 'adj_close' in df.columns:
            # Compute adjustment factor and adjust OHLC prices
            df['adjustment_factor'] = df['adj_close'] / df['close']
            for col in ['open', 'high', 'low', 'close']:
                df[col] = df[col] * df['adjustment_factor']
            logging.info("Adjusted OHLC prices using adjustment factor.")
            df.drop(columns=['adjustment_factor'], inplace=True)
        
        return df
    except Exception as e:
        logging.error(f"Error cleaning data: {e}")
        raise

def save_cleaned_data(df, output_path):
    """
    Saves the cleaned data to a CSV file.
    
    Parameters:
        df (pd.DataFrame): Cleaned OHLCV data.
        output_path (str): Path to save the cleaned CSV.
    """
    try:
        df.to_csv(output_path, index=False)
        logging.info(f"Cleaned data saved to {output_path}")
    except Exception as e:
        logging.error(f"Error saving cleaned data: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    input_file = os.path.join('data', 'raw', 'ohlcv_data.csv')
    output_file = os.path.join('data', 'processed', 'cleaned_ohlcv_data.csv')
    
    # Read raw data from CSV (or modify to read from an API as needed)
    raw_data = read_data(input_file)
    
    # Clean the data (handle missing values and adjust prices)
    cleaned_data = clean_data(raw_data)
    
    # Save the cleaned data for further processing
    save_cleaned_data(cleaned_data, output_file)
