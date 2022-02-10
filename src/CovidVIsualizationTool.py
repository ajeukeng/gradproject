import pandas as pd


class CovidVisualizationTool:
    def __init__(self, csv_data):
        self.csv_data = csv_data

    def get_data(self):
        """Place Data into Pandas dataframe"""
        covid_df = pd.read_csv(self.csv_data)
        return covid_df
