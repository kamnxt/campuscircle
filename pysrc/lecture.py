import event
from utils import get_last_part_of_string_filtered, get_time_from_period


class Lecture(event.Event):
    def __init__(self, dictform):
        self._dictform = dictform

    def to_jsonable(self):
        return self._dictform

    @classmethod
    def from_html(cls, date, html):
        split = html.text.split(":")
        period = split[0].strip()
        lastpart = ""
        flag = False

        info = split[1].strip()
        try:
            time_from_period = get_time_from_period(period)
        except ValueError:
            flag = True
            period, moreinfo = get_last_part_of_string_filtered(
                period, lambda c: c.isalnum()
            )
            info = moreinfo + info
            time_from_period = get_time_from_period(period)
        from_time, to_time = time_from_period
        from_h, from_m = (int(x) for x in from_time.split(":"))
        to_h, to_m = (int(x) for x in to_time.split(":"))
        try:
            loc_split = info.split("@")
            info = "@".join(loc_split[:-1])
            location = loc_split[-1]
        except IndexError:
            location = ""

        return cls(
            {
                "type": "lecture",
                "from_time": from_time,  # day.replace(hour=from_h, minute=from_m).isoformat(),
                "to_time": to_time,  # day.replace(hour=to_h, minute=to_m).isoformat(),
                "location": location,
                "info": info,
                "flag": flag,
            }
        )
