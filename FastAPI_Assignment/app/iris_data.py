import pandas as pd


class IrisDataFilter:
    def __init__(self, file_path: str):
        self.df = pd.read_csv(file_path)

    def filter_by_species(self, species: str):
        return self.df[self.df['Species'] == species]

    def get_unique_species(self):
        return self.df['Species'].unique()
