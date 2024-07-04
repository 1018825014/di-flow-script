
import json
from datetime import datetime, timedelta

def run(event_dict):
    # 解析JSON字符串
    dcs_str = event_dict['dc']
    dcs = json.loads(dcs_str)
    for dcData in dcs:
        dc = dcData['DC']

        status_mappings = {
            'Shipped': 'S',
            'Cancelled': 'C',
            'Short Shipped': 'E',
            'Partial Shipped': 'E'
        }

        status = status_mappings.get(dc['Status'], '')

        dc_attach_data = {
            'ProductLine': dc['MISC03'],
            'TruckID': dc['TrailerNumber'],
            'Status': status,
            'Items': dc['Items']

        }
        dcData['DC']['shipmentAttachData'] = json.dumps(dc_attach_data)

        shipped_date = datetime.datetime.strptime(dc['ShippedDate'], '%Y-%m-%dT%H:%M:%S.%f')
        formatted_date = shipped_date.strftime('%Y%m%d')
        dcData['DC']['ShippedDate'] = formatted_date
        dcData['DC']['shipped_date'] = shipped_date.strftime('%Y-%m-%dT%H:%M:%S.%f')  # 将 datetime 转换为字符串

        for cartons in dcData['DC']['Cartons']:
            if not cartons['TrackingNo']:
                cartons['TrackingNo'] = cartons['CartonNo']
            for item in cartons['ItemLines']:
                shipmentItemAttachData = {
                    'Ficha': item['DTLMISC02']
                }
                item['shipmentItemAttachData'] = json.dumps(shipmentItemAttachData)

    return json.dumps(dcs)
