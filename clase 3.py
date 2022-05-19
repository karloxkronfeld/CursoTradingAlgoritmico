import MetaTrader5 as mt5
import pandas as pd

# name = 3998980
# key = "Inup.2021"
# serv = "Deriv-Demo"
# mt5.initialize(login=name,server=serv,password=key)
mt5.initialize()
open_pos = mt5.positions_get()

df_open_positions = pd.DataFrame(list(open_pos), columns= open_pos[0]._asdict().keys())

#Cerrar para Operaciones de compra

buy_positions = df_open_positions[df_open_positions['type'] == 0]
lista_ops = buy_positions['ticket'].unique().tolist()
tipo_operacion = mt5.ORDER_TYPE_SELL

for operacion in lista_ops:
    df_operacion = buy_positions[buy_positions['ticket'] == operacion]
    price_close = mt5.symbol_info_tick(df_operacion['symbol'].item()).bid
    simbolo_operacion = df_operacion['symbol'].item()
    volumen_operacion = df_operacion['volume'].item()

    close_request = {
        'action': mt5.TRADE_ACTION_DEAL,
        'symbol':simbolo_operacion,
        'volume':volumen_operacion,
        'type': tipo_operacion,
        'position': operacion,
        'price': price_close,
        'comment':'Cerrar posiciones',
        'type_filling': mt5.ORDER_FILLING_FOK
    }

    # mt5.order_send(close_request)


def break_even_function(df_open_positions: pd.DataFrame,perc_rec):
    if df_open_positions.empty:
        print('No hay operaciones abiertas')
    if not df_open_positions.empty:
        for operacion in df_open_positions['ticket'].unique().tolist():
            df_pos = df_open_positions[df_open_positions['ticket'] == operacion]
            type_op = df_pos['type'].item()

            symb = df_pos['symbol'].item()
            po = df_pos['price_open'].item()
            tp1 = df_pos['tp'].item()

            if df_pos['profit'].item() > 0:
                if type_op == 0:
                    modify_order_request = {
                        'action':mt5.TRADE_ACTION_SLTP,
                        'symbol':symb,
                        'position':operacion,
                        'sl':po,
                        'tp':tp1,
                        'type':mt5.ORDER_TYPE_SELL,
                        'type_filling':mt5.ORDER_FILLING_FOK,
                    }

                    mt5.order_send(modify_order_request)

break_even_function(df_open_positions,0.2)