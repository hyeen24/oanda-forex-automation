# OANDA Forex Trading Automation

## Overview
This project provides an automated trading system for the OANDA forex trading platform. It is designed to execute trades based on predefined strategies and market conditions.
![image](https://github.com/user-attachments/assets/565571f7-ced6-428d-a410-f5ab1fb7a5b8)


## Features
- Automated trade execution
- Real-time market data analysis
- Customizable trading strategies
- Risk management tools

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/oanda_forex.git
    ```
2. Navigate to the project directory:
    ```sh
    cd oanda_forex
    ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   

## Configuration
1. Create a configuration file `.env` in the root directory with your OANDA API credentials and trading preferences:
    ```
    API_KEY=YOUR API KEY
    ACCOUNT_ID=YOUR ACCOUNT ID
    OANDA_PRAC_URL="https://api-fxpractice.oanda.com/v3"
    OANDA_URL="https://api-fxtrade.oanda.com/v3"
    ```

## Testing
You can test your strategy using a python notebook to test if it works before running it on your bot.

After testing your strategy you can modify your signal class according to your strategy.

## Usage
1. Run the trading bot:
    ```sh
    python main.py
    ```



