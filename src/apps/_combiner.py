from collections import deque
import pandas as pd

from models import DataCard, EventBuilder, Event

__all__ = ["Combiner"]


class Combiner:
    def __init__(self, file, subtypes: dict):
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
        return self.__events

    def __filter_datacards(self, data_cards):
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
        assert all(datacard.is_date_valid() for datacard in filtered_datacards)
        return sorted(filtered_datacards,
                      key=lambda datacard: datacard.get_date())


class EventTypeAdapter:
    def __init__(self, subtypes: dict):
        for event, subtype_file in subtypes.items():
            contents = list(
                map(
                    lambda event_type: event_type.split('.')[0].upper(),
                    subtype_file.readlines()
                )
            )
            self.__setattr__(event, contents)

    def in_required_types(self, item):
        return (
            any(
                item.upper() in subtypes
                for event, subtypes in self.__dict__.items()
            )
            if isinstance(item, str)
            else False
        )

    def in_trigger_types(self, item):
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
    def __init__(self, trigger: DataCard, rest_datacards: deque[DataCard],
                 type_adapter: EventTypeAdapter):
        self.type_adapter = type_adapter
        assert self.type_adapter.in_trigger_types(trigger.event)
        self.event_type = self.type_adapter.root_type(trigger.event)
        self.builder = EventBuilder(trigger, self.event_type)
        self.event: Event | None = None
        self.rest_datacards = rest_datacards
        self.start_split()

    def start_split(self):
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
        return self.event, self.rest_datacards

    def __parse_unused_event(self):
        while len(self.rest_datacards) > 0:
            datacard = self.rest_datacards.popleft()
            if not self.type_adapter.in_required_types(datacard.event):
                continue
            self.rest_datacards.appendleft(datacard)
            break

    def __parse_fatal_failure(self, trigger):
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
