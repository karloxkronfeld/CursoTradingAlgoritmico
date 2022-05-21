#indicador super trend

import pandas as pd
import numpy as np


class supertrend_ind:

    def true_range(self, data: pd.DataFrame):
        data['previous_close'] = data['close'].shift(1)
        data['high-low'] = abs(data['high'] - data['low'])
        data['high-pc'] = abs(data['high'] - data['previous_close'])
        data['low-pc'] = abs(data['low'] - data['previous_close'])

        tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)

        return tr

    def atr(self, data: pd.DataFrame, period: int):
        data['tr'] = self.true_range(data)
        avtr = data['tr'].rolling(period).mean()

        return avtr

    def supertrend(self, df: pd.DataFrame, period=7, atr_multiplier=3):
        hl2 = (df['high'] + df['low']) / 2
        df['atr'] = self.atr(df, period)
        df['upperband'] = hl2 + (atr_multiplier * df['atr'])
        df['lowerband'] = hl2 - (atr_multiplier * df['atr'])
        df['in_uptrend'] = True

        for current in range(1, len(df.index)):
            previous = current - 1

            if df['close'][current] > df['upperband'][previous]:
                df['in_uptrend'][current] = True
            elif df['close'][current] < df['lowerband'][previous]:
                df['in_uptrend'][current] = False
            else:
                df['in_uptrend'][current] = df['in_uptrend'][previous]

                if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                    df['lowerband'][current] = df['lowerband'][previous]

                if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                    df['upperband'][current] = df['upperband'][previous]

        return df


from indicador_supertrend import supertrend_ind

st = supertrend_ind()

path = r'C:\Program Files\MetaTrader 5\terminal64.exe'#Ubicación de la terminal de MT5
# name = 3998980
# key = "Inup.2021"
# serv = "Deriv-Demo"

symbol = 'XAUUSD'

mt5.initialize(login = name, server = serv, password = key, path = path)
tasas_m1 = mt5.copy_rates_from_pos(symbol,mt5.TIMEFRAME_H1,0,9000)
tabla_tasas_m1 = pd.DataFrame(tasas_m1)

dfst = st.supertrend(tabla_tasas_m1)

dfst['previous_trend'] = dfst['in_uptrend'].shift()
dfst['signal'] = np.where( (dfst['previous_trend'] == True) & (dfst['in_uptrend'] == False),'sell',
np.where((dfst['previous_trend'] == False) & (dfst['in_uptrend'] == True),'buy','')
)
dfst['time'] = pd.to_datetime(dfst['time'],unit = 's')

dfst[dfst['previous_trend'] != dfst['in_uptrend']]


buys = dfst[dfst['signal'] == 'buy']
sells = dfst[dfst['signal'] == 'sell']

buys_time = buys['time'].tolist()
resultados_compras = pd.DataFrame()

for i in buys_time:
    temp_buys = buys[buys['time'] == i]
    temp_sells = sells[sells['time'] > i]
    current_sell = temp_sells[temp_sells['time'] == temp_sells['time'].min()]
    temp_buys['exit_price'] = current_sell['close'].item()
    temp_buys['exit_time'] = current_sell['time'].item()
    resultados_compras = resultados_compras.append(temp_buys)

resultados_compras['diff_price'] = resultados_compras['exit_price'] - resultados_compras['close']
resultados_compras['aciertos'] = np.where(resultados_compras['diff_price'] > 0,1,0)

sells_time = sells['time'].tolist()
resultados_ventas = pd.DataFrame()

for i in sells_time:
    temp_sells = sells[sells['time'] == i]
    temp_buys = sells[sells['time'] > i]
    current_sell = temp_buys[temp_buys['time'] == temp_buys['time'].min()]
    temp_sells['exit_price'] = current_sell['close'].item()
    temp_sells['exit_time'] = current_sell['time'].item()
    resultados_ventas = resultados_ventas.append(temp_sells)

resultados_ventas['diff_price'] = resultados_ventas['exit_price'] - resultados_ventas['close']
resultados_ventas['aciertos'] = np.where(resultados_ventas['diff_price'] > 0,1,0)

full_results = resultados_compras.append(resultados_ventas)
full_results = full_results.sort_values('time',ascending = True)

full_results['sum_acumulada'] = full_results['diff_price'].cumsum()

full_results['sum_acumulada'].plot()