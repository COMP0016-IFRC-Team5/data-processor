from datetime import date, timedelta

from ._event import Event
from ._data_card import DataCard

__all__ = ['EventBuilder']


class EventBuilder:
    """A builder class for creating Event objects based on input DataCards.

    Attributes:
        __records (list[DataCard]): A list of DataCard objects.
        __event_type (str): The type of the event.
        __start_date (date): The start date of the event.
        __end_date_primary (date): The end date of the primary event interval.
        __end_date_secondary (date): The end of the secondary event interval.
    """
    def __init__(self, trigger: DataCard, event_type: str):
        """Constructs an EventBuilder object.

        Args:
            trigger (DataCard): The initial DataCard to trigger the event.
            event_type (str): The type of the event.
        """
        self.__records: list[DataCard] = [trigger]
        self.__event_type: str = event_type
        self.__start_date: date = trigger.get_date()
        self.__end_date_primary: date = self.__start_date + \
            timedelta(days=self.__get_primary_duration())
        self.__end_date_secondary: date = self.__start_date + \
            timedelta(days=self.__get_secondary_duration())

    def __get_primary_duration(self):
        match self.__event_type:
            case 'EARTHQUAKES':
                return 2
            case 'FLOODS':
                return 5
            case 'STORMS':
                return 5
            case _:
                return 1

    def __get_secondary_duration(self):
        match self.__event_type:
            case 'EARTHQUAKES':
                return 3
            case 'FLOODS':
                return 5
            case 'STORMS':
                return 5
            case _:
                return 1

    def in_secondary_interval(self, data_card: DataCard) -> bool:
        """Checks if a given DataCard is within the secondary event interval.

        Args:
            data_card (DataCard): The DataCard to check.

        Returns:
            bool: True if the DataCard is within the secondary interval, False
                otherwise.
        """
        return self.__start_date <= data_card.get_date() <= \
            self.__end_date_secondary

    def in_primary_interval(self, data_card: DataCard) -> bool:
        """Checks if a given DataCard is within the primary event interval.

        Args:
            data_card (DataCard): The DataCard to check.

        Returns:
            bool: True if the DataCard is within the primary interval, False
                otherwise.
        """
        return self.__start_date <= data_card.get_date() <= \
            self.__end_date_primary

    def add(self, data_card: DataCard):
        """Adds a DataCard to the event.

        Args:
            data_card (DataCard): The DataCard to add.

        Raises:
            AssertionError: If the DataCard is not within either the primary or
                secondary interval.
        """
        assert self.in_secondary_interval(data_card) or \
            self.in_primary_interval(data_card)
        self.__records.append(data_card)

    @staticmethod
    def __convert_to_dict(data_card):
        """Converts a DataCard object to a dictionary, excluding certain keys.

        Args:
            data_card (DataCard): The DataCard object to convert.

        Returns:
            dict: A dictionary representation of the DataCard object, with
                certain keys excluded.
        """
        return {
            k: v
            for k, v in data_card.__dict__.items()
            if k not in ['serial', 'level0', 'level1', 'level2', 'approved',
                         'latitude', 'longitude', 'uuid', 'name0', 'name1',
                         'name2', 'event', 'location', 'date']
        }

    def build(self) -> Event:
        """Builds and returns an Event object based on the DataCards in the
        event.

        Returns:
            Event: The built Event object.
        """
        data = {}
        for record in self.__records:
            for k, v in self.__convert_to_dict(record).items():
                if k in data:
                    data[k] += v
                else:
                    data[k] = v
        return Event(data, self.__event_type, self.__start_date,
                     self.__end_date_primary, self.__end_date_secondary)
