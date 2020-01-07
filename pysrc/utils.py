"Just some utilities"

class ParseError(Exception):
    "Raised when we fail to parse an event."


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


def get_last_part_of_string_filtered(string, predicate):
    lastpart = ""
    rev = reversed(string)
    rest = ""

    for i in rev:
        if predicate(i):
            lastpart += i
        else:
            rest = i

            break
    lastpart = "".join(reversed(lastpart))
    rest = "".join(reversed(list(rev))) + rest

    return (lastpart, rest)


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
