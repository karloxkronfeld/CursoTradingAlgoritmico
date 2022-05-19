import MetaTrader5 as mt5
##EJERCICIO BUY
name = 	67042877
key = "Genttly.2022"
serv = "RoboForex-ECN"

mt5.initialize(login=name,server=serv,password=key)

request = {
        "action":mt5.TRADE_ACTION_DEAL, #se ejecuta de inmediato
        "symbol":'EURUSD',
        "type" : mt5.ORDER_TYPE_BUY, ####COMPRA
        "price": mt5.symbol_info_tick('EURUSD').ask, #PRECIO ASK
        "sl": mt5.symbol_info_tick().ask - 1.5,
        "tp": mt5.symbol_info_tick().bid - 3.5,
        "volume":0.01,
        "price": mt5.symbol_info_tick("EURUSD").ask,
        "comment":'NOMBRE______',
        "type_filling":mt5.ORDER_FILLING_IOC
}

result = mt5.order_send(request)
print("Orden enviada en {}".format("BTCUSD"));
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("ERROR: {} ".format(result.comment))

###EJERCICIO BUY-LIMIT
mt5.initialize()
request = {
        "action":mt5.TRADE_ACTION_PENDING, #orden pendiente
        "symbol":'BTCUSD',
        "type" : mt5.ORDER_TYPE_BUY_LIMIT, ####COMPRA
        "price": mt5.symbol_info_tick('BTCUSD').ask+200, #PRECIO ASK
        "volume":0.01,
        "comment":'NOMBRE_____',
        "type_filling":mt5.ORDER_FILLING_IOC
}

mt5.order_send(request)
