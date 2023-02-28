from utils import Directory

__all__ = ["SlicingFileGetter"]


class SlicingFileGetter:
    _EVENT_FOLDER_NAME = "events"

    def __init__(self, data_folder: Directory, slice=True):
        sliced_folder_name = "sliced_data_sheets" if slice \
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
        return self.__countries

    @property
    def sliced_folder(self):
        return self.__sliced_folder
