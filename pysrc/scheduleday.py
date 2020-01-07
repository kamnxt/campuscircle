from lecture import Lecture
from other_event import OtherEvent
from utils import ParseError


class ScheduleDay:
    "A day with its schedule"

    def __init__(self, date, events):
        self._date = date
        self._events = events

    def to_jsonable(self):
        "Returns the day in a format that can easily be serialized"

        return {'date': self._date.strftime("%Y/%m/%d"), 'events': [event.to_jsonable() for event in self._events]}

    @classmethod
    def from_html(cls, date, html):
        "Creates a schedule day from html"
        events_html = html.find(".cal-content", first=True).find("span")

        def parse_event(event_html):
            try:
                return Lecture.from_html(date, event_html)
            except (ParseError, IndexError):
                return OtherEvent.from_html(date, event_html)

        return cls(date, [parse_event(event_html) for event_html in events_html])
