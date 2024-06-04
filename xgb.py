import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
import pickle

tuna = pd.read_csv(r'C:\Users\DELL\Desktop\Detection-of-Phishing-Website-Using-Machine-Learning-master\ML work\DataSets\urldata.csv')
tuna.head()

dfsa = tuna.drop(['Domain'], axis = 1).copy()

dfsa = dfsa.sample(frac=1).reset_index(drop=True)

y = dfsa['Label']  #target variable
X = dfsa.drop('Label',axis=1)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 12)



# instantiate the model
xgb = XGBClassifier(learning_rate=0.4,max_depth=7)
#fit the model
xgb.fit(X_train, y_train)

y_test_xgb = xgb.predict(X_test)
y_train_xgb = xgb.predict(X_train)

#acc_train_xgb = accuracy_score(y_train,y_train_xgb)
#acc_test_xgb = accuracy_score(y_test,y_test_xgb)

#storeResults('XGBoost', acc_train_xgb, acc_test_xgb)

pickle.dump(xgb, open("XGBoostClassifier.pkl", "wb"))

