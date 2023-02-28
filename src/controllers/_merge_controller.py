import pandas as pd

from utils import Directory, File
from apps import Combiner
from file_getters import MergeFileGetter, SubtypeFileGetter

__all__ = ['merge_controller']


class MergeController:
    def __init__(self):
        self.__output_folder: Directory | None = None
        self.__countries: list[Directory] | None = None
        self.__subtypes: dict | None = None

    def start_merging(self, data_folder: Directory):
        merge_file_getter = MergeFileGetter(data_folder)
        subtype_file_getter = SubtypeFileGetter(data_folder)
        self.__output_folder = merge_file_getter.output_folder
        self.__countries = merge_file_getter.countries
        self.__subtypes = subtype_file_getter.subtypes
        self.__merge_for_all_countries()

    def __merge_for_all_countries(self):
        for country in self.__countries:
            self.__merge_for_one_country(country)

    def __merge_for_one_country(self, file: File):
        country = file.get_filename()
        combiner = Combiner(file, self.__subtypes)
        events = combiner.events
        self.__write_results(country, events)

    def __write_results(self, country, events):
        filepath = f"{self.__output_folder.get_path()}/{country}"
        contents = list(
            map(
                lambda event: event.as_dict(),
                events
            )
        )
        # noinspection PyTypeChecker
        df = pd.DataFrame.from_dict(contents)
        df.to_csv(filepath, index=False)


merge_controller = MergeController()
