import pandas as pd


class DataFrameState:
    def __init__(self, dataframe: pd.DataFrame):
        self.original = dataframe.copy()
        self.current = dataframe

    def reset(self):
        self.current = self.original.copy()
