from .._utils import Directory

__all__ = ["SubtypeFileGetter"]


class SubtypeFileGetter:
    """A class to retrieve subtype files and store them as a dictionary.

    Attributes:
        _SUBTYPE_FOLDER_NAME (str): Name of the subtype folder.

    Args:
        data_folder (Directory): A `Directory` object containing the subtype
            files.
    """
    _SUBTYPE_FOLDER_NAME = "categorizations"

    def __init__(self, data_folder: Directory):
        self.__subtype_folder = \
            data_folder.find_directory(
                SubtypeFileGetter._SUBTYPE_FOLDER_NAME
            )
        required_subtypes = ["STORMS.txt", "FLOODS.txt", "EARTHQUAKES.txt",
                             "LANDSLIDES.txt"]
        self.__subtypes = \
            list(
                filter(
                    lambda subtype: subtype.get_filename() in required_subtypes,
                    self.__subtype_folder.get_files()
                )
            )
        # convert subtypes in dict by its name
        self.__subtypes = \
            {subtype.get_filename().split(".")[0]: subtype for subtype in
             self.__subtypes}

    @property
    def subtypes(self):
        """
        Returns the subtype files as a dictionary, with subtype names as keys
        and `File` objects as values.

        Returns:
            dict: A dictionary of subtype files.
        """
        return self.__subtypes

