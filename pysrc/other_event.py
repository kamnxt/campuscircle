import event


class OtherEvent(event.Event):
    "Some event we are not sure how to parse properly"

    def __init__(self, dictform):
        self._dictform = dictform

    def to_jsonable(self):
        return self._dictform

    @classmethod
    def from_html(cls, date, html):
        return cls(
            {
                "type": "other",
                "from_time": "00:00",  # day.isoformat(),
                "to_time": "23:59",  # day.replace(hour=23, minute=59).isoformat(),
                "location": "",
                "info": html.text,
                "flag": True,
            }
        )
