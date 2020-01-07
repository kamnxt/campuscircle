import datetime

from scheduleday import ScheduleDay


class Schedule:
    "A schedule with some amount of days"
    def __init__(self, days):
        self._days = days

    def to_jsonable(self):
        "Returns the schedule in jsonable format"
        return [day.to_jsonable() for day in self._days]

    @classmethod
    def from_html(cls, calendar_html):
        "Creates a schedule from html"
        year_and_month = calendar_html.find("#header-title", first=True).text
        year, base_month = (int(x) for x in year_and_month.split("/"))
        calendar_cells = calendar_html.find("#schedule-calender", first=True).find("td")
        days = []

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
            month = base_month + month_offset

            # make sure months wrap around nicely

            while month > 12:
                month = month - 12
                year += 1

            while month < 1:
                month += 12
                year -= 1

            date = datetime.datetime(year=year, month=month, day=day)

            # finally parse the classes for that day
            days.append(ScheduleDay.from_html(date, cell))
            #classes.append({"day": date.strftime("%Y/%m/%d"), "items": dayclasses})

        return cls(days)
