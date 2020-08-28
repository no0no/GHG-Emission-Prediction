from sklearn.feature_selection import f_regression, SelectKBest

class Preparer:

    def feature_selection(self, data, labels,):
        X_select = SelectKBest(f_regression, k=3).fit_transform(data, labels)
        return X_select

    def drop_label_outlier(self, data, label):
        Q1 = data[label].quantile(0.25)
        Q3 = data[label].quantile(0.75)
        IQR = Q3 - Q1
        true_list = ~((data[label] < (Q1 - 1.5 * IQR)) | (data[label] > (Q3 + 1.5 * IQR)))
        return true_list

    if __name__ == "__main__":
        pass