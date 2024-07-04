def run(event_dict):\n    # 解析JSON字符串\n    paramObjects = [\n        {'WarehouseID': '6106_107', 'FacilityID': '875', 'Desc': 'Charleston'},\n        {'WarehouseID': '6101_108', 'FacilityID': '909', 'Desc': 'New Jersey'},\n        {'WarehouseID': '6103_103', 'FacilityID': '920', 'Desc': 'Long Beach'},\n        {'WarehouseID': '6108_106', 'FacilityID': '140', 'Desc': 'Ignition'},\n        {'WarehouseID': '6111_106', 'FacilityID': '895', 'Desc': 'Houston'}\n    ]\n    dcs_str = event_dict['rnDatas']\n    rnData = json.loads(dcs_str)\n\n    if isinstance(rnData['row'], dict):\n        rnData['row'] = [rnData['row']]\n    elif isinstance(rnData['row'], list):\n        pass\n    rows = rnData['row']\n    rnMappingResult = []\n    for rn in rows:\n        if 'Header' in rn:\n            header = rn['Header']\n\n            itemsData = []\n\n            productLine = header['ProductLine']\n            processed_productLine = productLine.replace(' ', '').lower()\n            lumber_search = 'LUMBER'.replace(' ', '').lower()\n            forsac_search = 'FORSAC'.replace(' ', '').lower()\n            for item in header['Details']:\n                expectedQty = 0\n                if lumber_search in processed_productLine:\n                    expectedQty = item['Pcs_Unit']\n                elif forsac_search in processed_productLine:\n                    expectedQty = item['Quantity']\n                itemsData.append({\n                    'SerialNumber': item['Unit_ID'],  # RN没有SN这个字段\n                    'ItemNumber': item['SAPMaterialCode'],\n                    'ExpectedQty': expectedQty\n                })\n\n            # shipped_date = datetime.strptime(header['ArrivalDate'], '%Y-%m-%d')\n            # formatted_arr_date = shipped_date.strftime('%Y%m%d')\n\n            ASNContent = {\n                'ActionCode': 'Imported',\n                'PONo': header['CMPC_Invoice_Num'],\n                'DynTxtPropertyValue02': header['ProductLine'],\n                'ContainerNo': header['ContainerNumber'],\n                'ScheduledDate': header['ArrivalDate'],\n                'BOLNo': header['OceanBillofLading'],\n                'ReferenceNo': header['CMPC_PO_Num'],\n                'DynTxtPropertyValue01': header['SalesType'],\n                'Items': itemsData\n            }\n\n            warehouse_id_to_find = header['DestinationPort']\n            # 使用循环查找匹配的WarehouseID\n            facility_id = None\n            for obj in paramObjects:\n                if obj['WarehouseID'] == warehouse_id_to_find:\n                    facility_id = obj['FacilityID']\n                    break  # 找到匹配项后立即停止循环\n\n            rnMappingResult.append({\n                'CompanyID': 'LT',\n                'CustomerID': 'CMPCPL0001',\n                'FacilityID': facility_id,\n                'ASNContent': ASNContent\n            })\n    return json.dumps(rnMappingResult)