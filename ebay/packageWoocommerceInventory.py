import json


def run(event_dict):
    inventory_data = json.loads(event_dict.get('inventoryData'))
    all_products = json.loads(event_dict.get('allProducts'))

    products_map = {}
    for product in all_products:
        sku = product['sku']
        if sku:
            products_map[sku] = product['id']

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
        product_id = products_map.get(skuStockInfoKey)
        if product_id:
            stock_arr.append({
                'stock_quantity': sku_stock_map[skuStockInfoKey],
                'id': product_id
            })

    if stock_arr:
        res_data = {
            'update': stock_arr
        }
        return json.dumps(res_data)

    return res_data
