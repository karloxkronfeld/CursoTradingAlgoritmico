import MetaTrader5 as mt5
import pandas as pd
import statistics as stats

from pylab import *



pd.set_option('mode.chained_assignment',None)
pd.set_option('display.max_columns', 500,'display.width', 1000)


name = 	67042877
key = "Genttly.2022"
serv = "RoboForex-ECN"
path = r"C:\Program Files\MetaTrader 5\terminal64.exe"

temporalidad=16385
mt5.initialize(login=name, server=serv, password=key, path=path)

def simbolo_aleatorio():
    simbolos=[]
    for x in mt5.symbols_get():
        simbolos.append("{} {}".format(x.name,x.description))
    simbolo=choice(simbolos)  ###SYMBOLO ALEATORIO
    print(f"SELECCION \n{simbolo} ")
    simbolo=simbolo.split(sep=' ', maxsplit=1)[0]
    return simbolo

simbolo=simbolo_aleatorio()

# simbolo="EURUSD"

def RSI(datos):

    close = datos.close


    time_period = 400
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

    datos = datos.assign(ClosePrice=pd.Series(close, index=datos.index))
    datos = datos.assign(RelStrAvgGain=pd.Series(avg_gain_values, index=datos.index))
    datos = datos.assign(RelStrAvgLoss=pd.Series(avg_loss_values, index=datos.index))
    datos = datos.assign(RSI=pd.Series(rsi_values, index=datos.index))
    datos = datos.iloc[2:]
    close_price = datos['ClosePrice']
    rs_gain = datos["RelStrAvgGain"]
    rs_loss = datos['RelStrAvgLoss']
    rsi = datos['RSI']
    limite_inferior = rsi.sort_values()[:1000].mean()
    limite_superior = rsi.sort_values()[-1000:].mean()

    datos["signal"] = np.where(datos['RSI'] > limite_superior, 'sell', np.where(datos['RSI'] < limite_inferior, 'buy', ''))


    # print("{}, Precio = {}, NO HAY ENTRADA (RSI signal) ".format(datos.index[-1], datos.close[-1], ))

    return datos

def creacion_de_señales():
    precio= pd.DataFrame(mt5.copy_rates_from_pos(simbolo, temporalidad, 0, 1000))
    precio.time= pd.to_datetime(precio.time,unit="s")
    df_signal= RSI(precio)

    return df_signal

def graficar(datos):
    nro=100
    fig=figure()
    ax1= fig.add_subplot(211, ylabel="{} precios".format(simbolo))
    datos[0].close[nro:-nro].plot(ax=ax1)
    ax2= fig.add_subplot(212)
    datos[0].RSI[nro:-nro].plot(ax=ax2)
    # #

    ax2.hlines(datos[1], datos[0].index[0], datos[0].index[-1],color="g")
    ax2.hlines(datos[2], datos[0].index[0], datos[0].index[-1],color="red")
    show()

def crear_sl_tp(rates_frame, sl, tp):

    rates_frame['SL'] = np.where(rates_frame['signal'] == 'sell', rates_frame['close'] + sl, np.where(rates_frame['signal'] == 'buy', rates_frame['close'] - sl, 0))
    rates_frame['TP'] = np.where(rates_frame['signal'] == 'sell', rates_frame['close'] - tp,
                                 np.where(rates_frame['signal'] == 'buy', rates_frame['close'] + tp, 0))

    shorts = rates_frame[rates_frame['signal'] == 'sell']
    longs = rates_frame[rates_frame['signal'] == 'buy']

    return shorts, longs


def backtesting_shorts(rates_frame, shorts, winner_op, loser_op):
    result_values = []

    for i in range(len(shorts['time'])):

        data = rates_frame[rates_frame['time'] > shorts.iloc[i, 0]]

        data_sl_shorts = data[(data['close'] >= shorts.iloc[i, 8]) | (data['high'] >= shorts.iloc[i, 8]) | (
                    data['low'] >= shorts.iloc[i, 10])]

        data_sl_shorts_min = data_sl_shorts[data_sl_shorts['time'] == data_sl_shorts['time'].min()]

        data_sl_shorts_min['result'] = 'loser'
        data_tp_shorts = data[(data['close'] <= shorts.iloc[i, 11]) | (data['high'] <= shorts.iloc[i, 11]) | (
                    data['low'] <= shorts.iloc[i, 11])]
        data_tp_shorts_min = data_tp_shorts[data_tp_shorts['time'] == data_tp_shorts['time'].min()]
        data_tp_shorts_min['result'] = 'winner'

        if len(data_tp_shorts_min) > 0 and len(data_sl_shorts_min) > 0:
            if data_tp_shorts_min.iloc[0, 0] < data_sl_shorts_min.iloc[0, 0]:
                resultado = 'winner'
            else:
                resultado = 'loser'
        elif len(data_tp_shorts_min) > 0 and len(data_sl_shorts_min) == 0:
            resultado = 'winner'
        else:
            resultado = 'loser'
        result_values.append(resultado)

    shorts['resultado'] = result_values
    shorts['profit'] = np.where(shorts['resultado'] == 'winner', winner_op, loser_op)

    return shorts


