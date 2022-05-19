############## Soportes y Resistencias #################

# Profundidad del Mercado #
symbol = 'EURUSD'
mt5.initialize(login = name, server = serv, password = key, path = path)
tasas_m1 = mt5.copy_rates_from_pos(symbol,mt5.TIMEFRAME_M15,0,99000)
tabla_tasas_m1 = pd.DataFrame(tasas_m1)

temp = tabla_tasas_m1[['close','tick_volume']]
temp['close2'] = round(temp['close'])
temp_agrupado = temp.groupby('close', as_index = False)['tick_volume'].sum()

temp_agrupado['close'].hist(bins = 100)

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, k_means

X = temp_agrupado[['close','tick_volume']]

#Preprocesamiento

scaler = StandardScaler().fit(X)
X_scaled = scaler.transform(X)

km_model = KMeans(n_clusters = 3, random_state = 0)
km_model.fit(X_scaled)

X['cluster_id'] = km_model.labels_
temp_agrupado['cluster_id'] = km_model.labels_

list_clusters = temp_agrupado['cluster_id'].unique().tolist()

min_vec = []
max_vec = []
mean_vec = []

for i in range(len(list_clusters)):
    X_temp = temp_agrupado[temp_agrupado['cluster_id'] == list_clusters[i]]

    std = X_temp['close'].std()
    med = X_temp['close'].mean()
    mins = med - std
    max = med + std

    min_vec.append(mins)
    max_vec.append(max)
    mean_vec.append(med)
