import json


def run(event_dict):
    inventory_data = json.loads(event_dict.get('inventoryData'))
    inventoryItems = json.loads(event_dict.get('allProducts'))

    skuList = []
    for product in inventoryItems:
        sku = product['sku']
        if sku:
            skuList.append(sku)

    stock_arr = []
    res_data = {}
    sku_stock_map = {}
    for inventory in inventory_data:
        item_sku = inventory.get('itemSku')
        qty = inventory.get('qty')
        if sku_stock_map.get(item_sku):
            sku_stock_map[item_sku] += qty
        else:
            sku_stock_map[item_sku] = qty

    for skuStockInfoKey in sku_stock_map:
        if skuStockInfoKey in skuList:
            shipToLocationAvailability = {}
            shipToLocationAvailability['quantity'] = sku_stock_map[skuStockInfoKey]
            stock_arr.append({
                'shipToLocationAvailability': shipToLocationAvailability,
                'sku': skuStockInfoKey
            })

    if stock_arr:
        res_data = {
            'requests': stock_arr
        }
        return json.dumps(res_data)

    return res_data
