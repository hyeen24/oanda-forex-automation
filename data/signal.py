import pandas as pd
from api.oanda import OandaAPI

class Signal:
    def __init__(self, data):
        self.__data = data
        self.__df = self.convert_data_to_dataframe()

    @property
    def df(self):
        return self.__df
    
    @property
    def lastcandle(self):
        return self.__df.iloc[-1]
    
    def convert_data_to_dataframe(self):
        hist_data = []
        for candle in self.__data['candles']:
            if candle['complete']:
                hist = dict(
                    time=candle['time'],
                    volume=candle['volume'],
                    open=float(candle['mid']['o']),
                    low=float(candle['mid']['l']),
                    high=float(candle['mid']['h']),
                    close=float(candle['mid']['c']),
                )
                hist_data.append(hist)

        df = pd.DataFrame(hist_data)
        return df
    
    def transform_data(self):
        df = self.df.copy()

        # Calculate EMAs
        df['EMA_200'] = df['close'].ewm(span=200, adjust=False).mean()
        df['EMA_50'] = df['close'].ewm(span=50, adjust=False).mean()
        df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()

        # Caluculate the difference between the EMAs
        df['diff'] =  df['EMA_20'] - df['EMA_50']

        # Determine the previous difference
        df['diff_prev'] = df['diff'].shift(1)

        # If cross downward, set to -1, if cross upward, set to 1
        df['cross'] = ((df['diff'] > 0) & (df['diff_prev'] < 0)).astype(int) - \
                        ((df['diff'] < 0) & (df['diff_prev'] > 0)).astype(int)

        # Calculate the low and high for the last 50 candles
        df['last_low'] = df['low'].rolling(window=50, min_periods=1).min()
        df['last_high'] = df['high'].rolling(window=50, min_periods=1).max()

        # Determine the trade signals
        df[['isTrade', 'takeprofit', 'stoploss']] = df.apply(self.is_trade, axis=1, result_type="expand")

        return df
    
    def is_trade(self, row):
        try:
            if row['cross'] == 1 and row['close'] > row['EMA_200']: # close > ema200 is uptrend
                isTrade = True
                stoploss = row['last_low']
                lossdept = abs(row['close'] - stoploss)
                takeprofit = max(row['last_high'], row['close'] + 2 * lossdept)  # Ensure TP is 2x SL
                
                return isTrade, takeprofit, stoploss

            if row['cross'] == -1 and row['close'] < row['EMA_200']: # close < ema200 is downtrend
                isTrade = True
                stoploss = row['last_high']
                lossdept = abs(row['close'] - stoploss)
                takeprofit = min(row['close'] - 2 * lossdept, row['last_low'])  # Ensure TP is 2x SL
                
                return isTrade, takeprofit, stoploss
        except Exception as e:
            print(f"Error: {e}")
        
        return False, None, None