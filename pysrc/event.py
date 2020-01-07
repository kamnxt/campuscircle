import abc

class Event(abc.ABC):
    "Represents an event"

    @abc.abstractmethod
    def to_jsonable(self):
        "Returns the event in a format that can be easily serialized"

    @abc.abstractclassmethod
    def from_html(cls, date, html):
        "Parses html and returns an event"
