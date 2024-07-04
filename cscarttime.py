import math
import base64
import json
from datetime import datetime, timedelta

def run(event_dict):
    persistent_order_max_date = event_dict['orderMaxDate']
    created_at_min = event_dict['created_at_min']

    # Check if the datetime string ends with 'Z' indicating it's in UTC
    if created_at_min.endswith('Z'):
        # Directly parse the datetime string without timezone offset
        datetime_obj = datetime.strptime(created_at_min[:-1], '%Y-%m-%dT%H:%M:%S')
    elif not persistent_order_max_date:
        # Manually parsing the timezone offset
        date_str, tz_offset_str = created_at_min[:-6], created_at_min[-6:]
        datetime_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')

        # Convert timezone offset to hours and minutes
        tz_hours, tz_minutes = int(tz_offset_str[1:3]), int(tz_offset_str[4:])

        # Adjust datetime object according to the timezone offset
        if tz_offset_str[0] == '+':
            datetime_obj -= timedelta(hours=tz_hours, minutes=tz_minutes)
        else:
            datetime_obj += timedelta(hours=tz_hours, minutes=tz_minutes)

    if not persistent_order_max_date:
        timestamp_seconds = int((datetime_obj - datetime(1970,1, 1)).total_seconds())
        order_fetch_start_date = datetime_obj.isoformat() + 'Z'
    else:
        order_fetch_start_date = persistent_order_max_date

    order_date_json_object = {'orderFetchStartDate': order_fetch_start_date}
    return json.dumps(order_date_json_object)


def run(event_dict):\n    persistent_order_max_date = event_dict["orderMaxDate"]\n    created_at_min = event_dict["created_at_min"]\n\n    if created_at_min.endswith('Z'):\n        datetime_obj = datetime.strptime(created_at_min[:-1], "%Y-%m-%dT%H:%M:%S")\n    elif not persistent_order_max_date:\n        date_str, tz_offset_str = created_at_min[:-6], created_at_min[-6:]\n        datetime_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")\n        tz_hours, tz_minutes = int(tz_offset_str[1:3]), int(tz_offset_str[4:])\n        if tz_offset_str[0] == '+':\n            datetime_obj -= timedelta(hours=tz_hours, minutes=tz_minutes)\n        else:\n            datetime_obj += timedelta(hours=tz_hours, minutes=tz_minutes)\n\n    if not persistent_order_max_date:\n        timestamp_seconds = int((datetime_obj - datetime(1970,1, 1)).total_seconds())\n        order_fetch_start_date = datetime_obj.isoformat() + "Z"\n    else:\n        order_fetch_start_date = persistent_order_max_date\n\n    order_date_json_object = {'orderFetchStartDate': order_fetch_start_date}\n    return json.dumps(order_date_json_object)
