import pandas as pd

from ._emdat_file_getter import EMDATFileGetter
from ._splitter import EMDATSplitter
from .._utils import Directory

__all__ = ["emdat_controller"]


class EMDATController:
    """Controller class for splitting and writing EM-DAT data into separate
    CSV files based on country and event type.

    Attributes:
        __data: EM-DAT data loaded from the given data folder.
        __output_folder: The output folder where the split data is saved.
        __split_data: A dictionary containing the split data, where the
            keys are the country names and the values are dictionaries of event
            types and dataframes.

    Methods:
        start(data_folder: Directory) -> None: Start the splitting and writing
            processed data for the given data folder.

    Note:
        This class depends on the following modules: pandas,
            ._emdat_file_getter, and ._splitter.
    """
    def __init__(self):
        self.__data: pd.DataFrame | None = None
        self.__output_folder: Directory | None = None
        self.__split_data: dict[str, dict[str, pd.DataFrame]] | None = None

    def start(self, data_folder: Directory):
        """Start the splitting and writing process for the given data folder.

        Args:
            data_folder: The directory where the EM-DAT data is located.
        """
        file_getter = EMDATFileGetter(data_folder)
        self.__data = file_getter.data
        self.__output_folder = file_getter.output_folder
        splitter = EMDATSplitter(self.__data)
        self.__split_data = splitter.data
        self.__write_results()

    def __write_results(self):
        """Write the split data to separate CSV files."""
        for country, events in self.__split_data.items():
            self.__output_folder.create_subdirectory(country)
            country_folder = self.__output_folder.find_directory(country)
            for event, df in events.items():
                df.sort_values(by=['Start Year', 'Start Month', 'Start Day'],
                               na_position='first', inplace=True)
                df.dropna(subset=['Start Year', 'Start Month', 'Start Day'],
                          inplace=True)
                df.to_csv(f"{country_folder.get_path()}/"
                          f"{event}.csv", index=False)


emdat_controller = EMDATController()
