from datetime import date

__all__ = ['Event']


class Event:
    def __init__(self, data: dict,
                 event_type: str,
                 start_date: date, primary_end: date, secondary_end: date):
        self.data = data
        self.event_type = event_type
        self.start_date = start_date
        self.primary_end = primary_end
        self.secondary_end = secondary_end

    def as_dict(self) -> dict:
        """
        add event_type, start_date, primary_end, secondary_end to data
        and return
        """
        return {
            **self.data,
            'event': self.event_type,
            'start_date': self.start_date,
            'primary_end': self.primary_end,
            'secondary_end': self.secondary_end
        }

