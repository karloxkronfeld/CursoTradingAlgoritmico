import MetaTrader5 as mt5
import pandas as pd
import time
from datetime import datetime



# MeanFollowing
symbol = 'EURUSD'
tasas_m1 = mt5.copy_rates_from_pos(symbol,mt5.TIMEFRAME_M15,0,99000)
tabla_tasas_m1 = pd.DataFrame(tasas_m1)
tabla_tasas_m1['time'] = pd.to_datetime(tabla_tasas_m1['time'],unit = 's')
tabla_tasas_m1['ma15'] = tabla_tasas_m1['close'].rolling(15).mean()
tabla_tasas_m1['diff_ma15'] = tabla_tasas_m1['ma15'] - tabla_tasas_m1['ma15'].shift()
tabla_tasas_m1['senial_c_l'] = np.where( (tabla_tasas_m1['close'] >= tabla_tasas_m1['ma15']) & (tabla_tasas_m1['diff_ma15']>0),'Buy','')
tabla_tasas_m1['senial_s'] = np.where( (tabla_tasas_m1['close'] <= tabla_tasas_m1['ma15']) & (tabla_tasas_m1['diff_ma15']>0),'Buy','')


# Mean Reversion
symbol = '.USTECHCash'
tasas_m1 = mt5.copy_rates_from_pos(symbol,mt5.TIMEFRAME_M15,0,99000)
tabla_tasas_m1 = pd.DataFrame(tasas_m1)
tabla_tasas_m1['time'] = pd.to_datetime(tabla_tasas_m1['time'],unit = 's')
tabla_tasas_m1['ma15'] = (tabla_tasas_m1['close'].rolling(30).mean())**(1/2)
tabla_tasas_m1['d1_ma15'] = (tabla_tasas_m1['ma15'] - tabla_tasas_m1['ma15'].shift())
tabla_tasas_m1['d2_ma15'] = tabla_tasas_m1['d1_ma15'] - tabla_tasas_m1['d1_ma15'].shift()
tabla_tasas_m1['signal'] = np.where( (( tabla_tasas_m1['d1_ma15'] < (tabla_tasas_m1['d1_ma15'].std())/2  ) & ( tabla_tasas_m1['d1_ma15'] < (tabla_tasas_m1['d1_ma15'].std())/2  )) & (tabla_tasas_m1['d2_ma15'] < 0),'Sell','')
