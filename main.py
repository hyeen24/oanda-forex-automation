import time
from api.oanda import OandaAPI
from data.signal import Signal
from datetime import datetime


def automated_trading_loop():

    while True:
        instrument = "USD_HKD"
        oanda = OandaAPI()
        raw_data = oanda.fetch_candles_data(instrument,"M1",201)
        dt =  Signal(raw_data)
        dt.transform_data()

        # Retrieve the last candle data
        last = dt.lastcandle
        takeprofit = last['takeprofit']
        stoploss = last['stoploss']
        entry = last['close']

        # Get the current position and pending order
        open_pos = oanda.get_position()
        pending_pos = oanda.get_pending_order()

        # Check if the instrument is in the position
        if open_pos['positions']:
            
            pos_list = []
            for item in open_pos['positions']:
                pos_list.append(item['instrument'])

            if instrument in pos_list:
                print("currently in position...waiting to close...")
            else:
                print("Position closed. Balance :",oanda.get_account_balance())
        
        # Check if the instrument is in the pending order
        elif pending_pos['orders']:
            print(pending_pos['orders'])
            print("Currently in pending order...waiting to execute...")
            
        else:    
            # If there is a trade signal, place the trade 
            if last['isTrade']:          
                print("Not in a trade, placing trade...")
                
                
                position_size = oanda.calculate_position_size(entry,stoploss)
                
                if entry < stoploss:
                    position_size = -position_size

                position_size = round(position_size)
                takeprofit = round(takeprofit, 5)
                stoploss = round(stoploss,5)
                oanda.place_order(instrument,round(position_size),entry,round(stoploss,5),round(takeprofit,5))

                
                with open("trade_history.csv","a") as file:
                    file.write(f"\n{datetime.now()},{entry},{position_size},{takeprofit},{stoploss}")
                
                print(f"New order placed. Entry: {entry}, Qty: {position_size}, TakeProfit : {takeprofit}, StopLost: {stoploss}")
                
            else:
                print("\rNo trade condition....waiting next candle...", end = "")
        
        # Sleep time based on the timeframe
        time.sleep(60)


if __name__ == "__main__" :
    automated_trading_loop()