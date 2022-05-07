import MetaTrader5 as mt5

mt5.initialize()

request = {
        "action":mt5.TRADE_ACTION_DEAL,
        "symbol":'BTCUSD',
        "type" : mt5.ORDER_TYPE_BUY,
        "price": mt5.symbol_info_tick('BTCUSD').ask,
        "volume":0.01,
        "comment":'NOMBRE',
        "type_filling":mt5.ORDER_FILLING_IOC
}

result = mt5.order_send(request)
print("Orden enviada en {}".format("BTCUSD"));
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("ERROR: {} ".format(result.comment))

    # mt5.shutdown()

# import MetaTrader5 as mt5
#
#
# mt5.initialize()
# LOS_ACT=["EURUSD","XAUUSD","USDJPY","USDCHF","GBPJPY","EURCHF","BTCUSD","CADJPY","EURAUD","GBPCHF","NZDJPY"]
#
#
# def comprar():
#
#     for x in LOS_ACT:
#         symbol = x  #<<<<x son los activos desde el eurusd hasta el btc
#
#
#
#         point = mt5.symbol_info(symbol).point
#         price = mt5.symbol_info_tick(symbol).bid
#         deviation = 0
#
#         request = {
#             "action": mt5.TRADE_ACTION_DEAL,
#             "symbol": symbol,
#             "volume": 0.01,
#             "type": mt5.ORDER_TYPE_BUY,
#             "price": price,
#             "sl": price - 10 * point,
#             "tp": price + 50 * point,
#             "deviation": deviation,
#             "magic": 234000,
#             "comment": "carlos canola",
#             "type_time": mt5.ORDER_TIME_GTC,
#             "type_filling": mt5.ORDER_FILLING_IOC,
#         }
#
#         # print("{:<7}|{:>10f}".format(x,point))
#
#         # enviamos la solicitud comercial
#         result = mt5.order_send(request)
#         # comprobamos el resultado de la ejecución
#         print("Orden enviada en {} {} lots al precio {}".format(symbol, 0.01, price));
#         if result.retcode != mt5.TRADE_RETCODE_DONE:
#             print("ERROR: {} ".format(result.comment))
#
#             # mt5.shutdown()
#
# comprar()




