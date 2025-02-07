import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split 
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler 
from sklearn.preprocessing import normalize 
from sklearn.metrics import accuracy_score



df =  pd.read_excel('AI Data.xlsx',engine='openpyxl' )

X = df["Score"] 
y = df['Bonus']

predictions= {}

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
print(X_train)
# print(X_train[0])
# print(X_train[1])
k = 3
knn = KNeighborsRegressor(n_neighbors=k)

knn.fit(X_train.values.reshape(-1,1), y_train)
y_predict = knn.predict([[10],[11.1],[19.2],[8.1]])

#print(y_predict)
score = knn.score(X_test.values.reshape(-1,1), y_test)


print(score)