from datetime import date, timedelta

from ._event import Event
from ._data_card import DataCard

__all__ = ['EventBuilder']


class EventBuilder:
    def __init__(self, trigger: DataCard, event_type: str):
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
        return self.__start_date <= data_card.get_date() <= \
            self.__end_date_secondary

    def in_primary_interval(self, data_card: DataCard) -> bool:
        return self.__start_date <= data_card.get_date() <= \
            self.__end_date_primary

    def add(self, data_card: DataCard):
        assert self.in_secondary_interval(data_card) or \
            self.in_primary_interval(data_card)
        self.__records.append(data_card)

    @staticmethod
    def __convert_to_dict(data_card):
        """remove keys:
        serial,level0,level1,level2,approved,latitude,longitude,uuid,
        name0,name1,name2,event,location,date"""
        return {
            k: v
            for k, v in data_card.__dict__.items()
            if k not in ['serial', 'level0', 'level1', 'level2', 'approved',
                         'latitude', 'longitude', 'uuid', 'name0', 'name1',
                         'name2', 'event', 'location', 'date']
        }

    def build(self) -> Event:
        """
        sum values in the __records and build Event
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
