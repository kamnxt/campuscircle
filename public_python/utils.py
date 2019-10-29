"Just some utilities"


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
