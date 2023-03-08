from .._utils import Directory

__all__ = ["MergeFileGetter"]


class MergeFileGetter:
    _RECORD_FOLDER_NAME = "records"
    _EVENT_FOLDER_NAME = "events"

    def __init__(self, data_folder: Directory):
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
        return self.__countries

    @property
    def output_folder(self):
        return self.__output_folder
