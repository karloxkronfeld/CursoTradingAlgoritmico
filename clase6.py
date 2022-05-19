from talib import RSI
from talib import ATR

symbol = 'Boom 1000 Index'
mt5.initialize(login = name, server = serv, password = key, path = path)
tasas_m1 = mt5.copy_rates_from_pos(symbol,mt5.TIMEFRAME_M30,0,99000)
tabla_tasas_m1 = pd.DataFrame(tasas_m1)

tabla_tasas_m1['RSI'] = RSI(tabla_tasas_m1['close'])
tabla_tasas_m1['atipico_compra'] = np.where(tabla_tasas_m1['RSI']<(tabla_tasas_m1['RSI'].mean()-3*tabla_tasas_m1['RSI'].std()),1,0)
tabla_tasas_m1['RSI'].hist()


