import MetaTrader5 as mt5
import pandas as pd
from pylab import *
pd.set_option('display.max_rows', None)

mt5.initialize()
simbolo="USDJPY"
datos=pd.DataFrame(mt5.copy_rates_from_pos(simbolo,mt5.TIMEFRAME_H1,0,24000))[["close","time"]].set_index("time")
datos.index=pd.to_datetime(datos.index,unit="s")
datos["signal"]=[0,0,1,-1,0,0,
                 0,0,0,0,0,0,
                 0,0,0,0,0,0,
                 0,0,0,0,0,0,]*1000
datos["mult"]=datos.signal*datos.close
datos["retornos_simbol"]=datos.close.apply(np.log).diff()
datos["mis_retornos"]=datos.signal.shift(1)*datos.retornos_simbol
datos["mis_retornos_acum"]=datos.mis_retornos.cumsum().apply(np.exp)

subplot(221)
datos.mis_retornos.plot(kind="hist")
subplot(222)
datos.retornos_simbol.plot(kind="hist")
subplot(224)
datos.close.plot()
subplot(223)
datos.mis_retornos_acum.plot()

show()

print(pd.DataFrame(datos))