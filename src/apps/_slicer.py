import pandas as pd

from utils import Directory, File

__all__ = ["Slicer"]

TRIGGER_EVENTS = ["STORMS", "FLOODS", "EARTHQUAKES"]


class Slicer:
    def __init__(self, country: File, output_folder: Directory):
        self.__country_name = country.get_filename().split(".")[0]
        self.__country_path = country.get_filepath()
        self.__output_folder = output_folder
        self.__start()

    def __start(self):
        try:
            df = pd.read_csv(self.__country_path)
        except pd.errors.EmptyDataError:
            return
        splitter = Splitter(df)
        split_events = splitter.split_events
        sliced_events = Slicer.__slice_for_all_events(split_events)
        self.__save_results(sliced_events)

    @staticmethod
    def __slice_for_all_events(split_events):
        return [
            (trigger, Slicer.__slice_for_one_event(df))
            for trigger, df in split_events
        ]

    @staticmethod
    def __slice_for_one_event(df: pd.DataFrame):
        """remove first 5% amount of rows of df"""
        return df.iloc[int(len(df) * 0.05):]

    def __save_results(self, sliced_events):
        for trigger, df in sliced_events:
            self.__output_folder.create_subdirectory(self.__country_name)
            country_directory = \
                self.__output_folder.find_directory(self.__country_name)
            filepath = f"{country_directory.get_path()}/{trigger}.csv"
            df.to_csv(filepath, index=False)


class Splitter:
    def __init__(self, df: pd.DataFrame):
        self.__split_events = []
        self.__split_events.extend(
            (trigger, df[df['event'] == trigger]) for trigger in TRIGGER_EVENTS
        )

    @property
    def split_events(self):
        return self.__split_events
