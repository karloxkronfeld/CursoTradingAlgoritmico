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

