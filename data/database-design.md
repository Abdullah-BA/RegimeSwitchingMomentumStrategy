# Database Schema and Data Flow Design for Regime‑Switching Momentum Strategy

This document provides a detailed overview of the database schema and data flow design for a Regime‑Switching Momentum Strategy using daily OHLCV data. The design outlines how raw market data is transformed through feature engineering and regime detection, leading to trading signal generation and comprehensive backtesting.

---

## 1. Database Schema

### 1.1. Raw OHLCV Data Table
**Table Name:** `ohlcv_data`

| Column Name | Data Type | Description                                |
|-------------|-----------|--------------------------------------------|
| date        | DATE      | The trading date.                          |
| ticker      | VARCHAR   | The stock ticker symbol.                   |
| open        | DECIMAL   | Opening price of the day.                  |
| high        | DECIMAL   | Highest price of the day.                  |
| low         | DECIMAL   | Lowest price of the day.                   |
| close       | DECIMAL   | Closing price of the day.                  |
| volume      | BIGINT    | Trading volume of the day.                 |

**Primary Key:** Composite key `(date, ticker)`

---

### 1.2. Technical Indicators Table
**Table Name:** `technical_indicators`

| Column Name         | Data Type | Description                                                          |
|---------------------|-----------|----------------------------------------------------------------------|
| date                | DATE      | Trading date (references `ohlcv_data`).                              |
| ticker              | VARCHAR   | Stock ticker symbol (references `ohlcv_data`).                       |
| sma_20              | DECIMAL   | 20-day Simple Moving Average.                                        |
| sma_50              | DECIMAL   | 50-day Simple Moving Average.                                        |
| ema_20              | DECIMAL   | 20-day Exponential Moving Average.                                   |
| daily_return        | DECIMAL   | Daily return calculated from closing prices.                         |
| volatility          | DECIMAL   | Measure of price volatility (e.g., standard deviation over a window).  |
| additional_indicator| DECIMAL   | Placeholder for any additional technical indicator as required.      |

**Primary Key:** Composite key `(date, ticker)`

---

### 1.3. Regime Classifications Table
**Table Name:** `regime_classifications`

| Column Name  | Data Type | Description                                                                                   |
|--------------|-----------|-----------------------------------------------------------------------------------------------|
| date         | DATE      | Trading date (references `ohlcv_data`).                                                       |
| ticker       | VARCHAR   | Stock ticker symbol (references `ohlcv_data`).                                                |
| regime_label | VARCHAR   | Detected regime label (e.g., "bullish", "bearish", "neutral").                                |
| regime_prob  | DECIMAL   | Confidence level or probability of the regime classification.                                 |
| hmm_state    | INT       | The numerical state output by the Hidden Markov Model (HMM).                                  |

**Primary Key:** Composite key `(date, ticker)`

---

### 1.4. Trading Signals Table
**Table Name:** `trading_signals`

| Column Name       | Data Type | Description                                                                                  |
|-------------------|-----------|----------------------------------------------------------------------------------------------|
| date              | DATE      | Trading date.                                                                                |
| ticker            | VARCHAR   | Stock ticker symbol.                                                                         |
| signal            | VARCHAR   | Trading signal (e.g., "buy", "sell", "hold").                                                |
| indicator_value   | DECIMAL   | Value of the technical indicator or momentum score that triggered the signal.                |
| regime_label      | VARCHAR   | Regime classification at the time the signal was generated.                                  |
| signal_confidence | DECIMAL   | Confidence or strength score of the generated signal.                                        |

**Primary Key:** Composite key `(date, ticker)`

---

### 1.5. Backtesting Results Table
**Table Name:** `backtesting_results`

| Column Name  | Data Type | Description                                                                        |
|--------------|-----------|------------------------------------------------------------------------------------|
| backtest_id  | INT       | Unique identifier for each backtesting run.                                        |
| ticker       | VARCHAR   | Stock ticker symbol for which the backtest was conducted.                          |
| start_date   | DATE      | Start date of the backtesting period.                                              |
| end_date     | DATE      | End date of the backtesting period.                                                |
| total_return | DECIMAL   | Total return achieved over the backtesting period.                                 |
| sharpe_ratio | DECIMAL   | Risk-adjusted return metric (Sharpe ratio).                                         |
| max_drawdown | DECIMAL   | Maximum drawdown observed during the backtest.                                     |
| trades_count | INT       | Total number of trades executed during the backtest.                               |
| win_rate     | DECIMAL   | Percentage of trades that were profitable.                                         |
| notes        | TEXT      | Additional notes, parameters, or remarks regarding the backtest.                   |

