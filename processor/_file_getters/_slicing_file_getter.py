from .._utils import Directory

__all__ = ["SlicingFileGetter"]


class SlicingFileGetter:
    """
    A class that retrieves countries and sliced/unsliced output directories
    for slicing files.

    Attributes:
        _EVENT_FOLDER_NAME (str): A private attribute representing the folder
            name where the event files are stored.
        __event_folder (Directory): A private attribute representing the
            directory object where the event files are located.
        __sliced_folder (Directory): A private attribute representing the
            directory object where the sliced/unsliced event files will be
            stored.
        __countries (list): A private attribute representing the list of
            countries where the event files are located.

    Args:
        data_folder (Directory): A Directory object representing the directory
            where the event files are located.
        _slice (bool): A private boolean attribute representing whether to
            slice the files or not. Default value is True.

    Properties:
        countries (list): A property representing the list of countries where
            the event files are located.
        sliced_folder (Directory): A property representing the directory where
            the sliced/unsliced event files will be stored.

    """
    _EVENT_FOLDER_NAME = "events"

    def __init__(self, data_folder: Directory, _slice=True):
        """
        Constructor of the SlicingFileGetter class.

        Args:
            data_folder (Directory): A Directory object representing the
                directory where the event files are located.
            _slice (bool): A private boolean attribute representing whether to
                slice the files or not. Default value is True.
        """
        sliced_folder_name = "sliced_data_sheets" if _slice \
            else "unsliced_data_sheets"
        self.__event_folder = \
            data_folder.find_directory(
                SlicingFileGetter._EVENT_FOLDER_NAME
            )
        data_folder.create_subdirectory(
            sliced_folder_name
        )
        self.__sliced_folder = \
            data_folder.find_directory(
                sliced_folder_name
            )
        self.__countries = self.__event_folder.get_files()

    @property
    def countries(self):
        """
        A property representing the list of countries where the event files
        are located.

        Returns:
            list: The list of countries where the event files are located.
        """
        return self.__countries

    @property
    def sliced_folder(self):
        """
        A property representing the directory where the sliced/unsliced event
        files will be stored.

        Returns:
            Directory: A Directory object representing the directory where
                the sliced/unsliced event files will be stored.
        """
        return self.__sliced_folder
