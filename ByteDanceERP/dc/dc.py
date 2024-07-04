import json
import datetime


def run(event_dict):
    # 解析JSON字符串
    dcs_str = event_dict['dc']
    dcs = json.loads(dcs_str)
    for dcData in dcs:
        dc = dcData['DC']
        dc_attach_data = {
            'Items': dc['Items'],
            'callbackUrl': dc.get('MISC16', ''),
            'businessType': dc.get('SubOrderType', '')
        }
        dcData['DC']['shipmentAttachData'] = json.dumps(dc_attach_data)
        shipped_date = datetime.datetime.strptime(dc['ShippedDate'], '%Y-%m-%dT%H:%M:%S.%f')
        formatted_date = shipped_date.strftime('%Y%m%d')
        # dcData['DC']['shipped_date'] = shipped_date.strftime('%Y-%m-%dT%H:%M:%S.%f')  # 将 datetime 转换为字符串
        for cartons in dcData['DC']['Cartons']:
            for item in cartons['ItemLines']:
                shipmentItemAttachData = {
                    'qualityLevel': 1,
                    'skuName': item['Description'],
                }
                item['shipmentItemAttachData'] = json.dumps(shipmentItemAttachData)
    return json.dumps(dcs)
