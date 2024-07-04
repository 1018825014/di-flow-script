import math
import base64
import json
from datetime import datetime, timedelta

import json


def run(event_dict):
    # 解析JSON字符串
    order_datas_str = event_dict['orderDatas']
    order_datas = json.loads(order_datas_str)
    for order in order_datas:
        # 创建orderAttachData内容并转换为JSON字符串
        order_attach_data = {
            'SpecialRemarks': order['Deliveries']['SpecialRemarks'],
            'ProductLine': order['Deliveries']['ProductLine']
        }
        order['Deliveries']['orderAttachData'] = json.dumps(order_attach_data)
        deliveryDate = str(order['Deliveries']['DeliveryDate'])
        # 假设所有的日期都是在午后2点15分22秒
        dt = datetime.strptime(deliveryDate + '000000', '%Y%m%d%H%M%S')
        # 将datetime对象格式化为ISO 8601格式，并添加Z表示UTC时间
        order['Deliveries']['DeliveryDate'] = dt.isoformat() + 'Z'
        # 遍历DeliveriesDetail数组，为每个元素添加orderItemAttachData字段
        for item in order['Deliveries']['DeliveriesDetail']:
            if item['UnitOfMeasure'] == 'PC':
                item['UnitOfMeasure'] = 'PT'
            item_attach_data = {
                'UnitID': item['UnitID'],
                'Ficha': item['Ficha']
            }
            item['orderItemAttachData'] = json.dumps(item_attach_data)
    # 将修改后的order_datas转换回JSON字符串
    modified_order_datas_str = json.dumps(order_datas)
    return modified_order_datas_str
