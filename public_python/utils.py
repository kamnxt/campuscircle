"Just some utilities"

import datetime


class BetterClassEntry:
    "Class for representing a lecture in the schedule"

    def __init__(self, date, from_str):

        self.date = date
        self.fulltext = from_str
        try:
            self.period = from_str.split(" ")[0]
            self.time = (
                self.date.strftime("%Y/%m/%d")
                + " "
                + (" - ".join(get_time_from_period(self.period)))
            )
            self.class_info = ":".join(self.fulltext.split(":")[1:]).strip()
            self.location = self.class_info.split("@")[-1]
            self.class_info = "@".join(self.class_info.split("@")[:-1])
        except (KeyError, ValueError, IndexError):
            self.period = ""
            self.location = ""
            self.time = self.date.strftime("%Y/%m/%d")
            self.class_info = self.fulltext

    def __str__(self):
        return f"ClassEntry({self.period})"


def parse_classes_for_day(day, cell_html):
    entries = [e.text for e in cell_html.find(".cal-content", first=True).find("span")]

    return [BetterClassEntry(day, entry) for entry in entries]


def parse_full_calendar(calendar_html):
    yearmonth = calendar_html.find("#header-title", first=True).text
    calendar_cells = calendar_html.find("#schedule-calender", first=True).find("td")
    classes = []

    # So the calendar we get can have leading days (from the previous month)
    month_offset = -1

    for cell in calendar_cells:
        date_elem = cell.find(".cal-head-number", first=True)

        # If we no longer have cal-head-oth we're in the current month

        if month_offset == -1 and "cal-head-oth" not in date_elem.attrs["class"]:
            month_offset = 0
        # and if it's back that means we are in the next month already!
        elif month_offset == 0 and "cal-head-oth" in date_elem.attrs["class"]:
            month_offset = 1
        day = int(cell.find(".cal-head-number", first=True).text)
        year, month = (int(x) for x in yearmonth.split("/"))
        month += month_offset

        # make sure months wrap around nicely

        while month > 12:
            month = month - 12
            year += 1

        while month < 1:
            month += 12
            year -= 1

        date = datetime.datetime(year=year, month=month, day=day)

        # finally parse the classes for that day
        dayclasses = parse_classes_for_day(date, cell)
        classes += dayclasses

    return [c for c in classes if c.date.date() >= datetime.datetime.now().date()]


def pluralize(num, singular):
    """Return the proper plural version.
    Examples:

    >>> pluralize(2, "meme")
    '2 memes'

    >>> pluralize(1, "thing")
    '1 thing'

    >>> pluralize(1, "class")
    '1 class'

    >>> pluralize(0, "class")
    '0 classes'
    """

    if num == 1:
        return f"{num} {singular}"

    plural_form = singular + ("es" if (singular[-1] == "s") else "s")

    return f"{num} {plural_form}"


PERIODS_TO_TIMES = {
    "1st": ("09:00", "10:40"),
    "2nd": ("10:55", "12:35"),
    "3rd": ("13:30", "15:10"),
    "4th": ("15:25", "17:05"),
    "5th": ("17:20", "19:00"),
    "6th": ("19:10", "20:50"),
}


def get_time_from_period(period):
    """Returns the start and end time of a period.
    Examples:

    >>> get_time_from_period("1st")
    ('09:00', '10:40')

    >>> get_time_from_period("999th")
    Traceback (most recent call last):
        ...
    ValueError: invalid period format
    """

    if period in PERIODS_TO_TIMES:
        return PERIODS_TO_TIMES[period]
    raise ValueError("invalid period format")
