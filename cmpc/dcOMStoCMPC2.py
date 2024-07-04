import json

def run(event_dict):
    shipment = json.loads(event_dict['shipment'])

    row = []
    units = []
    for item in shipment.get('shipmentAttachData', {}).get('Items', []):
        units.append({
            'DeliveryItemRef': item.get('DTLMISC01', ''),
            'Material': item.get('ItemNumber', ''),
            'UnitID': item.get('BuyerItemID', ''),
            'Quantity': item.get('ShippedQty', ''),
            'UnitOfMeasure': item.get('UOM', ''),
            'Ficha': item.get('DTLMISC02', '')
        })

    row.append({
        'WarehouseCompany': 'UNIS',
        'OutboundDelivery': shipment.get('referenceNo', ''),
        'ProductLine': shipment.get('shipmentAttachData', {}).get('ProductLine', ''),
        'CarrierName': shipment.get('carrier', {}).get('name', ''),
        'TruckID': shipment.get('shipmentAttachData', {}).get('TruckID', ''),
        'ShipmentDate': shipment.get('shipDate', ''),
        'Status': shipment.get('shipmentAttachData', {}).get('Status', ''),
        'Units': units
    })

    returnJson = {
        'row': row,
        'Details': [{
            'Status': 'I',
            'Message': 'Extra information'
        }]
    }
    return json.dumps(returnJson)
