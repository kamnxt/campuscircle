import datetime

import requests_html

from utils import get_time_from_period, pluralize


class ClassEntry:
    "Class for representing a lecture in the schedule"
    def __init__(self, from_str):
        self.fulltext = from_str
        self.period = from_str.split(" ")[0]

        try:
            self.time = " - ".join(get_time_from_period(self.period))
        except ValueError:
            self.time = "?"
        self.class_info = ":".join(self.fulltext.split(":")[1:]).strip()
        self.location = self.class_info.split("@")[-1]
        self.class_info = "@".join(self.class_info.split("@")[:-1])

    def __str__(self):
        return f"ClassEntry({self.period})"


def get_calendar(username, password):
    "Gets a list of events"
    session = requests_html.HTMLSession()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"
        }
    )

    # first let's make a POST to the login endpoint so we get a session cookie
    session.post(
        "https://scs.cl.sophia.ac.jp/campusweb/campusportal.do",
        data={
            "userName": username,
            "password": password,
            "locale": "en_US",
            "wfId": "nwf_PTW0000002_login",
            "tabId": "home",
            "action": "rwf",
            "rwfHash": "ecf2c53af6d67fc9e90fc946bcfe97a7",
            "page": "",
        },
    )
    # Then let's actually get the page we want
    res = session.get(
        "https://scs.cl.sophia.ac.jp/campusweb/campusportal.do", params={"page": "main"}
    )
    todays_stuff = [
        line.strip()
        for line in res.html.find("ul.mysch-portlet-list", first=True).text.split("\n")
        if line
    ]
    todays_stuff = [line for line in todays_stuff if line]

    if len(todays_stuff) == 1 and todays_stuff[0] == "no schedule.":
        return []

    return [ClassEntry(line) for line in todays_stuff]


def show_page(calendar_items):
    "Renders the page"

    def to_table_item(item):
        return f"""<tr>
    <td>{item.period}</td>
    <td>{item.time}</td>
    <td>{item.class_info}</td>
    <td>{item.location}</td>
    </tr>"""

    pagetitle = f"Classes for {datetime.date.today()}"

    table_items = "\n".join(to_table_item(item) for item in calendar_items)

    return f"""
        <head>
        <title>{pagetitle}</title>
        <meta charset=utf-8>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel=stylesheet href=style.css></link>
        </head>
        <body>
            <div id=container>
                <h1>{pagetitle}</h1>
                <h2>You have {pluralize(len(calendar_items), 'class')} today.</h2>
                <table>
                    {table_items}
                </table>
            </div>
        </body>
        """
