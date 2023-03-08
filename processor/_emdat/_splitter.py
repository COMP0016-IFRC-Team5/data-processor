import pandas as pd

__all__ = ['EMDATSplitter']


class EMDATSplitter:
    def __init__(self, df: pd.DataFrame):
        self.__data = {}
        self.__df = df
        self.__start()

    def __start(self):
        countries = self.__df['Country'].unique()
        for country in countries:
            self.__data[country] = self.__df[self.__df['Country'] == country]

        self.__split()

    def __split(self):
        for country, df in self.__data.items():
            required_events = ['Storm', 'Flood', 'Earthquake']
            events = {
                event: df[df['Disaster Type'] == event]
                for event in required_events
            }
            self.__data[country] = events

    @property
    def data(self):
        return self.__data
