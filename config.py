import pandas as pd


class SpectrumConfig:
    def __init__(self):
        self.Savitzky_df = pd.DataFrame({'window_length':[1],'polyorder':[0], 'Savitzky_mode':['nearest']})