def backtesting_longs(rates_frame, longs, winner_op, loser_op):
    result_values_longs = []
    for i in range(len(longs['time'])):

        data = rates_frame[rates_frame['time'] > longs.iloc[i, 0]]

        data_sl_longs = data[(data['close'] <= longs.iloc[i, 10]) | (data['high'] <= longs.iloc[i, 10]) | (
                    data['low'] <= longs.iloc[i, 10])]

        data_sl_longs_min = data_sl_longs[data_sl_longs['time'] == data_sl_longs['time'].min()]
        data_sl_longs_min['result'] = 'loser'
        data_tp_longs = data[(data['close'] >= longs.iloc[i, 11]) | (data['high'] >= longs.iloc[i, 11]) | (
                    data['low'] >= longs.iloc[i, 11])]
        data_tp_longs_min = data_tp_longs[data_tp_longs['time'] == data_tp_longs['time'].min()]
        data_tp_longs_min['result'] = 'winner'

        if len(data_tp_longs_min) > 0 and len(data_sl_longs_min) > 0:
            if data_tp_longs_min.iloc[0, 0] < data_sl_longs_min.iloc[0, 0]:
                resultado = 'winner'
            else:
                resultado = 'loser'
        elif len(data_tp_longs_min) > 0 and len(data_sl_longs_min) == 0:
            resultado = 'winner'
        else:
            resultado = 'loser'
        result_values_longs.append(resultado)

    longs['resultado'] = result_values_longs
    longs['profit'] = np.where(longs['resultado'] == 'winner', winner_op, loser_op)

    return longs


def backtest_results_consolidated(shorts, longs):
    resultados_backtesting = pd.concat([shorts, longs])
    resultados_backtesting = resultados_backtesting.sort_values(by=['time'])
    resultados_backtesting['ganancias'] = resultados_backtesting['profit'].cumsum()
    # resultados_backtesting['ganancias'].plot()
    profit = sum(resultados_backtesting['profit'])
    try:
        q_longs = len(longs)
    except:
        q_longs = 0
    try:
        q_shorts = len(shorts)
    except:
        q_shorts = 0
    try:
        effectiveness = len(resultados_backtesting[resultados_backtesting['resultado'] == 'winner']) / len(
            resultados_backtesting['resultado'])
    except:
        effectiveness = 0

    # av_pos_month = (q_longs + q_longs)/((datetime.now() - min(shorts['time'],longs['time']))/30.0)

    total_profit = sum(resultados_backtesting['profit'])
    minimun = resultados_backtesting['ganancias'].min()
    try:
        shorts_effectiveness = len(shorts[shorts['resultado'] == 'winner']) / len(shorts)
    except:
        shorts_effectiveness = 0
    try:
        longs_effectiveness = len(longs[longs['resultado'] == 'winner']) / len(longs)
    except:
        longs_effectiveness = 0

    return resultados_backtesting, profit, effectiveness, total_profit, minimun, shorts_effectiveness, longs_effectiveness, q_longs, q_shorts


def handler_backtesting(symbol, sigma, sl, list_tp):

    rates_frame = creacion_de_señales()



    profits_list = []
    efec_list = []
    efe_shorts = []
    efe_longs = []
    winner_op = 30
    loser_op = 30

    for i in list_tp:
        shorts, longs = crear_sl_tp(rates_frame, sl, i)
        shorts = backtesting_shorts(rates_frame, shorts, winner_op, loser_op)
        longs = backtesting_longs(rates_frame, longs, winner_op, loser_op)
        resultados_backtesting, profit, effectiveness, total_profit, minimun, shorts_effectiveness, longs_effectiveness, q_longs, q_shorts = backtest_results_consolidated(shorts, longs)

        profits_list.append(profit)
        efec_list.append(effectiveness)
        efe_shorts.append(shorts_effectiveness)
        efe_longs.append(longs_effectiveness)

        print('############## Se ejecutó un TP  ####################')

    df_resultados = pd.DataFrame(zip(list_tp, profits_list, efec_list, efe_shorts, efe_longs))
    df_resultados.columns = ['TP', 'profit', 'efect_total', 'efectividad_shorts', 'efectividad_longs']

    return df_resultados


list_tp = [0.004, 0.005, 0.006]
print(handler_backtesting('EURUSD', sigma=2, sl=0.008, list_tp=list_tp))