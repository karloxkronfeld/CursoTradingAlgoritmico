import tkinter as tk
from tkinter import ttk
import MetaTrader5 as mt5
import pandas as pd
import statistics as stats
from pylab import *


name = 	67042877
key = "Genttly.2022"
serv = "RoboForex-ECN"
path = r"C:\Program Files\MetaTrader 5\terminal64.exe"

class Robots_():
    mt5.initialize(login=name, server=serv, password=key, path=path)
    def Obtener_datos(self, symbol,temporalidad=15,Nro_datos=100):
        datos = pd.DataFrame(mt5.copy_rates_from_pos(symbol,temporalidad,0,Nro_datos))[["time","close"]].set_index("time")
        datos.index = pd.to_datetime(datos.index, unit='s')
        return datos

    def Una_signal(self,symbol,temporalidad):


        datos = self.Obtener_datos(symbol,temporalidad=temporalidad,Nro_datos=300)


        datos["media20"]=datos.close.rolling(20).mean()
        # datos["diff_media"] = datos.media20.diff()
        # datos["signal_buy"] = np.where((datos.close >= datos.media20) & (datos.diff_media > 0), 1, 0)
        # print(datos)
        # datos["posicion_buy"] = datos.signal_buy.diff()
        # datos["signal_sell"] = np.where((datos.close <= datos.media20) & (datos.diff_media < 0), 1, 0)
        # datos["posicion_sell"] = datos.signal_sell.diff()

        print("{}, Precio = {}, Media = {}, NO HAY ENTRADA(Una_signal) ".format(datos.index[-1],datos.close[-1],round(datos.media20[-1],2)))

    def Otra_signal(self,symbol):
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

    def RSI_signal(self,symbol):
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

    def Abrir_operaciones(self, symbol, temporalidad, datos, lote=0.01):

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

    def robot_handler(self,symbol,temporalidad,esta_apagado):

        contador=0
        while not esta_apagado:

            #Estrategia Una_signal()
            datos_una = self.Una_signal(symbol,temporalidad)

            # self.Abrir_operaciones(datos=datos_una,symbol=symbol,temporalidad=temporalidad)

            #Estrategia Otra_signal()
            # datos_otra= self.Otra_signal()
            # self.Abrir_operaciones(datos=datos_otra)

            #Estrategia RSI-signal
            # datos_rsi= self.RSI_signal()
            # self.Abrir_operaciones(datos=datos_rsi)

            contador+=1
            time.sleep(1 - datetime.datetime.now().microsecond / 1000000)
            if contador==4:
                esta_apagado=True
                # esta_apagado=False



ventana = tk.Tk()
ventana.geometry("450x250")
ventana.title("Consola estrategias trading")
label______ = tk.Label(ventana,text="_________").grid(row=0,sticky="w")

label_temporalidad = tk.Label(ventana,text="Temporalidades   ").grid(row=1,sticky="w")
valor_temporalidad=tk.IntVar()
temp_1= tk.Radiobutton(ventana, text='1M',variable=valor_temporalidad, value=0,indicatoron=0).grid(column=1,row=1)
temp_5= tk.Radiobutton(ventana, text='5M',variable=valor_temporalidad, value=1,indicatoron=0).grid(column=2,row=1)
temp_15= tk.Radiobutton(ventana, text='15M',variable=valor_temporalidad, value=2,indicatoron=0).grid(column=3,row=1)
temp_1h= tk.Radiobutton(ventana, text='1H',variable=valor_temporalidad, value=3,indicatoron=0).grid(column=4,row=1)

label_simbolos= tk.Label(ventana,text="Lista de simbolos").grid(row=2,sticky="w")
simbolos=[]
for x in mt5.symbols_get():
    simbolos.append(x.name)
lista_simbolos_combo=tk.ttk.Combobox(values=simbolos) #lista de simbolos disponibles en mt5
lista_simbolos_combo.current(0) #default el primer simbolo
lista_simbolos_combo.grid(column=2,row=2,columnspan=7)


label_estrategia= tk.Label(ventana,text="Estrategias").grid(pady=5,sticky="w")
estrategia1=tk.IntVar()
estrategia2=tk.IntVar()
estrategia3=tk.IntVar()
estrategia1_check= tk.Checkbutton(ventana,text="Medias",variable=estrategia1).grid(sticky="w")
estrategia2_check= tk.Checkbutton(ventana,text="Mean Reversion",variable=estrategia2).grid(sticky="w")
estrategia3_check= tk.Checkbutton(ventana,text="RSI ",variable=estrategia3).grid(sticky="w")


esta_apagado=True
label_on_off= tk.Label(ventana,text="Esta esta_apagado",fg="red")
label_on_off.grid(column=10,row=3)

def switch():

    global esta_apagado

    if esta_apagado:
        boton_encendido.config(image=on)

        label_on_off.config(text="ENCENDIDO \n buena suerte!",fg="green")
        esta_apagado=False
        symbol = lista_simbolos_combo.get()
        temporality = valor_temporalidad.get()
        una_lista_temp = [1, 5, 15, 16385]
        temporalidad = una_lista_temp[temporality]
        estrategia = [estrategia1.get(), estrategia2.get(), estrategia3.get()]
        lista_estrategias = ["medias", "mean", "rsi"]
        lista_estrategias_print = []

        Robots_().robot_handler(symbol,temporalidad,esta_apagado)


    else:
        boton_encendido.config(image=off)
        label_on_off.config(text="APAGADO",fg="RED")
        esta_apagado=True




off=tk.PhotoImage(file="off.png")
on=tk.PhotoImage(file="on.png")
boton_encendido=tk.Button(ventana, image=off,bd=0,command=lambda :[switch()])
boton_encendido.grid(column=10,row=2,ipady=1,padx=50)

#

        #
        # for x in range(len(estrategia)):
        #     if estrategia[x] == 1:
        #         lista_estrategias_print.append(lista_estrategias[x])
        #
        # print("===\nTemporalidad : {}, \n"
        #       "Activo : {}, \n"
        #       "las estrategias son: {}".format(una_lista_temp[temporality], symbol, lista_estrategias_print))
        # return symbol, temporality


ventana.mainloop()

quit()

# Robot_medias_moviles().Obtener_datos(symbol=symbol)
# Robot_medias_moviles().Una_signal()
# Robot_medias_moviles().Otra_signal()
# Robot_medias_moviles().RSI_signal()
# Robot_medias_moviles().robot_handler()



