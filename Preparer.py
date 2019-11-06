import numpy as np
from scipy import stats
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import f_regression, SelectKBest
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler

class Preparer:

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
       Q1 = data.quantile(0.25)
       Q3 = data.quantile(0.75)
       IQR = Q3 - Q1
       true_list = ~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR)))
       return true_list

    def drop_label_outlier(self, data, label):
        Q1 = data[label].quantile(0.25)
        Q3 = data[label].quantile(0.75)
        IQR = Q3 - Q1
        true_list = ~((data[label] < (Q1 - 1.5 * IQR)) | (data[label] > (Q3 + 1.5 * IQR)))
        return true_list

    if __name__ == "__main__":
        pass