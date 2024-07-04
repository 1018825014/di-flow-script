import math
import base64
import json
from datetime import datetime, timedelta

import json


def run(event_dict):

    # 解析JSON字符串
    dcs_str = event_dict['dc']
    dcs = json.loads(dcs_str)
    for dcData in dcs:
        dc = options['record']['DC']
        row = []
        status = ''
        units = []

        status_mappings = {
            "Shipped": "S",
            "Cancelled": "C",
            "Short Shipped": "E",
            "Partial Shipped": "E"
        }

        status = status_mappings.get(dc['Status'], '')

        for item in dc['Items']:
            units.append({
                "DeliveryItemRef": item['DTLMISC01'],
                "Material": item['ItemNumber'],
                "UnitID": item['BuyerItemID'],
                "Quantity": item['ShippedQty'],
                "UnitOfMeasure": item['UOM'],
                "Ficha": item['DTLMISC02']
            })

        shipped_date = datetime.datetime.strptime(dc['ShippedDate'], '%Y-%m-%d')
        formatted_date = shipped_date.strftime('%Y%m%d')

        row.append({
            "WarehouseCompany": "UNIS",
            "OutboundDelivery": dc['ReferenceNo'],
            "ProductLine": dc['MISC03'],
            "CarrierName": dc['CarrierID'],
            "TruckID": dc['TrailerNumber'],
            "ShipmentDate": formatted_date,
            "Status": status,
            "Units": units
        })

        return {
            "row": row,
            "Details": [{
                "Status": "I",
                "Message": "Extra information"
            }]
        }


# Example usage
event_dict = {
    'record': {
        'DC': {
            'Status': 'Shipped',
            'Items': [
                {
                    'DTLMISC01': 'Ref123',
                    'ItemNumber': '123456',
                    'BuyerItemID': '78910',
                    'ShippedQty': 100,
                    'UOM': 'PCS',
                    'DTLMISC02': 'Info'
                }
            ],
            'ReferenceNo': 'Ref001',
            'MISC03': 'ProdLine1',
            'CarrierID': 'CarrierXYZ',
            'TrailerNumber': 'Trailer001',
            'ShippedDate': '2024-04-29'
        }
    }
}

result = run(event_dict)
print(result)
