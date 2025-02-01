# Regime-Switching Momentum Strategy 

A quantitative trading framework that leverages daily OHLCV stock data and a Hidden Markov Model (HMM) to dynamically identify market regimes and generate momentum-based trading signals.

## Table of Contents
- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About

The Regime-Switching Momentum Strategy is designed for quantitative traders, financial analysts, and researchers. The project uses daily OHLCV data and advanced statistical methods (HMM) to:
- Detect market regimes (e.g., bullish, bearish, neutral)
- Generate regime-dependent momentum trading signals
- Backtest performance and assess risk management measures

This repository includes planning documents, core modules for data ingestion, feature engineering, regime detection, signal generation, and a backtesting engine.

## Features

- **Dynamic Regime Detection:** Uses a Hidden Markov Model to identify market conditions.
- **Momentum Signal Generation:** Generates buy, hold, and sell signals based on regime-specific momentum.
- **Robust Backtesting:** Simulates historical performance and computes key metrics (Sharpe ratio, drawdown, etc.).
- **Integrated Risk Management:** Implements dynamic risk controls based on market regimes.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Abdullah-BA/RegimeSwitchingMomentumStrategy.git
   cd RegimeSwitchingMomentumStrategy
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

- **Data Ingestion:**  
  Run the data ingestion script to load and preprocess OHLCV data:
  ```bash
  python src/data_ingestion.py
  ```

- **Feature Engineering:**  
  Generate technical indicators:
  ```bash
  python src/feature_engineering.py
  ```

- **Regime Detection:**  
  Train and apply the HMM for regime detection:
  ```bash
  python src/regime_detection.py
  ```

- **Signal Generation and Backtesting:**  
  Generate trading signals and run the backtesting framework:
  ```bash
  python src/signal_generation.py
  python src/backtesting.py
  ```

## Project Structure

```
RegimeSwitchingMomentumStrategy/
│
├── data/
│   ├── PRD.md                # Product Requirements Document
│   ├── color-palette.md      # UI/Visualization Guidelines
│   ├── database-design.md    # Database schema and data flow
│   └── project-structure.md  # Folder structure and conventions
│
├── src/
│   ├── data_ingestion.py     # Load and preprocess OHLCV data
│   ├── feature_engineering.py# Compute technical indicators
│   ├── regime_detection.py   # HMM-based regime detection logic
│   ├── signal_generation.py  # Trading signal generation
│   └── backtesting.py        # Backtesting framework and performance metrics
│
├── .gitignore                # Files to ignore in Git
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview and documentation
```

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with descriptive messages.
4. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or feedback, please reach out to:
- **Name:** Abdullah-BA