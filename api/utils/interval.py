from dateutil.relativedelta import relativedelta
from datetime import datetime

# models
from models.event import Event


def generate_interval(event: Event) -> datetime:
    end_time = event.end_time
    start_time = event.start_time
    repeat_interval = event.repeat_interval
    repeat_unit = event.repeat_unit
    events: datetime = []

    events.append(start_time)
    if repeat_interval > 0:
        i = 0
        while start_time <= end_time and i < 200: #i < 200 -> don't create more than 200 events. Avoid endless loop
            i+=1
            if repeat_unit == 'days':
                start_time = start_time + relativedelta(days=+repeat_interval)
            elif repeat_unit == 'weeks':
                start_time = start_time + relativedelta(weeks=+repeat_interval)
            elif repeat_unit == 'months':
                start_time = start_time + relativedelta(months=+repeat_interval)
            elif repeat_unit == 'years':
                start_time = start_time + relativedelta(years=+repeat_interval)

            if start_time <= end_time:
                events.append(start_time)

    return events
