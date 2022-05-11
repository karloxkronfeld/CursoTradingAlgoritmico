import MetaTrader5 as mt5
import pandas as pd
import time
from datetime import datetime


name = 	67042877
key = "Genttly.2022"
serv = "RoboForex-ECN"
path = r"C:\Program Files\MetaTrader 5\terminal64.exe"
symbolos="XAUUSD"

class Algo_Trading_Udea():
    def obtener_datos(self, symbol, name, serv, key, path):
        mt5.initialize(login=name, server=serv, password=key, path=path)

        tasas_m1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 100)
        tabla_tasas_m1 = pd.DataFrame(tasas_m1)
        tabla_tasas_m1['time'] = pd.to_datetime(tabla_tasas_m1['time'], unit='s')

        return tabla_tasas_m1

    def calcular_lotaje(self, lotaje_inicial: float, tabla_tasas_m1):

        tabla_tasas_m1['rezago_precio1'] = tabla_tasas_m1['close'].shift()
        tabla_tasas_m1['perc_diferencia'] = (tabla_tasas_m1['close'] - tabla_tasas_m1['rezago_precio1']) / \
                                            tabla_tasas_m1['close']
        ultima_diferencia = tabla_tasas_m1['perc_diferencia'].iloc[99]

        try:
            open_pos = mt5.positions_get()
            df_open_positions = pd.DataFrame(list(open_pos), columns=open_pos[0]._asdict().keys())
            num_operaciones = len(df_open_positions)

        except:
            num_operaciones = 0

        if (ultima_diferencia > 0) and (num_operaciones == 0):
            volumen = lotaje_inicial
        elif (ultima_diferencia > 0) and (num_operaciones > 0):
            volumen = round(lotaje_inicial * (1.1 + ultima_diferencia), 2)
        else:
            volumen = lotaje_inicial

        return volumen

    def abrir_operaciones(self, symbol, tabla_tasas_m1, lotaje_inicial):
        tabla_tasas_m1['rezago_precio1'] = tabla_tasas_m1['close'].shift()
        tabla_tasas_m1['diferencia'] = tabla_tasas_m1['close'] - tabla_tasas_m1['rezago_precio1']
        ultima_diferencia = tabla_tasas_m1['diferencia'].iloc[99]

        if ultima_diferencia > 0:
            # lot = calcular_lotaje(1.0,tabla_tasas_m1)
            lot = self.calcular_lotaje(0.01, tabla_tasas_m1)

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "type": mt5.ORDER_TYPE_SELL,
                "volume": float(lot),
                "price": mt5.symbol_info_tick(symbol).ask,
                "tp": mt5.symbol_info_tick(symbol).ask + 0.0002,
                "comment": 'Cod prueba2',
                "type_filling": mt5.ORDER_FILLING_FOK
            }

            mt5.order_send(request)

    def robot_handler(self):
        while True:
            tabla_tasas_m1 = self.obtener_datos('XAUUSD', name, serv, key, path)
            self.abrir_operaciones('XAUUSD', tabla_tasas_m1, 0.01)

            time.sleep(60 - datetime.now().microsecond / 1000000)



Algo_Trading_Udea().robot_handler()