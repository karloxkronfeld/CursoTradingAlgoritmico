import MetaTrader5 as mt5
import numpy as np
import pandas as pd

name = 	67042877
key = "Genttly.2022"
serv = "RoboForex-ECN"
path = r"C:\Program Files\MetaTrader 5\terminal64.exe"
symbolos="EURUSD"

mt5.initialize(login=name,server=serv,password=key,path=path)
tasas= mt5.copy_rates_from_pos(symbolos,mt5.TIMEFRAME_M1,0,99999)
tabla=pd.DataFrame(tasas)
tabla['time'] = pd.to_datetime(tabla['time'], unit='s')

# ticks =  mt5.copy_ticks_from(simbolos, datetime(2022, 3, 31, 19), 100000000, mt5.COPY_TICKS_ALL)  #año,mes,dia,hora
print(tabla)
