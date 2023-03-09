from .._utils import Directory, File
from .._apps import Slicer
from .._file_getters import SlicingFileGetter

__all__ = ["slice_controller"]


class SliceController:
    """A class for slicing files.

    Attributes:
        __sliced_folder (Directory | None): The directory where sliced files
            will be saved.
        __countries (list[File] | None): A list of files to be sliced.
        __slice (bool): A boolean to indicate whether to slice the files or not.

    Methods:
        start_slice(data_folder: Directory, _slice=True): Start the slicing
            process for the files in the data_folder.
    """
    def __init__(self):
        self.__sliced_folder: Directory | None = None
        self.__countries: list[File] | None = None
        self.__slice: bool = True

    def start_slice(self, data_folder: Directory, _slice=True):
        """Starts the slicing process for the files in the data_folder.

        Args:
            data_folder (Directory): The directory containing the files to be
                sliced.
            _slice (bool): A boolean to indicate whether to slice the files or
                not.
        """
        self.__slice = _slice
        file_getter = SlicingFileGetter(data_folder, _slice)
        self.__sliced_folder = file_getter.sliced_folder
        self.__countries = file_getter.countries
        self.__slice_for_all_countries()

    def __slice_for_all_countries(self):
        for country in self.__countries:
            self.__slice_for_one_country(country)

    def __slice_for_one_country(self, country: File):
        Slicer(country, self.__sliced_folder, self.__slice)


slice_controller = SliceController()
