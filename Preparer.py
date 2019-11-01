import numpy as np
from scipy import stats
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import f_regression, SelectKBest
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler

class Preparer:

    def fill(self, train_set):
        imputer = SimpleImputer(strategy='mean')
        imputer.fit(train_set)
        X = imputer.transform(train_set)
        return X

    # Impute and standardize data
    def pipeline_gen(self, data):
        pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('robust_scaler', RobustScaler()),
#            ('std_scaler', StandardScaler())
        ])
        return pipeline.fit_transform(data)

    def feature_selection(self, data, labels):
        pipeline = Pipeline([
            ('feature_selector', SelectKBest(f_regression, k=3))
        ])
        return pipeline.fit_transform(data, labels)

    def drop_outlier(self, data):
       return data[(np.abs(stats.zscore(data)) < 3).all(axis=1)]

    if __name__ == "__main__":
        pass