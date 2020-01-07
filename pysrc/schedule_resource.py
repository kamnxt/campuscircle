import json
import traceback
from utils import ParseError
from get_schedule import get_schedule

class ScheduleResource:
    _cached_media = None
    def on_get(self, req, resp):
        try:
            with open('config.json') as f:
                conf = json.load(f)
            if not conf.get('cache', True) or self._cached_media is None:
                username = conf['username']
                password = conf['password']
                events = get_schedule(username, password).to_jsonable()
                self._cached_media = events
            else:
                events = self._cached_media
            resp.set_header('Access-Control-Allow-Origin', '*')
            resp.media = events
            resp.status = '200'
        except ParseError:
            resp.set_header('Access-Control-Allow-Origin', '*')
            resp.media = {"error": "failed to parse data from loyola."}
            resp.status = '500'
            traceback.print_exc()
        except Exception:
            resp.set_header('Access-Control-Allow-Origin', '*')
            resp.media = {"error": "internal server error"}
            resp.status = '500'
            traceback.print_exc()
            #resp.body = '<!doctype html><head><link rel=stylesheet href=style.css></head><body><h1>Internal server error.</h1></body>'
