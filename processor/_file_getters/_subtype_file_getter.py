from .._utils import Directory

__all__ = ["SubtypeFileGetter"]


class SubtypeFileGetter:
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
        return self.__subtypes

