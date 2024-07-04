import math
import base64
import json
from datetime import datetime, timedelta

import json


def run(event_dict):
    # 解析JSON字符串
    order_datas_str = event_dict['orderDatas']
    order_datas = json.loads(order_datas_str)

    cancelledOrders = []

    # 遍历订单数据
    for order in order_datas:
        # 检查取消状态是否为CANCELED
        if order['cancelStatus']['cancelState'] == 'CANCELED':
            cancelledOrders.append(order)

    # 返回包含最大lastModifiedDate的JSON对象
    return json.dumps({'cancelledOrders': cancelledOrders})


# 示例调用
event_dict = {
    "orderDatas": json.dumps([
        {
            "lastModifiedDate": "2024-04-19T12:00:00Z",
            "cancelStatus": {
                "cancelState": "CANCELED",
                "cancelRequests": [
                    {
                        "cancelReason": "BUYER_ASKED_CANCEL",
                        "cancelRequestedDate": "2024-04-18T05:41:22.062Z",
                        "cancelInitiator": "SELLER",
                        "cancelRequestId": "5360375787",
                        "cancelRequestState": "COMPLETED"
                    }
                ]
            }
        },
        {
            "lastModifiedDate": "2024-04-20T12:00:00Z",
            "cancelStatus": {
                "cancelState": "NOT_CANCELED",
                "cancelRequests": []
            }
        },
        {
            "lastModifiedDate": "2024-04-21T12:00:00Z",
            "cancelStatus": {
                "cancelState": "CANCELED",
                "cancelRequests": [
                    {
                        "cancelReason": "NO_STOCK",
                        "cancelRequestedDate": "2024-04-18T06:00:00.000Z",
                        "cancelInitiator": "SELLER",
                        "cancelRequestId": "5360375890",
                        "cancelRequestState": "PENDING"
                    }
                ]
            }
        }
    ])
}

print(run(event_dict))
