import math
import base64
import json
from datetime import datetime, timedelta


def run(event_dict):
    inventoryData = json.loads(event_dict.get('inventoryData'))

    allLocations = json.loads(event_dict.get('allLocations'))
    allProducts = json.loads(event_dict.get('allProducts'))
    locationName = event_dict.get('locationName')
    locationsMap = {}
    productsMap = {}
    variantsQtyMap = {}
    variants_id = inventoryData.get('skuReferenceNo')
    qty = inventoryData.get('inventory')
    if variants_id and qty:
        if variants_id in variantsQtyMap:
            variantsQtyMap[variants_id] += qty
        else:
            variantsQtyMap[variants_id] = qty
    returnData = None
    for data in allLocations:
        name = data.get('name')
    lid = data.get('id')
    if name and lid:
        locationsMap[name] = lid
    for data in allProducts:
        for variants in data.get('variants'):
            variants_id = variants.get('id')
            inventoryItemId = variants.get('inventory_item_id')
    if variants_id and inventoryItemId:
        productsMap[variants_id] = inventoryItemId
    for inventory in variantsQtyMap:
        tLocationId = locationsMap.get(locationName)
        tInventoryItemId = productsMap.get(inventory)
        tQty = variantsQtyMap[inventory]
    if tLocationId and tInventoryItemId and tQty:
        returnData = {'location_id': tLocationId,
                      'inventory_item_id': tInventoryItemId,
                      'available': tQty}
    return json.dumps(returnData)
