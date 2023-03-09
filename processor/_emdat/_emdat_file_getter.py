import pandas as pd

from .._utils import Directory

__all__ = ["EMDATFileGetter"]


class EMDATFileGetter:
    """
    A class that loads EM-DAT cleaned dataset from disk.

    Attributes:
        _FOLDER_NAME (str): A private attribute representing the folder name
            where the EM-DAT dataset is stored.
        _FILE_NAME (str): A private attribute representing the name of the
            EM-DAT dataset file.
        __output_folder (Directory): A private attribute representing the
            directory object where _FOLDER_NAME indicated.
        __data (pd.DataFrame): A private attribute representing the EM-DAT
            dataset loaded from the disk.

    Args:
        data_folder (Directory): A Directory object representing the directory
            where the EM-DAT dataset is located.

    Properties:
        data (pd.DataFrame): A property representing the loaded EM-DAT dataset.
        output_folder (Directory): A property representing the directory
            where _FOLDER_NAME indicated.

    """
    _FOLDER_NAME = "emdat"
    _FILE_NAME = "emdat_cleaned.csv"

    def __init__(self, data_folder: Directory):
        """
        Constructor of the EMDATFileGetter class.

        Args:
            data_folder (Directory): A Directory object representing the
                directory where the EM-DAT dataset is located.
        """
        self.__output_folder = \
            data_folder.find_directory(EMDATFileGetter._FOLDER_NAME)
        data_path = f"{self.__output_folder.get_path()}/" \
                    f"{EMDATFileGetter._FILE_NAME}"
        self.__data = pd.read_csv(data_path)

    @property
    def data(self) -> pd.DataFrame:
        """
        A property representing the loaded EM-DAT dataset.

        Returns:
            pd.DataFrame: The EM-DAT dataset loaded from the disk.
        """
        return self.__data

    @property
    def output_folder(self) -> Directory:
        """
        A property representing the directory where the EM-DAT dataset is
        located

        Returns:
            Directory: A Directory object representing the directory where the
                EM-DAT dataset is located.
        """
        return self.__output_folder
