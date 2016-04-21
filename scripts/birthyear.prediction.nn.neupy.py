import numpy as np
import pandas as pd
import networkx as nx

from sklearn import preprocessing
from sklearn.cross_validation import train_test_split

from neupy import environment
from neupy import algorithms, layers
from neupy.estimators import rmsle

g = nx.read_gexf("datasets/influences.gexf")

df = pd.DataFrame.from_csv("datasets/dates.birthdeath.csv",encoding="utf-8")

df_train = pd.DataFrame.from_csv("datasets/generations.training_sample.csv",encoding="utf-8")

df_test = pd.DataFrame.from_csv("datasets/generations.test.csv",encoding="utf-8")

# demographical statistics as input
input1 = list(df_train.fillna(0).loc[:,:].as_matrix())

# correlation matrix as input
g_train = g.subgraph([ n for n in df_train.index if n in g.nodes()])
input2 = nx.to_numpy_matrix(g_train)

# target
target = map(lambda idx: [df.fillna(0).loc[idx,"birthyear"]], df_train.index)

print input1[0:10]
print target[0:10]

data_scaler = preprocessing.MinMaxScaler()
target_scaler = preprocessing.MinMaxScaler()
target_scaler = target_scaler.fit([ [v] for v in list(df["birthyear"].fillna(0)) ])

data = data_scaler.fit_transform(input1)
target = target_scaler.transform(target)

environment.reproducible()

x_train, x_test, y_train, y_test = train_test_split(
    data, target, train_size=0.85
)


cgnet = algorithms.ConjugateGradient(
    connection=[
        layers.Sigmoid(len(input1[0])),
        layers.Sigmoid(100),
        layers.Output(1),
    ],
    search_method='golden',
    show_epoch=25,
    verbose=True,
    addons=[algorithms.LinearSearch],
)

cgnet.train(x_train, y_train, x_test, y_test, epochs=250)

# cgnet.plot_errors()

y_predict = cgnet.predict(x_test).round(1)
error = rmsle(target_scaler.inverse_transform(y_test),
              target_scaler.inverse_transform(y_predict))

search = data_scaler.fit_transform(list(df_test.fillna(0).as_matrix()))
search_y_predict = cgnet.predict(search).round(2)

df_test["predict"] = target_scaler.inverse_transform(search_y_predict)

print df_test["predict"]

df_test.to_csv("datasets/generations.test.predict.csv", encoding="utf-8")
