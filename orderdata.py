import math
import base64
import json
from datetime import datetime, timedelta

def run(event_dict):
    persistent_order_max_date = event_dict['orderMaxDate']
    created_at_min = event_dict['created_at_min']
    if not persistent_order_max_date:
        # created_at_min now is iso8601 UTC
        datetime_obj = datetime.strptime(created_at_min, "%Y-%m-%dT%H:%M:%SZ")
        timestamp_seconds = int(datetime_obj.timestamp())
        order_fetch_start_date = created_at_min

    else:
        order_fetch_start_date = persistent_order_max_date

    order_date_json_object = {'orderFetchStartDate': order_fetch_start_date}
    return json.dumps(order_date_json_object)
