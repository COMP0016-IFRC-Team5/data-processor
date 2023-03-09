import pandas as pd

from .._utils import Directory, File
from .._apps import Combiner
from .._file_getters import MergeFileGetter, SubtypeFileGetter

__all__ = ['merge_controller']


class MergeController:
    """A controller for merging data files from different countries.

    Attributes:
        __output_folder (Directory | None): The output folder for merged files.
        __countries (list[Directory] | None): The countries to be merged.
        __subtypes (dict | None): The subtypes of events to be merged.
    """
    def __init__(self):
        self.__output_folder: Directory | None = None
        self.__countries: list[Directory] | None = None
        self.__subtypes: dict | None = None

    def start_merging(self, data_folder: Directory):
        """Starts merging the files in the given folder.

        Args:
            data_folder (Directory): The folder containing the data files.
        """
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
        """Writes the merged results to a CSV file.

        Args:
            country: The name of the country.
            events: The merged events.
        """
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
