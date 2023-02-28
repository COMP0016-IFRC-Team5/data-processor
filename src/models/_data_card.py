from datetime import date

__all__ = ['DataCard']


class DataCard:
    def __init__(self, record: dict):
        self.date: str | None = None
        self.event: str | None = None
        self.__dict__ = record

    def is_date_valid(self):
        year, month, day = self.__split_date()
        try:
            date(year, month, day)
            return True
        except ValueError:
            return False

    def __split_date(self):
        day_month_year = self.date.split('/')
        day = int(day_month_year[0])
        month = int(day_month_year[1])
        year = int(day_month_year[2])
        return year, month, day

    def get_date(self):
        year, month, day = self.__split_date()
        return date(year, month, day)
