from Preparer import Preparer
from Visualizer import Visualizer
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
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
        clf = SVR(kernel='poly', gamma='scale', C=2.0, epsilon=0.2)
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

model = Modeler()
data = model.data_loader('Data/Merged.xlsx')

idx = data['Total emissions (CDP) [tCO2-eq]'].idxmax()
data.drop(data.index[idx], inplace=True)

print(data.shape)

train_set, test_set, labels = model.splitter(data, 42, 'Total emissions (CDP) [tCO2-eq]')

prep = Preparer()
X = prep.pipeline_gen(train_set)
train_set_tr = pd.DataFrame(X, columns=train_set.columns, index=train_set.index)
train_set_tr = prep.feature_selection(train_set_tr, labels)

predictions = model.trainer(train_set_tr, labels)
error = model.calculate_error(labels, predictions)
print('Specific:', error)

viz = Visualizer()
viz.box_plot(data['Total emissions (CDP) [tCO2-eq]'])
#viz.scatter_matrix_plt(data['Total emissions (CDP) [tCO2-eq]',
#                              'High BUA Mean - 1990, 2000, 2014 (UEX) [km2]',
#                              'Population Density Merged (GEA/UITP/WB)'])
