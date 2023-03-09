import pandas as pd

from .._utils import Directory, File

__all__ = ["Slicer"]

TRIGGER_EVENTS = ["STORMS", "FLOODS", "EARTHQUAKES"]


class Slicer:
    """
    A class that slices a CSV file of disaster data for a specific country into
    separate CSV files for each type of disaster.

    Args:
        country (File): The input CSV file of disaster data.
        output_folder (Directory): The output directory for the sliced CSV files
        _slice (bool): Whether to slice the data by removing the first 5% of
            rows. Default is True.

    Attributes:
        __country_name (str): The name of the country derived from the input
            file name.
        __country_path (str): The path to the input file.
        __slice (bool): Whether to slice the data by removing the first 5% of
            rows.
        __output_folder (Directory): The output directory for the sliced CSV
            files.

    Methods:
        __start: Slices the input data and saves the sliced data as separate CSV
            files for each type of disaster.
        __slice_for_all_events: Slices the input data for all types of disasters
        __slice_for_one_event: Slices the input data for one type of disaster.
        __save_results: Saves the sliced data as separate CSV files for each
            type of disaster.
    """
    def __init__(self, country: File, output_folder: Directory, _slice=True):
        self.__country_name = country.get_filename().split(".")[0]
        self.__country_path = country.get_filepath()
        self.__slice = _slice
        self.__output_folder = output_folder
        self.__start()

    def __start(self):
        """
        Reads the input data, splits it by type of disaster, slices it for each
        disaster, and saves the sliced data.
        """
        try:
            df = pd.read_csv(self.__country_path)
        except pd.errors.EmptyDataError:
            return
        splitter = Splitter(df)
        split_events = splitter.split_events
        sliced_events = self.__slice_for_all_events(split_events)
        self.__save_results(sliced_events)

    def __slice_for_all_events(self, split_events):
        """
        Slices the input data for all types of disasters.

        Args:
            split_events (list): A list of tuples where each tuple contains the
                type of disaster and the corresponding subset of the input data.

        Returns:
            list: A list of tuples where each tuple contains the type of
                disaster and the corresponding sliced subset of the input data.
        """
        return [
            (trigger, self.__slice_for_one_event(df))
            for trigger, df in split_events
        ]

    def __slice_for_one_event(self, df: pd.DataFrame):
        """
        Slices the input data for a single type of disaster.

        Args:
            df (pd.DataFrame): The subset of the input data for a single type of
                disaster.

        Returns:
            pd.DataFrame: The sliced subset of the input data for a single type
                of disaster.
        """
        return df.iloc[int(len(df) * 0.05):] if self.__slice else df

    def __save_results(self, sliced_events):
        """
        Saves the sliced data as separate CSV files for each type of disaster.

        Args:
            sliced_events (list): A list of tuples where each tuple contains the
                type of disaster and the corresponding sliced subset of the
                input data.
        """
        for trigger, df in sliced_events:
            self.__output_folder.create_subdirectory(self.__country_name)
            country_directory = \
                self.__output_folder.find_directory(self.__country_name)
            filepath = f"{country_directory.get_path()}/{trigger}.csv"
            df.to_csv(filepath, index=False)


class Splitter:
    """Initializes a Splitter object that splits the given DataFrame by
        event type.

    Args:
        df (pd.DataFrame): A pandas DataFrame containing information on
            events.

    Attributes:
        __split_events (List[Tuple[str, pd.DataFrame]]): A list of tuples
            where the first element is the event type and the second element
            is a DataFrame containing information on events of that type.
    """
    def __init__(self, df: pd.DataFrame):
        self.__split_events = []
        self.__split_events.extend(
            (trigger, df[df['event'] == trigger]) for trigger in TRIGGER_EVENTS
        )

    @property
    def split_events(self):
        """Returns a list of tuples where the first element is the event type
        and the second element is a DataFrame containing information on events
        of that type.

        Returns:
            List[Tuple[str, pd.DataFrame]]: A list of tuples where the first
                element is the event type and the second element is a DataFrame
                containing information on events of that type.
        """
        return self.__split_events
