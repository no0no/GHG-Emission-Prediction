from Preparer import Preparer
from Visualizer import Visualizer
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
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
        #clf = SVR()
        clf = BaggingRegressor(n_estimators=1000)
        #clf = LinearRegression()
        #clf = LogisticRegression()
        clf.fit(train_set, labels)
        predictions = clf.predict(train_set)
        return predictions

    def calculate_error(self, labels, predictions):
        lin_mse = mean_squared_error(labels, predictions)
        lin_mse = np.sqrt(lin_mse)
        return lin_mse

    if __name__ == "__main__":
        pass

model = Modeler()
data = model.data_loader('Data/Merged.xlsx')
prep = Preparer()

print(data.shape)
no_outliers = prep.drop_label_outlier(data, 'Total emissions (CDP) [tCO2-eq]')
data = data[no_outliers]
print(data.shape)

#idx = data['Total emissions (CDP) [tCO2-eq]'].idxmax()
#data.drop(data.index[idx], inplace=True)

train_set, test_set, labels = model.splitter(data, 42, 'Total emissions (CDP) [tCO2-eq]')

X = prep.pipeline_gen(train_set)
train_set_tr = pd.DataFrame(X, columns=train_set.columns, index=train_set.index)

no_outliers = prep.drop_outlier(train_set_tr)
train_set_no_o = train_set_tr[no_outliers]
train_set_no_o = prep.feature_selection(train_set_tr, labels)

predictions = model.trainer(train_set_no_o, labels)
error = model.calculate_error(labels, predictions)
print('Specific:', error)

viz = Visualizer()
viz.box_plot(data['Total emissions (CDP) [tCO2-eq]'])
#viz.scatter_matrix_plt(data['Total emissions (CDP) [tCO2-eq]',
#                              'High BUA Mean - 1990, 2000, 2014 (UEX) [km2]',
#                              'Population Density Merged (GEA/UITP/WB)'])
