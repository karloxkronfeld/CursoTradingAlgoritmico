import MetaTrader5 as mt5



##EJERCICIO BUY
mt5.initialize()
request = {
        "action":mt5.TRADE_ACTION_DEAL,
        "symbol":'BTCUSD',
        "type" : mt5.ORDER_TYPE_BUY, ####COMPRA
        "price": mt5.symbol_info_tick('BTCUSD').ask, #PRECIO ASK
        "volume":0.01,
        "comment":'NOMBRE______',
        "type_filling":mt5.ORDER_FILLING_IOC
}

result = mt5.order_send(request)
# print("Orden enviada en {}".format("BTCUSD"));
# if result.retcode != mt5.TRADE_RETCODE_DONE:
#     print("ERROR: {} ".format(result.comment))

###EJERCICIO BUY-LIMIT
mt5.initialize()
request = {
        "action":mt5.TRADE_ACTION_PENDING,
        "symbol":'BTCUSD',
        "type" : mt5.ORDER_TYPE_BUY_LIMIT, ####COMPRA
        "price": mt5.symbol_info_tick('BTCUSD').ask+200, #PRECIO ASK
        "volume":0.01,
        "comment":'NOMBRE_____',
        "type_filling":mt5.ORDER_FILLING_IOC
}

mt5.order_send(request)
