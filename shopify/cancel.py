

import math
import base64
import json
from datetime import datetime, timedelta
def run(event_dict):
    json_array = json.loads(event_dict['orderDatas'])
    max_time = None
    max_data = None
    for order in json_array:
        update_time = order['updated_at']
        if max_time is None or update_time > max_time:
            max_time = update_time
            max_data = order
            if max_data:
                last_colon_index = max_time.rfind(':')
                if '+' in max_time or '-' in max_time:
                    datetime_part, timezone_part = max_time[:last_colon_index - 3], max_time[last_colon_index - 3:]
                else:
                    datetime_part = max_time
                    timezone_part = ''
                    current_time = datetime.strptime(datetime_part, '%Y-%m-%dT%H:%M:%S')
                    new_time = current_time.replace(second=current_time.second + 1)
                    new_update_time = str(new_time.strftime('%Y-%m-%dT%H:%M:%S'))+str(timezone_part)
                    max_data['updated_at'] = new_update_time
                    return json.dumps(max_data)