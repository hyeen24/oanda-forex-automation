import requests
import pandas as pd
import os
import json

class OandaAPI:
    _RISK = 1# % loss
    
    def __init__(self):
        # load_dotenv()
        self.__API_KEY = os.getenv("API_KEY")
        self.__ACCOUNT_ID = os.getenv("ACCOUNT_ID")
        self.__URL = os.getenv("OANDA_URL")
        self.__SECURE_HEADER = {
            'Authorization': f'Bearer {self.__API_KEY}',
            'Content-Type': 'application/json'
        }
        self.__session = requests.Session()

    def fetch_candles_data(self, instrument="XAU_USD", granularity="H1", count=200):
        """
        Fetches historical candle data for a given instrument.

        Parameters:
        instrument (str): The instrument to fetch data for (default is "XAU_USD").
        granularity (str): The granularity of the candles (default is "H1").
        count (int): The number of candles to fetch (default is 200).

        Returns:
        dict: The JSON response containing the candle data.
        """
        params = {
            "count": count,
            "granularity": granularity,
        }

        url = f"{self.__URL}/instruments/{instrument}/candles"
        response = self.__session.get(url, params=params, headers=self.__SECURE_HEADER) 
        
        return response.json()
    
    def fetch_account_data(self):
        """
        Fetches account data for the authenticated user.

        Returns:
        dict: The JSON response containing the account data.
        """
        url = f"{self.__URL}/accounts/{self.__ACCOUNT_ID}/summary"

        response = self.__session.get(url, headers=self.__SECURE_HEADER)

        return response.json()
    
    def get_account_balance(self):
        """
        Retrieves the account balance for the authenticated user.

        Returns:
        float: The account balance.
        """
        account = self.fetch_account_data()

        return float(account['account']['balance'])
    
    def calculate_position_size(self, entry_price, stop_loss_price):
        """
        Calculates the position size based on entry price, stop loss price, and risk percentage.

        Parameters:
        entry_price (float): The price at which the position is entered.
        stop_loss_price (float): The price at which the position will be exited to prevent further loss.

        Returns:
        float: The calculated position size.
        """
        account_balance = self.get_account_balance()
        # Calculate risk amount
        risk_amount = account_balance * OandaAPI._RISK /100

        # Calculate position size
        risk_per_unit = abs(entry_price - stop_loss_price)
        if risk_per_unit == 0:
            raise ValueError("Entry price and stop loss price cannot be the same.")

        position_size = risk_amount / risk_per_unit
        return position_size
    
    def get_position(self):
        """
        Retrieves the open position for the authenticated user.
        """
        url = f"{self.__URL}/accounts/{self.__ACCOUNT_ID}/openPositions"

        response = self.__session.get(url,headers=self.__SECURE_HEADER)
        return response.json()
    
    def place_order(self,instrument, units,price, stop_loss_price, take_profit_price):
        url = f"{self.__URL}/accounts/{self.__ACCOUNT_ID}/orders"
        
        data = {
            "order": {
                "price": price,
                "stopLossOnFill": {
                    "timeInForce": "GTC",
                    "price": str(stop_loss_price)
                },
                "takeProfitOnFill": {
                    "timeInForce": "GTC",
                    "price": str(take_profit_price)
                },
                "timeInForce": "GTC",
                "instrument": instrument,
                "units": str(units),
                "type": "LIMIT",
                "positionFill": "DEFAULT"
            }
        }

        response = self.__session.post(url, headers=self.__SECURE_HEADER,data=json.dumps(data))

        print(response.json())

    def get_pending_order(self):
        url = f"{self.__URL}/accounts/{self.__ACCOUNT_ID}/pendingOrders"
        response = self.__session.get(url, headers=self.__SECURE_HEADER)
        return response.json()




