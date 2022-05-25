import MetaTrader5 as mt5
import pandas as pd
import statistics as stats
from pylab import *



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
        return datos
        print("{}, Precio = {}, Media = {}, NO HAY ENTRADA(Una_signal) ".format(datos.index[-1],datos.close[-1],round(datos.media20[-1],2)))

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
        # show()


        # # GRAFICO 2
        # datos[["close", "media200"]].plot(figsize=(20, 7))
        # twinx()
        # datos.diferencia.plot(color="red")
        # show()

        # GRAFICO 3
        datos[["close", "media200"]].plot()
        plot(datos.loc[datos.posicion_buy == 1].index, datos.close[datos.posicion_buy == 1], '^', markersize=7, color="g", label="buy")
        plot(datos.loc[datos.posicion_sell == 1].index, datos.close[datos.posicion_sell == 1], 'v', markersize=7, color="r", label="sell")
        show()
        return datos

    def RSI_signal(self):
        datos=self.Obtener_datos(symbol=symbol,temporalidad=16385,Nro_datos=1000)
        close=datos.close
        time_period = 20
        gain_history = []
        loss_history = []
        avg_gain_values = []
        avg_loss_values = []
        rsi_values = []
        last_price = 0

        for close_price in close:
            if last_price == 0:
                last_price = close_price
            gain_history.append(max(0, close_price - last_price))
            loss_history.append(max(0, last_price - close_price))
            last_price = close_price

            if len(gain_history) > time_period:
                del (gain_history[0])
                del (loss_history[0])
            #
            avg_gain = stats.mean(gain_history)
            avg_loss = stats.mean(loss_history)

            avg_gain_values.append(avg_gain)
            avg_loss_values.append(avg_loss)
            rs = 0
            if avg_loss > 0:
                rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)

        datos = datos.assign(ClosePrice=pd.Series(close,index=datos.index))
        datos = datos.assign(RelativeStrengthAvgGainOver20Days=pd.Series(avg_gain_values, index = datos.index))
        datos = datos.assign(RelativeStrengthAvgLossOver20Days=pd.Series(avg_loss_values, index = datos.index))
        datos = datos.assign(RelativeStrengthIndicatorOver20Days=pd.Series(rsi_values, index=datos.index))
        datos=datos.iloc[2:]
        close_price = datos['ClosePrice']
        rs_gain = datos['RelativeStrengthAvgGainOver20Days']
        rs_loss = datos['RelativeStrengthAvgLossOver20Days']
        rsi = datos['RelativeStrengthIndicatorOver20Days']
        limite_inferior = rsi.sort_values()[:1000].mean()
        limite_superior = rsi.sort_values()[-1000:].mean()

        datos["signal_buy"] = where(rsi<limite_inferior,1,0)
        datos["posicion_buy"] = datos.signal_buy.diff()

        datos["signal_sell"] = where(rsi < limite_inferior,1,0)

        datos["posicion_sell"] = datos.signal_sell.diff()
        print("{}, Precio = {}, NO HAY ENTRADA (RSI signal) ".format(datos.index[-1], datos.close[-1],))

        return datos
        # fig=figure()
        # ax1= fig.add_subplot(211, ylabel="{} precios".format(symbol))
        # close_price.plot(ax=ax1)
        # ax2= fig.add_subplot(212)
        # rsi.plot(ax=ax2)
        # #
        # ax2.hlines(limite_inferior, datos.index[0], datos.index[-1],color="g")
        # ax2.hlines(limite_superior, datos.index[0], datos.index[-1],color="red")
        # show()
        # fig = figure()
        # ax1 = fig.add_subplot(311, ylabel="{} precios".format(symbol))
        # close_price.plot(ax=ax1, color='black', lw=2., legend=True)
        # ax2 = fig.add_subplot(312, ylabel='RS')
        # rs_gain.plot(ax=ax2, color='g', lw=2., legend=True)
        # rs_loss.plot(ax=ax2, color='r', lw=2., legend=True)
        # ax3 = fig.add_subplot(313, ylabel='RSI')
        # rsi.plot(ax=ax3, color='b', lw=2., legend=True)
        # show()

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
            #Estrategia Una_signal()
            # datos_una = self.Una_signal()
            # self.Abrir_operaciones(datos=datos_una)

            #Estrategia Otra_signal()
            # datos_otra= self.Otra_signal()
            # self.Abrir_operaciones(datos=datos_otra)

            #Estrategia RSI-signal
            datos_rsi= self.RSI_signal()
            self.Abrir_operaciones(datos=datos_rsi)

            time.sleep(5 - datetime.datetime.now().microsecond / 1000000)

# Robot_medias_moviles().Obtener_datos(symbol=symbol)
# Robot_medias_moviles().Una_signal()
# Robot_medias_moviles().Otra_signal()
# Robot_medias_moviles().RSI_signal()
Robot_medias_moviles().robot_handler()




#diccionario_temporalidades
# {'mt5.TIMEFRAME_D1': 16385, 'mt5.TIMEFRAME_H1': 16408, 'mt5.TIMEFRAME_H12': 16396, 'mt5.TIMEFRAME_H2': 16386, 'mt5.TIMEFRAME_H3': 16387, 'mt5.TIMEFRAME_H4': 16388, 'mt5.TIMEFRAME_H6': 16390, 'mt5.TIMEFRAME_H8': 16392, 'mt5.TIMEFRAME_M1': 1, 'mt5.TIMEFRAME_M10': 10, 'mt5.TIMEFRAME_M12': 12, 'mt5.TIMEFRAME_M15': 15, 'mt5.TIMEFRAME_M2': 2, 'mt5.TIMEFRAME_M20': 20, 'mt5.TIMEFRAME_M3': 3, 'mt5.TIMEFRAME_M30': 30, 'mt5.TIMEFRAME_M4': 4, 'mt5.TIMEFRAME_M5': 5, 'mt5.TIMEFRAME_M6': 6, 'mt5.TIMEFRAME_MN1': 49153, 'mt5.TIMEFRAME_W1': 32769}