import pandas as pd

from .._utils import Directory

__all__ = ["EMDATFileGetter"]


class EMDATFileGetter:
    _FOLDER_NAME = "_emdat"
    _FILE_NAME = "emdat_cleaned.csv"

    def __init__(self, data_folder: Directory):
        self.__output_folder = \
            data_folder.find_directory(EMDATFileGetter._FOLDER_NAME)
        data_path = f"{self.__output_folder.get_path()}/" \
                    f"{EMDATFileGetter._FILE_NAME}"
        self.__data = pd.read_csv(data_path)

    @property
    def data(self) -> pd.DataFrame:
        return self.__data

    @property
    def output_folder(self) -> Directory:
        return self.__output_folder