**Primary Key:** `backtest_id`

---

## 2. Data Flow Design

This section describes the flow of data from ingestion to backtesting. Each stage is designed to ensure data integrity and provide actionable insights for trading strategy evaluation.

### 2.1. Data Ingestion
- **Source:** Daily OHLCV data is sourced from external providers (APIs, CSV files, databases).
- **Steps:**
  1. **Extraction:** Retrieve raw data for all required tickers and dates.
  2. **Validation:** Check for missing values, correct data formats, and outlier detection.
  3. **Normalization:** Standardize data formats (e.g., date, decimal precision).
  4. **Storage:** Insert the cleaned data into the `ohlcv_data` table.

---

### 2.2. Feature Engineering
- **Input:** Raw data from the `ohlcv_data` table.
- **Steps:**
  1. **Calculation:** Compute technical indicators such as moving averages (SMA, EMA), daily returns, and volatility.
  2. **Aggregation:** Align computed values with corresponding dates and tickers.
  3. **Storage:** Save the results in the `technical_indicators` table.
- **Tools:** This can be achieved using SQL scripts, Python (with libraries such as Pandas), or ETL tools.

---

### 2.3. Regime Detection (Hidden Markov Model)
- **Input:** Technical indicators from the `technical_indicators` table.
- **Steps:**
  1. **Model Training:** Train a Hidden Markov Model (HMM) using historical technical indicator data.
  2. **Classification:** Apply the HMM to each trading day to determine the market regime (e.g., bullish, bearish, neutral).
  3. **Output Generation:** For each record, produce a regime label, associated probability, and HMM state.
  4. **Storage:** Write the regime classification results into the `regime_classifications` table.
- **Notes:** This process can run periodically as new data is ingested or on a scheduled batch process.

---

### 2.4. Signal Generation
- **Inputs:** 
  - Technical indicators from `technical_indicators`
  - Regime classifications from `regime_classifications`
- **Steps:**
  1. **Rule Application:** Combine momentum indicators with regime information to generate trading signals (e.g., "buy" when momentum is strong in a bullish regime).
  2. **Signal Scoring:** Optionally assign a confidence score based on indicator values and regime probability.
  3. **Storage:** Insert the generated trading signals into the `trading_signals` table.
- **Output:** A record for each date and ticker that details the trading signal, the triggering indicator value, the regime context, and a confidence score.

---

### 2.5. Backtesting
- **Inputs:** 
  - Trading signals from `trading_signals`
  - Raw market data from `ohlcv_data`
- **Steps:**
  1. **Simulation:** Simulate trades over historical data using the generated signals.
  2. **Metric Calculation:** Compute key performance metrics, including total return, Sharpe ratio, maximum drawdown, trade count, and win rate.
  3. **Visualization:** Create equity curves, drawdown charts, and regime plots to visualize strategy performance.
  4. **Storage:** Save aggregated backtesting results and metadata into the `backtesting_results` table.
- **Tools:** Use a dedicated backtesting engine or Python libraries such as Pandas and Matplotlib to execute and visualize the backtests.

---

## 3. Conclusion

This document details the structured database schema and the systematic data flow for a Regime‑Switching Momentum Strategy that leverages daily OHLCV data. The design ensures that:

- **Data Ingestion:** Reliable acquisition and storage of raw market data.
- **Feature Engineering:** Accurate calculation and storage of technical indicators.
- **Regime Detection:** Robust identification of market regimes using a Hidden Markov Model.
- **Signal Generation:** Clear and actionable trading signals that factor in both momentum and market regime.
- **Backtesting:** Comprehensive performance evaluation through historical simulation.

Together, these components form an integrated system that supports effective quantitative trading strategy development and evaluation.
