
# K Means para construir soportes y resistencias
symbol = 'EURUSD'
mt5.initialize(login = name, server = serv, password = key, path = path)
tasas_m1 = mt5.copy_rates_from_pos(symbol,mt5.TIMEFRAME_M1,0,500)
tabla_tasas_m1 = pd.DataFrame(tasas_m1)

tabla_tasas_m1['rounded_close'] = round(tabla_tasas_m1['close'],3)
tabla_tasas_m1['rounded_open'] = round(tabla_tasas_m1['open'],3)
tabla_tasas_m1['rounded_high'] = round(tabla_tasas_m1['high'],3)
tabla_tasas_m1['rounded_low'] = round(tabla_tasas_m1['low'],3)
tabla_tasas_m1['diff_from_rounded_close'] = abs(tabla_tasas_m1['close'] - tabla_tasas_m1['rounded_close'])
tabla_tasas_m1['diff_from_rounded_open'] = tabla_tasas_m1['open'] - tabla_tasas_m1['rounded_open']
tabla_tasas_m1['diff_from_rounded_high'] = tabla_tasas_m1['high'] - tabla_tasas_m1['rounded_high']
tabla_tasas_m1['diff_from_rounded_low'] = tabla_tasas_m1['low'] - tabla_tasas_m1['rounded_low']

series_close = tabla_tasas_m1['rounded_close']
prices_list = series_close.tolist()

import collections

freq_close = collections.Counter(prices_list)
my_dict1 = dict(freq_close)
df = pd.DataFrame(list(my_dict1.items()), columns = ['precio','frecuencia'])
df_ordered = df.sort_values(['precio','frecuencia'], ascending = [True,False])
avg_desv_close = tabla_tasas_m1['diff_from_rounded_close'].mean()

df_ordered['rango_inferior'] = df_ordered['precio'] - avg_desv_close
df_ordered['rango_superior'] = df_ordered['precio'] + avg_desv_close

# Introducir el concepto de Pickle

import pickle

filename = 'modelo_k_means.sav'
pickle.dump(km_model,open(filename,'wb'))

model_loaded = pickle.load(open(filename,'rb'))

# Patrones de velas


#Dojis

symbol = 'EURUSD'
mt5.initialize(login = name, server = serv, password = key, path = path)
tasas_m1 = mt5.copy_rates_from_pos(symbol,mt5.TIMEFRAME_H4,0,99000)
tabla_tasas_m1 = pd.DataFrame(tasas_m1)

tabla_tasas_m1['body'] = tabla_tasas_m1['close'] - tabla_tasas_m1['open']
tabla_tasas_m1['mecha_abajo'] = np.where(tabla_tasas_m1['body'] > 0,tabla_tasas_m1['open'] - tabla_tasas_m1['low'],tabla_tasas_m1['close'] - tabla_tasas_m1['low'])
tabla_tasas_m1['mecha_arriba'] = np.where(tabla_tasas_m1['body'] > 0,tabla_tasas_m1['high'] - tabla_tasas_m1['close'], tabla_tasas_m1['high'] - tabla_tasas_m1['open'])

tabla_tasas_m1['doji'] = np.where(((tabla_tasas_m1['mecha_abajo'])/abs(tabla_tasas_m1['body']) > 3) & ((tabla_tasas_m1['mecha_arriba']/abs(tabla_tasas_m1['body'])) > 3),1,0 )
tabla_tasas_m1['hammer_up'] = np.where(((tabla_tasas_m1['mecha_abajo'])/abs(tabla_tasas_m1['body']) > 3) & (tabla_tasas_m1['doji'] != 1),1,0 )
tabla_tasas_m1['hammer_dw'] = np.where(((tabla_tasas_m1['mecha_arriba'])/abs(tabla_tasas_m1['body']) > 3) & (tabla_tasas_m1['doji'] != 1),1,0 )