import tkinter as tk
from tkinter import ttk
import MetaTrader5 as mt5
from pylab import *
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


mis_simbolos_test =["EURUSD","GBPJPY","AUDJPY","EURJPY","CHFJPY","CADJPY","USDJPY"]
mt5.initialize()

class Robot_minuto_exacto():

    def Abrir_operaciones(self):
        for x in mis_simbolos_test:
            symbol =x
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "type": mt5.ORDER_TYPE_BUY,
                "volume": 0.01,
                "price": mt5.symbol_info_tick(symbol).ask,
                "comment": "TRUErobot_minuto_",
                "type_filling": mt5.ORDER_FILLING_IOC
            }

            result = mt5.order_send(request)

            print("Orden Compra en {}".format(symbol))
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("ERROR: {} ".format(result.comment))

    def Cerrar_operaciones(self):

        posiciones_abiertas=pd.DataFrame(list(mt5.positions_get()),columns=mt5.positions_get()[0]._asdict().keys()).set_index("symbol",drop=False)
        para_cerrar=posiciones_abiertas[posiciones_abiertas.comment=="TRUErobot_minuto_"]

        for nro_ in range(len(para_cerrar)):
            symbol = para_cerrar.symbol[nro_]
            position_id = int(para_cerrar.ticket[nro_])
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol ,
                "volume": 0.01,
                "type": mt5.ORDER_TYPE_SELL,
                "position": position_id,
                "price": mt5.symbol_info_tick(symbol).bid,
                "comment": "python script close",
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            # enviamos la solicitud comercial
            result = mt5.order_send(request)
            print("Se cerro la posicion #{} en {} ".format(position_id,symbol))
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("ERROR: {} ".format(result.comment))

    def robot_handler(self,minuto_entrada=55,minuto_salida=15):

        while True:
            ahora = int(datetime.datetime.now().strftime("%M"))
            print("Ahora es el minuto:",ahora)

            if ahora ==minuto_entrada:
                print("\u2663"*20)
                print("BUENA SUERTE!!!!")
                print("\u2663" * 20)
                self.Abrir_operaciones()
            else:
                if minuto_entrada-ahora<0:
                    minutos_que_faltan=60+ minuto_entrada-ahora
                else:
                    minutos_que_faltan = minuto_entrada - ahora
                print("""     
              |    |    |                 
             )_)  )_)  )_)              
            )___))___))___)\            
           )____)____)_____)
         _____|____|____|___\>
  -------\ Faltan {} minutos /-----------------------------------------------------------
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    """.format(minutos_que_faltan))
            if ahora ==minuto_salida:
                try:

                    self.Cerrar_operaciones()

                except:
                    exit()
            time.sleep(60)

    def backtest_consola(self):

        def _quit(): #para cerrar luego
            ventana.quit()
            ventana.destroy()

        ventana=tk.Tk()
        ventana.geometry("400x250")
        ventana.title("Backtest, robot_minutos")


        simbolos = []
        for x in mt5.symbols_get():

            simbolos.append(x.name)


        label_seleccione_simbolo = tk.Label(ventana,text="Seleccione un simbolo").grid(column=0,row=0)

        combo_simbolos= ttk.Combobox(ventana,values=simbolos,width=10)
        combo_simbolos.current(1)
        combo_simbolos.grid(column=0,row=1)

        label_seleccione_entrada = tk.Label(ventana, text="Minuto Entrada").grid(column=0, row=2)
        combo_min_entrada= ttk.Combobox(ventana,values=list(range(0,60,5)),width=2)
        combo_min_entrada.current(1)
        combo_min_entrada.grid(column=0,row=3)
        label_seleccione_salida = tk.Label(ventana, text="Minuto Cierre").grid(column=0, row=4)
        combo_min_cierre = ttk.Combobox(ventana, values=list(range(0,60,5)), width=2)
        combo_min_cierre.current(2)
        combo_min_cierre.grid(column=0, row=5)


        def el_boton_hace():
            data = pd.DataFrame(mt5.copy_rates_from_pos(combo_simbolos.get(), mt5.TIMEFRAME_M5, 0, 50000)[["time", "close"]]).set_index("time")
            data.index = pd.to_datetime(data.index, unit='s')
            fechas = data.index

            minuto_entrada=str(combo_min_entrada.get())
            minuto_cierre=str(combo_min_cierre.get())

            data["signal"] = np.where(fechas.strftime("%M") == minuto_entrada, 1,  ###compra
                                      np.where(fechas.strftime("%M") == minuto_cierre, -1, 0))  ###venta


            signal=data.close*data.signal
            posicion = signal.apply(np.sign)
            retornos = data.close.apply(np.log).diff()
            mis_retornos =(posicion.shift(1) * retornos)
            plot_returns = round(mis_retornos.cumsum().apply(np.exp) * 100, 2)

            fig = Figure(figsize=(5, 5),dpi=50)
            plot_backtest = fig.add_subplot(111)
            plot_backtest.plot(plot_returns)
            canvas = FigureCanvasTkAgg(fig,master=ventana)
            canvas.draw()
            canvas.get_tk_widget().place(x=140,y=0)


        boton_backtest=tk.Button(ventana,text="INICIO",command=el_boton_hace).grid(column=0,row=6,pady=10)

        ventana.protocol("WM_DELETE_WINDOW", _quit)
        ventana.mainloop()

Robot_minuto_exacto().robot_handler(minuto_entrada=5,minuto_salida=10)
# Robot_minuto_exacto().backtest_consola()