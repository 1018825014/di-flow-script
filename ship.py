def run(event_dict):
    fulfillments = json.loads(event_dict['fulfillments'])
    shipment = json.loads(event_dict['shipment'])
    openFulfillments = None
    for fillment in fulfillments:
        if fillment['status'] == 'open':
            openFulfillments = fillment
            if openFulfillments is None:
                return '[]'
                fulfillmentItemIdMap = {}
                for line_items in openFulfillments['line_items']:
                    fulfillmentItemIdMap[str(line_items['line_item_id'])] = line_items['id']
                    shopifyShipmentData = []    for package in shipment['packages']:
                        company = package['carrierName']
                        fulfillment_order_line_items = []
                        line_items_by_fulfillment_order = [{
                            'fulfillment_order_id': openFulfillments['id'],
                            'fulfillment_order_line_items': fulfillment_order_line_items        }]
                        for itemLines in package['itemLines']:
                            fulfillment_order_line_items.append({
                                'id': fulfillmentItemIdMap[itemLines['poLineNo']],
                                'quantity': itemLines['shippedQty']            })
                            data = {            'fulfillment': {
                                'message': 'The package was shipped',
                                'notify_customer': 'false',
                                'tracking_info': {
                                    'company': company
                                },
                                'line_items_by_fulfillment_order': line_items_by_fulfillment_order,
                            }
                            }
                            shopifyShipmentData.append(data)
return json.dumps(shopifyShipmentData)
