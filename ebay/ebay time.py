
import math
import base64
import json
from datetime import datetime, timedelta

def run(event_dict):
    # 解析JSON字符串
    order_datas_str = event_dict['orderDatas']
    order_datas = json.loads(order_datas_str)

    creation_date_list = [data['creationDate'] for data in order_datas]

    # 比较获取最大的时间
    if creation_date_list:
        max_date_time = parser.isoparse(creation_date_list[0])
        for date_time_str in creation_date_list:
            current_date_time = parser.isoparse(date_time_str)
            if current_date_time > max_date_time:
                max_date_time = current_date_time

        # 增加1微秒
        max_date_time += timedelta(microseconds=1)
        return json.dumps({"maxDateTime": max_date_time.isoformat()})
    else:
        return json.dumps({})