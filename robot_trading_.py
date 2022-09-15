import MetaTrader5 as mt5
import pandas as pd
import time
import datetime


name = 67042877
key = "Genttly.2022"
serv = "RoboForex-ECN"
path = r"C:\Program Files\MetaTrader 5\terminal64.exe"
symbolos = "EURUSD"

class Robot_trading():
    def obtener_datos(self):
        mt5.initialize(login=name, server=serv, password=key, path=path)
        tasas = mt5.copy_rates_from_pos(symbolos, mt5.TIMEFRAME_H1, 0, 9999)
        tabla = pd.DataFrame(tasas)
        tabla['time'] = pd.to_datetime(tabla['time'], unit='s')
        return tabla

    def abrir_operaciones(self, symbol, lotaje=0.01):

        tabla =pd.DataFrame(self.obtener_datos())
        soporte=tabla["low"][-24:].mean()  ## promedio lows de las ultimas 24horas
        resistencia = tabla["high"][-24:].mean() ##promedio highs las ultimas 24 hora

        ultimo_close=tabla.iloc[-1].close

        if ultimo_close<soporte:   # COMPRAR si ultimo precio es menor soporte.
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "type": mt5.ORDER_TYPE_BUY,
                "volume": float(lotaje),
                "price": mt5.symbol_info_tick(symbol).ask,
                "comment": "CODIGO_ELIANA",
                "type_filling": mt5.ORDER_FILLING_FOK
            }
            mt5.order_send(request)
            print("entro soporte")
        elif ultimo_close>resistencia: # VENDER si ultimo precio es mayor que resistencia.
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "type": mt5.ORDER_TYPE_SELL,
                "volume": float(lotaje),
                "price": mt5.symbol_info_tick(symbol).ask,
                "comment": "CODIGO_ELIANA",
                "type_filling": mt5.ORDER_FILLING_FOK
            }
            mt5.order_send(request)
            print("entro por resistencia")
        else:
            print("no hay entrada")

    def robot_handler(self,symbol):
        while True:
            self.abrir_operaciones(symbol)
            time.sleep(360 - datetime.datetime.now().microsecond / 1000000)






Robot_trading().robot_handler(symbolos)