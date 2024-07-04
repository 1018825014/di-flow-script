
import datetime
import json


def run(event_dict):
    persistent_order_max_date = event_dict['orderMaxModifiedDate']
    created_at_min = event_dict['created_at_min']
    if not persistent_order_max_date:
        created_at_min = created_at_min.replace('+08:00', '')
        order_fetch_start_date = created_at_min
    else:
        order_fetch_start_date = persistent_order_max_date

    order_date_json_object = {'orderFetchStartDate': order_fetch_start_date}
    return json.dumps(order_date_json_object)