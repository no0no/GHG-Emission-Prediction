from sklearn.impute import SimpleImputer

class Preparer:

    def fill(self, train_set):
        imputer = SimpleImputer(strategy='mean')
        imputer.fit(train_set)
        X = imputer.transform(train_set)
        return X

    if __name__ == "__main__":
        pass