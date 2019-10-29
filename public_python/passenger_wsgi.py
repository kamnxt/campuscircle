import json

from get_calendar import get_calendar, show_page

try:
    with open("config.json") as configfile:
        CONFIG = json.load(configfile)
except IOError:
    CONFIG = {}

try:
    USERNAME = CONFIG["username"]
    PASSWORD = CONFIG["password"]

    def application(env, start_response):
        start_response("200 OK", [("Content-Type", "text/html")])
        # TODO: perhaps try using env['REQUEST_URI'] for multiuser support

        return [show_page(get_calendar(USERNAME, PASSWORD)).encode()]


except KeyError:

    def application(env, start_response):
        start_response("500 Internal Server Error", [("Content-Type", "text/html")])

        return [b"Error in server configuration."]
