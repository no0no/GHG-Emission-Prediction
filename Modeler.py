from Preparer import Preparer
import numpy as np
import math
from sklearn.model_selection import train_test_split, GridSearchCV , cross_val_score
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from Visualizer import Visualizer

pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('robust_scaler', RobustScaler())
])

class Modeler:

    def __init__(self, data, seed):
        train_set, test_set, labels = self.generate_sets(data, seed)

        lin_scores, lin_model = self.lin_reg(train_set, labels)
        bagging_scores, bagging_model = self.bagging(train_set, labels)
        svr_scores, svr_model = self.svr(train_set, labels)

        lin_RMSE = self.final_RMSE(lin_model, test_set)
        bagging_RMSE = self.final_RMSE(bagging_model, test_set)
        svr_RMSE = self.final_RMSE(svr_model, test_set)

        names = ['Linear Regression', 'BaggingRegressor', 'SVR']
        scores = [lin_scores, bagging_scores, svr_scores]
        RMSEs = [lin_RMSE, bagging_RMSE, svr_RMSE]

        self.display_scores(scores, RMSEs, names)

    def generate_sets(self, data, seed):
        prep = Preparer()
        viz = Visualizer()

        viz.box_plot(data['Total emissions (CDP) [tCO2-eq]'])

        no_outliers = prep.drop_label_outlier(data, 'Total emissions (CDP) [tCO2-eq]')
        data_no_outliers = data[no_outliers]

        viz.box_plot(data_no_outliers['Total emissions (CDP) [tCO2-eq]'])

        train_set, test_set, labels = self.splitter(data_no_outliers, seed, 'Total emissions (CDP) [tCO2-eq]')
        X = pipeline.fit_transform(train_set)
        X_select = prep.feature_selection(X, labels)

        return X_select, test_set, labels

    def splitter(self, data, seed, label):
        train_set, test_set = train_test_split(data, test_size=0.2, random_state=seed)
        labels = train_set[label].copy()
        train_set.drop(label, axis=1, inplace=True)
        return train_set, test_set, labels

    def calculate_error(self, labels, predictions):
        lin_mse = mean_squared_error(labels, predictions)
        lin_mse = np.sqrt(lin_mse)
        return lin_mse

    def cross_val_score(self, model, data, labels):
        scores = cross_val_score(model, data, labels, scoring='neg_mean_squared_error', cv=5)
        return np.sqrt(-scores)

    def display_scores(self, validation_scores, test_RMSEs, names):

        for (score, RMSE, name) in zip(validation_scores, test_RMSEs, names):
            print(name)
            if name is 'SVR':
                print('Mean:', score[0])
                print('Standard Deviation', score[1])
            else:
                print('Mean:', score.mean())
                print('Standard Deviation', score.std())
            print('Final RMSE:', RMSE)
            print()

    def lin_reg(self, train_set, labels):
        model = LinearRegression()
        model.fit(train_set, labels)
        validation_RMSE = self.cross_val_score(model, train_set, labels)
        return validation_RMSE, model

    def bagging(self, train_set, labels):
        model = BaggingRegressor(n_estimators=1000)
        model.fit(train_set, labels)
        validation_RMSE = self.cross_val_score(model, train_set, labels)
        return validation_RMSE, model

    def svr(self, train_set, labels):
        param_grid = [
            {'kernel': ['rbf', 'poly'], 'C': [1.0, 1.5, 2.0], 'epsilon': [0.1, 0.2, 0.3, 0.4]}
        ]
        model = GridSearchCV(SVR(gamma='scale'), param_grid, cv=5, scoring='neg_mean_squared_error')
        model.fit(train_set, labels)

        mean = -(model.best_score_ / math.pow(10, 7))
        std = (model.cv_results_['std_test_score'][model.best_index_] / math.pow(10, 7))
        validation_RMSE = [mean, std]
        return validation_RMSE, model

    def final_RMSE(self, model, test_set):
        prep = Preparer()

        X_test = test_set.drop('Total emissions (CDP) [tCO2-eq]', axis=1)
        y_test = test_set['Total emissions (CDP) [tCO2-eq]'].copy()
        X_test_prepared = pipeline.transform(X_test)
        X_test_select = prep.feature_selection(X_test_prepared, y_test)

        final_predictions = model.predict(X_test_select)
        test_RMSE = self.calculate_error(y_test, final_predictions)
        return test_RMSE

    if __name__ == "__main__":
        pass