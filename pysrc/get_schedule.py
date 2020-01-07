import requests_html

from schedule import Schedule
from utils import ParseError


def get_schedule(username, password):
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
        "https://scs.cl.sophia.ac.jp/campusweb/campussquare.do",
        params={"_flowId": "PTW0001200-flow"},
    )

    try:
        return Schedule.from_html(res.html)
    except Exception as exc:
        raise ParseError(exc)
