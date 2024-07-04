import datetime
import json


def run(event_dict):
    json_array = json.loads(event_dict['orderDatas'])
    max_order_date = None
    max_order_json_object = None
    for json_obj in json_array:
        current_order_modified_date = json_obj['date_modified']
        if max_order_date is None or current_order_modified_date > max_order_date:
            max_order_date = current_order_modified_date
            max_order_json_object = json_obj
    return json.dumps(max_order_json_object)
