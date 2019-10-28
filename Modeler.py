from Preparer import Preparer
from Visualizer import Visualizer
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class Modeler:

    def data_loader(self, data_path):
        df = pd.read_excel(data_path)
        return df

    def splitter(self, data, seed, label):
        train_set, test_set = train_test_split(data, test_size=0.2, random_state=seed)
        labels = train_set[label].copy()
        train_set.drop(label, axis=1, inplace=True)
        return train_set, test_set, labels

    def trainer(self, train_set, labels):
        clf = svm.SVR()
        #clf = LinearRegression()
        clf.fit(train_set, labels)
        predictions = clf.predict(train_set)
        return predictions

    def calculate_error(self, labels, predictions):
        lin_mse = mean_squared_error(labels, predictions)
        lin_mse = np.sqrt(lin_mse)
        return lin_mse

    if __name__ == "__main__":
        pass

test = Modeler()
data = test.data_loader('Data/Merged.xlsx')

idx = data['Total emissions (CDP) [tCO2-eq]'].idxmax()
data.drop(data.index[idx], inplace=True)



"""
sample_data = data.sample(frac=0.3, replace=True, random_state=1)
train_set, test_set, labels = test.splitter(sample_data, 42, 'Total emissions (CDP) [tCO2-eq]')
prep = Preparer()
X = prep.fill(train_set)
train_set_tr = pd.DataFrame(X, columns=train_set.columns, index=train_set.index)
predictions = test.trainer(train_set_tr, labels)
error = test.calculate_error(labels, predictions)
print('Sample:', error)
"""


train_set, test_set, labels = test.splitter(data, 42, 'Total emissions (CDP) [tCO2-eq]')
prep = Preparer()
X = prep.fill(train_set)
train_set_tr = pd.DataFrame(X, columns=train_set.columns, index=train_set.index)
train_set_tr = train_set_tr[['High BUA Mean - 1990, 2000, 2014 (UEX) [km2]',
                             'Population Density Merged (GEA/UITP/WB)']]
predictions = test.trainer(train_set_tr, labels)
error = test.calculate_error(labels, predictions)
print('Specific:', error)


viz = Visualizer()
viz.box_plot(data['Total emissions (CDP) [tCO2-eq]'])
