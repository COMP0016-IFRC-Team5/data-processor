from collections import deque
import pandas as pd

from .._models import DataCard, EventBuilder, Event

__all__ = ["Combiner"]


class Combiner:
    """
    Combiner class is used to combine datacards into events
    """
    def __init__(self, file, subtypes: dict):
        """
        Initialise combiner with file and subtypes

        Args:
            file (File): File object
            subtypes (dict): Dictionary of event types and subtype files

        Attributes:
            __filtered_datacards (deque[DataCard]): Filtered datacards from file
                by date and time with invalid datacards removed
            __events (list[Event]): List of events combined from datacards
            __type_adapter (EventTypeAdapter): Adapter for event types and
                subtypes from subtype files to check if event is required
        """
        self.__filtered_datacards: deque[DataCard] | None = None
        self.__events: list[Event] = []
        self.__type_adapter = EventTypeAdapter(subtypes)
        df = pd.read_csv(file.get_filepath())
        data_cards = list(
            map(
                lambda record: DataCard(record),
                df.to_dict('index').values()
            )
        )
        self.__filter_datacards(data_cards)
        self.__start_processing()

    def __start_processing(self):
        """
        Start processing datacards to combine them into events
        """
        while len(self.__filtered_datacards) > 0:
            datacard = self.__filtered_datacards.popleft()
            if not self.__type_adapter.in_trigger_types(datacard.event):
                continue
            splitter = EventSplitter(datacard, self.__filtered_datacards,
                                     self.__type_adapter)
            event, rest_datacards = splitter.get_results()
            self.__filtered_datacards = rest_datacards
            if event is None:
                continue
            self.__events.append(event)

    @property
    def events(self):
        """
        Get list of events
        """
        return self.__events

    def __filter_datacards(self, data_cards):
        """
        Filter datacards by date and time with invalid datacards removed

        Args:
            data_cards (list[DataCard]): List of datacards to filter
        """
        filtered_datacards = list(
            filter(
                lambda datacard: datacard.is_date_valid(),
                data_cards
            )
        )
        self.__filtered_datacards = \
            deque(Combiner.__sort_datacards_by_date(filtered_datacards))

    @staticmethod
    def __sort_datacards_by_date(filtered_datacards):
        """
        Sort datacards by date

        Args:
            filtered_datacards (list[DataCard]): List of datacards to sort

        Returns:
            list[DataCard]: Sorted list of datacards

        Raises:
            AssertionError: If any datacard is invalid
        """
        assert all(datacard.is_date_valid() for datacard in filtered_datacards)
        return sorted(filtered_datacards,
                      key=lambda datacard: datacard.get_date())


class EventTypeAdapter:
    """
    Adapter for event types and subtypes from subtype files to check if event
    is required
    """
    def __init__(self, subtypes: dict):
        """
        Initialise adapter with subtypes

        Args:
            subtypes (dict): Dictionary of event types and subtype files

        --------------------

        Required Attributes:
            LANDSLIDES (list[str]): List of landslide subtypes
            FLOODS (list[str]): List of flood subtypes
            EARTHQUAKES (list[str]): List of earthquake subtypes
            STORMS (list[str]): List of storm subtypes
        """
        for event, subtype_file in subtypes.items():
            contents = list(
                map(
                    lambda event_type: event_type.split('.')[0].upper(),
                    subtype_file.readlines()
                )
            )
            self.__setattr__(event, contents)

    def in_required_types(self, item):
        """
        Check if event is required

        Args:
            item (str): Event type to check

        Returns:
            bool: True if event is required, False otherwise

        --------------------

        Required Types:
            LANDSLIDES, FLOODS, EARTHQUAKES, STORMS
        """
        return (
            any(
                item.upper() in subtypes
                for event, subtypes in self.__dict__.items()
            )
            if isinstance(item, str)
            else False
        )

    def in_trigger_types(self, item):
        """
        Check if event is trigger type

        Args:
            item (str): Event type to check

        Returns:
            bool: True if event is trigger type, False otherwise

        --------------------

        Trigger Types:
            FLOODS, EARTHQUAKES, STORMS
        """
        return (
            any(
                item.upper() in subtypes
                for event, subtypes in self.__dict__.items()
                if event != "LANDSLIDES"
            )
            if isinstance(item, str)
            else False
        )

    def root_type(self, item):
        """
        Get root type of event

        Args:
            item (str): Event type to check

        Returns:
            str: Root type of event

        Example:
            >>> subtypes = {
            ...     "LANDSLIDES": ["LANDSLIDE", "LANDSLIDES, ROCKSLIDE"],
            ...     "FLOODS": ["FLASH FLOOD", "FLOOD, flashflood"],
            ...     "EARTHQUAKES": ["EARTHQUAKE"],
            ...     "STORMS": ["TORNADO", "STORM"],
            ... }
            >>> type_adapter = EventTypeAdapter(subtypes)
            >>> type_adapter.root_type("Flash Flood")
            FLOODS
        """
        return (
            next(
                (
                    event
                    for event, subtypes in self.__dict__.items()
                    if item.upper() in subtypes
                ),
                None,
            )
            if isinstance(item, str)
            else None
        )


