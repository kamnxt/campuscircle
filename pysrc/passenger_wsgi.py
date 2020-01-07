import falcon
from schedule_resource import ScheduleResource

schedule_resource = ScheduleResource()

application = falcon.API()
application.add_route('/schedule', schedule_resource)
