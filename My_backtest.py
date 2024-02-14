import MetaTrader5 as mt5
import pandas as pd
from pylab import *
pd.set_option('display.max_rows', None,)


mt5.initialize()

simbolo="EURUSD"
def backtest_unSimbol():

    datos=pd.DataFrame(mt5.copy_rates_from_pos(simbolo,mt5.TIMEFRAME_H4,0,24000))[["close","time"]].set_index("time")
    datos.index=pd.to_datetime(datos.index,unit="s")



    datos["signal"]=[0,1,0,0,-1,0]*4000
    print(datos)
    datos["multiplicacion"]=datos.close*datos.signal
    # print(datos)
    retornos_simbol=datos.close.apply(np.log).diff()
    # print(retornos_simbol)
    mis_retornos = datos.signal.shift(1)*retornos_simbol
    mis_retornos_Acum=round(mis_retornos.cumsum().apply(np.exp),2)
    mis_retornos_Acum.plot()

    show()
    return mis_retornos

# datos=pd.DataFrame(backtest_unSimbol(),columns=["beneficio"])
#
# datos["ganadora"]=where(datos.beneficio>0,1,0)
# media=datos.ganadora.mean()
#
#
# winners= datos[datos.ganadora==1]
# losers= datos[datos.ganadora==0]
#
# SL= losers.beneficio.mean()
# TP= winners.beneficio.mean()
#
# b= TP/abs(SL)
#
# p_min = 1/(1+b)
#
#
# print(f"Odds: {b:.2f}")
# print(f"p_min: {p_min:.2f}")
#
# datos["estado_cuenta"]=datos.beneficio
# datos["cum_sum"]=datos.beneficio.cumsum()
# window = 30
#
# roll_max = datos.estado_cuenta.rolling(window,min_periods=5).max()
# drowdown = (datos.estado_cuenta / roll_max)
#
# max_drowdown = drowdown.rolling(window,min_periods=5).mean().min()
# print(max_drowdown)
# datos.cum_sum.plot(label=simbolo)
# legend()
#
# show()



my_symbols=["EURAUD","EURUSD", "USDCAD","USDCHF","EURGBP","EURNZD",
              "GBPJPY","AUDJPY","NZDJPY","EURJPY","CHFJPY","CADJPY","USDJPY",]

def backtest_variosSimbolos(symbol):
    data = []
    for x in symbol:
        data.append(
            pd.DataFrame(mt5.copy_rates_from_pos(x, mt5.TIMEFRAME_H4    , 0, 4662)[["time", "close"]]).set_index("time"))
    data = pd.concat(data, axis=1).dropna()
    data.columns = symbol
    data.index = pd.to_datetime(data.index, unit='s')


    data["signal"] = [0, 1, 0, 0, -1, 0] * 777
    signal= (data[symbol].T * data.signal).T

    posicion= signal.apply(np.sign)
    retornos_simbolos=data[symbol].apply(np.log).diff(1)
    mis_retornos= posicion.shift(1)*retornos_simbolos

    mis_retornos_acum= round(mis_retornos.cumsum().apply(np.exp)*100,2)
    print(mis_retornos_acum.iloc[-1].sort_values(ascending=False))
    mis_retornos_acum.plot()
    for x in mis_retornos_acum:
        text(mis_retornos_acum.index[-1], mis_retornos_acum[x].iloc[-1], f"{x}:{mis_retornos_acum[x].iloc[-1]:.2f}")

    print(f"Esto comenzo {data.index[0]}")
    show()

# backtest_variosSimbolos(my_symbols)
backtest_unSimbol()

