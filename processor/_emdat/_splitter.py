import pandas as pd

__all__ = ['EMDATSplitter']


class EMDATSplitter:
    """A class for splitting a pandas DataFrame into a dictionary of DataFrames
    based on the country and the disaster type.

    Attributes:
        __data (dict): A dictionary of DataFrames where the keys are country
            names and the values are dictionaries of DataFrames where the keys
            are disaster types and the values are DataFrames containing the data
            for that country and disaster type.
        __df (pd.DataFrame): The DataFrame to be split.

    Methods:
        data(): Returns the __data attribute.
    """
    def __init__(self, df: pd.DataFrame):
        """Initializes a new instance of the EMDATSplitter class.

        Args:
            df (pd.DataFrame): The DataFrame to be split.
        """
        self.__data = {}
        self.__df = df
        self.__start()

    def __start(self):
        """Splits the DataFrame based on the country name."""
        countries = self.__df['Country'].unique()
        for country in countries:
            self.__data[country] = self.__df[self.__df['Country'] == country]

        self.__split()

    def __split(self):
        """Splits the DataFrames for each country based on the disaster type."""
        for country, df in self.__data.items():
            required_events = ['Storm', 'Flood', 'Earthquake']
            events = {
                event: df[df['Disaster Type'] == event]
                for event in required_events
            }
            self.__data[country] = events

    @property
    def data(self):
        """Returns the __data attribute."""
        return self.__data
