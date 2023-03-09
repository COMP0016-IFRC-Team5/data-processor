from .._utils import Directory

__all__ = ["MergeFileGetter"]


class MergeFileGetter:
    """
    A class that retrieves countries and output directories for merging files.

    Attributes:
        _RECORD_FOLDER_NAME (str): A private attribute representing the folder
            name where the record files are stored.
        _EVENT_FOLDER_NAME (str): A private attribute representing the folder
            name where the event files are stored.
        __record_folder (Directory): A private attribute representing the
            directory object where the record files are located.
        __output_folder (Directory): A private attribute representing the
            directory object where the event files will be stored.
        __countries (list): A private attribute representing the list of
            countries where the record files are located.

    Args:
        data_folder (Directory): A Directory object representing the directory
            where the record files are located.

    Properties:
        countries (list): A property representing the list of countries where
            the record files are located.
        output_folder (Directory): A property representing the directory where
            the event files will be stored.

    """
    _RECORD_FOLDER_NAME = "records"
    _EVENT_FOLDER_NAME = "events"

    def __init__(self, data_folder: Directory):
        """
        Constructor of the MergeFileGetter class.

        Args:
            data_folder (Directory): A Directory object representing the
                directory where the record files are located.
        """
        self.__record_folder = \
            data_folder.find_directory(
                MergeFileGetter._RECORD_FOLDER_NAME
            )
        data_folder.create_subdirectory(
            MergeFileGetter._EVENT_FOLDER_NAME
        )
        self.__output_folder = \
            data_folder.find_directory(
                MergeFileGetter._EVENT_FOLDER_NAME
            )
        self.__countries = self.__record_folder.get_files()

    @property
    def countries(self):
        """
        A property representing the list of countries where the record files
        are located.

        Returns:
            list: The list of countries where the record files are located.
        """
        return self.__countries

    @property
    def output_folder(self):
        """
        A property representing the directory where the event files will be stored.

        Returns:
            Directory: A Directory object representing the directory where the
                event files will be stored.
        """
        return self.__output_folder
