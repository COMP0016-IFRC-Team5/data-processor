from utils import Directory, File
from apps import Slicer
from file_getters import SlicingFileGetter

__all__ = ["slice_controller"]


class SliceController:
    def __init__(self):
        self.__sliced_folder: Directory | None = None
        self.__countries: list[File] | None = None
        self.__slice: bool = True

    def start_slice(self, data_folder: Directory, slice=True):
        self.__slice = slice
        file_getter = SlicingFileGetter(data_folder, slice)
        self.__sliced_folder = file_getter.sliced_folder
        self.__countries = file_getter.countries
        self.__slice_for_all_countries()

    def __slice_for_all_countries(self):
        for country in self.__countries:
            self.__slice_for_one_country(country)

    def __slice_for_one_country(self, country: File):
        Slicer(country, self.__sliced_folder, self.__slice)


slice_controller = SliceController()
