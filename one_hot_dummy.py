import sklearn


class GetDummies(sklearn.base.TransformerMixin):
    """Fast one-hot-encoder that makes use of pandas.get_dummies() safely
    on train/test splits.
    """

    def __init__(self, dtypes=None):
        self.input_columns = None
        self.final_columns = None
        if dtypes is None:
            dtypes = [object, "category"]
        self.dtypes = dtypes

    def fit(self, X, y=None, **kwargs):
        self.input_columns = list(X.select_dtypes(self.dtypes).columns)
        X = pd.get_dummies(X, columns=self.input_columns)
        self.final_columns = X.columns
        return self

    def transform(self, X, y=None, **kwargs):
        X = pd.get_dummies(X, columns=self.input_columns)
        X_columns = X.columns
        # if columns in X had values not in the data set used during
        # fit add them and set to 0
        missing = set(self.final_columns) - set(X_columns)
        for c in missing:
            X[c] = 0
        # remove any new columns that may have resulted from values in
        # X that were not in the data set when fit
        return X[self.final_columns]

    def get_feature_names(self):
        return tuple(self.final_columns)


# https://github.com/dantegates/fast-one-hot-encoder/blob/master/fast-one-hot-encoder.ipynb