class EventSplitter:
    """
    Split datacards into different events
    """
    def __init__(self, trigger: DataCard, rest_datacards: deque[DataCard],
                 type_adapter: EventTypeAdapter):
        """
        Initialise splitter with trigger datacard and rest of datacards

        Args:
            trigger (DataCard): Trigger datacard
            rest_datacards (deque[DataCard]): Rest of datacards
            type_adapter (EventTypeAdapter): Adapter for event types and
                subtypes from subtype files to check if event is required

        Attributes:
            type_adapter (EventTypeAdapter): Adapter for event types and
                subtypes from subtype files to check if event is required
            event_type (str): Event type of trigger datacard
            builder (EventBuilder): Event builder
            event (Event | None): Event to be returned
            rest_datacards (deque[DataCard]): Rest of datacards
        """
        self.type_adapter = type_adapter
        assert self.type_adapter.in_trigger_types(trigger.event)
        self.event_type = self.type_adapter.root_type(trigger.event)
        self.builder = EventBuilder(trigger, self.event_type)
        self.event: Event | None = None
        self.rest_datacards = rest_datacards
        self.start_split()

    def start_split(self):
        """
        Start splitting datacards into events
        """
        while len(self.rest_datacards) > 0:
            datacard = self.rest_datacards.popleft()
            current_event_type = self.type_adapter.root_type(datacard.event)
            meet_another_trigger = current_event_type != self.event_type and \
                self.type_adapter.in_trigger_types(datacard.event)
            in_primary_interval = self.builder.in_primary_interval(datacard)
            if not self.type_adapter.in_required_types(datacard.event):
                self.__parse_unused_event()
                continue
            if meet_another_trigger and in_primary_interval:
                self.__parse_fatal_failure(datacard)
                break
            if meet_another_trigger or \
                    (not in_primary_interval and
                     not self.builder.in_secondary_interval(datacard)):
                self.rest_datacards.appendleft(datacard)
                self.event = self.builder.build()
                break
            self.builder.add(datacard)

    def get_results(self):
        """
        Get results of splitting

        Returns:
            tuple[Event | None, deque[DataCard]]: Event and rest of datacards
        """
        return self.event, self.rest_datacards

    def __parse_unused_event(self):
        while len(self.rest_datacards) > 0:
            datacard = self.rest_datacards.popleft()
            if not self.type_adapter.in_required_types(datacard.event):
                continue
            self.rest_datacards.appendleft(datacard)
            break

    def __parse_fatal_failure(self, trigger):
        """
        Simulate normal parsing and stop when back to normal
        """
        self.event_type = self.type_adapter.root_type(trigger.event)
        self.builder = EventBuilder(trigger, self.event_type)
        while len(self.rest_datacards) > 0:
            datacard = self.rest_datacards.popleft()
            current_event_type = self.type_adapter.root_type(datacard.event)
            meet_another_trigger = current_event_type != self.event_type and \
                self.type_adapter.in_trigger_types(datacard.event)
            in_primary_interval = self.builder.in_primary_interval(datacard)
            if not self.type_adapter.in_required_types(datacard.event):
                self.__parse_unused_event()
                continue
            if meet_another_trigger and in_primary_interval:
                self.builder = EventBuilder(datacard, datacard.event)
                self.event_type = datacard.event
                continue
            if meet_another_trigger or \
                    (not in_primary_interval and
                     not self.builder.in_secondary_interval(datacard)):
                self.rest_datacards.appendleft(datacard)
                break
