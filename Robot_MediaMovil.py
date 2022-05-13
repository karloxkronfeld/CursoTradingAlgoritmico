import MetaTrader5 as mt5
import pandas as pd
import time

import numpy as np
import statistics
from pylab import *

name = 	67042877
key = "Genttly.2022"
serv = "RoboForex-ECN"
path = r"C:\Program Files\MetaTrader 5\terminal64.exe"
symbol="XAUUSD"

mt5.initialize(login=name, server=serv, password=key, path=path)

class Robot_medias_moviles():

    def Obtener_datos(self, symbol,temporalidad=15,Nro_datos=100):
        datos = pd.DataFrame(mt5.copy_rates_from_pos(symbol,temporalidad,0,Nro_datos))[["time","close"]].set_index("time")
        datos.index = pd.to_datetime(datos.index, unit='s')
        return datos

    def Una_signal(self):
        datos = self.Obtener_datos(symbol,temporalidad=1,Nro_datos=300)
        datos["media20"]=datos.close.rolling(20).mean()
        datos["diff_media"] = datos.media20.diff()
        datos["signal_buy"] = np.where((datos.close >= datos.media20) & (datos.diff_media > 0), 1, 0)
        datos["posicion_buy"] = datos.signal_buy.diff()
        datos["signal_sell"] = np.where((datos.close <= datos.media20) & (datos.diff_media < 0), 1, 0)
        datos["posicion_sell"] = datos.signal_sell.diff()
        datos_signal=datos
        print("{}, Precio = {}, Media = {}, NO HAY ENTRADA(Una_signal) ".format(datos.index[-1],datos.close[-1],round(datos.media20[-1],2)))

        return datos_signal

    def Otra_signal(self):
        datos= self.Obtener_datos(symbol=symbol,temporalidad=30,Nro_datos=2000)
        datos["media200"] = datos.close.rolling(200).mean().fillna(method="bfill")
        datos["diferencia"] = datos.media200 - datos.close
        limite_inferior = datos.diferencia.sort_values()[:100].mean()  # TOP CIEN DE LAS DIFERENCIAS
        limite_superior = datos.diferencia.sort_values()[-100:].mean()
        datos["signal_buy"] = where(datos.diferencia>limite_superior,1,0)
        datos["posicion_buy"]= datos.signal_buy.diff()
        datos["signal_sell"] = where(datos.diferencia < limite_inferior, 1, 0)
        datos["posicion_sell"] = datos.signal_sell.diff()

        datos_signal=datos
        print("{}, Precio = {}, NO HAY ENTRADA(Otra_signal) ".format(datos.index[-1], datos.close[-1]))

        # #GRAFICO 1
        # f, (ax1, ax2) = subplots(2, 1, sharex=True, figsize=(19, 8))
        # ax1.plot(datos.iloc[:, [0, 1]])
        # ax1.legend(["close","media200"])
        # ax2.plot(datos.diferencia.iloc[:])
        # ax2.hlines(limite_inferior, datos.index[0], datos.index[-1],color="red")
        # ax2.hlines(limite_superior, datos.index[0], datos.index[-1],color="green")
        # ax2.legend(["Dif. Media Precio","Lim Inf","Lim Sup"])
        # xticks(rotation=50)

        # GRAFICO 2
        # datos[["close", "media200"]].plot(figsize=(20, 7))
        # twinx()
        # datos.diferencia.plot(color="red")
        # show()

        # GRAFICO 3
        # datos[["close", "media200"]].plot()
        # plot(datos.loc[datos.posicion_buy == 1].index, datos.close[datos.posicion_buy == 1], '^', markersize=7, color="g", label="buy")
        # plot(datos.loc[datos.posicion_sell == 1].index, datos.close[datos.posicion_sell == 1], 'v', markersize=7, color="r", label="sell")
        # show()
        return datos_signal

    def Abrir_operaciones(self, datos, lote=0.01):

        ultimo_dato=datos.iloc[-1]

        if ultimo_dato.posicion_buy == 1:
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "type": mt5.ORDER_TYPE_BUY,
                "volume": lote,
                "price": mt5.symbol_info_tick(symbol).ask,
                "comment": "Cañola_Medias",
                "type_filling": mt5.ORDER_FILLING_FOK
            }

            result = mt5.order_send(request)

            print("Orden Compra enviada en {} al precio {} ".format(symbol,datos.close[-1]));
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("ERROR: {} ".format(result.comment))

        elif ultimo_dato.posicion_sell ==1:
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "type": mt5.ORDER_TYPE_SELL,
                "volume": lote,
                "price": mt5.symbol_info_tick(symbol).bid,
                "comment": "Cañola_Medias",
                "type_filling": mt5.ORDER_FILLING_FOK
            }
            result = mt5.order_send(request)

            print("Orden Venta enviada en {}".format(symbol));
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("ERROR: {} ".format(result.comment))

    def robot_handler(self):
        while True:
            datos_una = self.Una_signal()
            self.Abrir_operaciones(datos=datos_una)
            # datos_otra= self.Otra_signal()
            # self.Abrir_operaciones(datos=datos_otra)

            time.sleep(5 - datetime.datetime.now().microsecond / 1000000)



Robot_medias_moviles().robot_handler()



#diccionario_temporalidades
# {'mt5.TIMEFRAME_D1': 16385, 'mt5.TIMEFRAME_H1': 16408, 'mt5.TIMEFRAME_H12': 16396, 'mt5.TIMEFRAME_H2': 16386, 'mt5.TIMEFRAME_H3': 16387, 'mt5.TIMEFRAME_H4': 16388, 'mt5.TIMEFRAME_H6': 16390, 'mt5.TIMEFRAME_H8': 16392, 'mt5.TIMEFRAME_M1': 1, 'mt5.TIMEFRAME_M10': 10, 'mt5.TIMEFRAME_M12': 12, 'mt5.TIMEFRAME_M15': 15, 'mt5.TIMEFRAME_M2': 2, 'mt5.TIMEFRAME_M20': 20, 'mt5.TIMEFRAME_M3': 3, 'mt5.TIMEFRAME_M30': 30, 'mt5.TIMEFRAME_M4': 4, 'mt5.TIMEFRAME_M5': 5, 'mt5.TIMEFRAME_M6': 6, 'mt5.TIMEFRAME_MN1': 49153, 'mt5.TIMEFRAME_W1': 32769}