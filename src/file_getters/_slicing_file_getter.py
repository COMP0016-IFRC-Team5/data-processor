from utils import Directory

__all__ = ["SlicingFileGetter"]


class SlicingFileGetter:
    _SLICED_FOLDER_NAME = "sliced_data_sheets"
    _EVENT_FOLDER_NAME = "events"

    def __init__(self, data_folder: Directory):
        self.__event_folder = \
            data_folder.find_directory(
                SlicingFileGetter._EVENT_FOLDER_NAME
            )
        data_folder.create_subdirectory(
            SlicingFileGetter._SLICED_FOLDER_NAME
        )
        self.__sliced_folder = \
            data_folder.find_directory(
                SlicingFileGetter._SLICED_FOLDER_NAME
            )
        self.__countries = self.__event_folder.get_files()

    @property
    def countries(self):
        return self.__countries

    @property
    def sliced_folder(self):
        return self.__sliced_folder
