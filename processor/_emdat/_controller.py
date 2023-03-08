import pandas as pd

from ._emdat_file_getter import EMDATFileGetter
from ._splitter import EMDATSplitter
from .._utils import Directory

__all__ = ["emdat_controller"]


class EMDATController:
    def __init__(self):
        self.__data: pd.DataFrame | None = None
        self.__output_folder: Directory | None = None
        self.__splitted_data: dict[str, dict[str, pd.DataFrame]] | None = None

    def start(self, data_folder: Directory):
        file_getter = EMDATFileGetter(data_folder)
        self.__data = file_getter.data
        self.__output_folder = file_getter.output_folder
        splitter = EMDATSplitter(self.__data)
        self.__splitted_data = splitter.data
        self.__write_results()

    def __write_results(self):
        for country, events in self.__splitted_data.items():
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
