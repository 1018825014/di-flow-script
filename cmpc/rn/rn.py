import math
import base64
import json
from datetime import datetime, timedelta

import json


def run(event_dict):
    # 解析JSON字符串
    paramObjects = [
        {'WarehouseID': '6106_107', 'FacilityID': '805', 'Desc': 'Charleston'},
        {'WarehouseID': '6101_108', 'FacilityID': '909', 'Desc': 'New Jersey'},
        {'WarehouseID': '6103_103', 'FacilityID': '920', 'Desc': 'Long Beach'},
        {'WarehouseID': '6108_106', 'FacilityID': '140', 'Desc': 'Ignition'},
        {'WarehouseID': '6111_106', 'FacilityID': '895', 'Desc': 'Houston'}
    ]
    dcs_str = event_dict['rnDatas']
    customerId = event_dict['CustomerID']
    rnData = json.loads(dcs_str)

    if isinstance(rnData['row'], dict):
        rnData['row'] = [rnData['row']]
    elif isinstance(rnData['row'], list):
        pass
    rows = rnData['row']
    rnMappingResult = []
    for rn in rows:
        if 'Header' in rn:
            header = rn['Header']

            itemsData = []

            productLine = header['ProductLine']
            processed_productLine = productLine.replace(' ', '').lower()
            lumber_search = 'LUMBER'.replace(' ', '').lower()
            forsac_search = 'FORSAC'.replace(' ', '').lower()
            for item in header['Details']:
                expectedQty = 0
                if lumber_search in processed_productLine:
                    expectedQty = item['Pcs_Unit']
                elif forsac_search in processed_productLine:
                    expectedQty = item['Quantity']
                itemsData.append({
                    # 'SerialNumber': item['Unit_ID'],  # RN没有SN这个字段
                    'ItemNumber': item['SAPMaterialCode'],
                    'ExpectedQty': expectedQty
                })

            # shipped_date = datetime.strptime(header['ArrivalDate'], '%Y-%m-%d')
            # formatted_arr_date = shipped_date.strftime('%Y%m%d')

            ASNContent = {
                'ActionCode': 'Imported',
                'PONo': header['CMPC_Invoice_Num'],
                'SupplierID': customerId,
                'SCACCode': 'UPSN',
                'DynTxtPropertyValue02': header['ProductLine'],
                'ContainerNo': header['ContainerNumber'],
                'ScheduledDate': header['ArrivalDate'],
                'BOLNo': header['OceanBillofLading'],
                'ReferenceNo': header['CMPC_PO_Num'],
                'DynTxtPropertyValue01': header['SalesType'],
                'Status': 'Imported',
                'Items': itemsData
            }

            warehouse_id_to_find = header['DestinationPort']
            # 使用循环查找匹配的WarehouseID
            facility_id = None
            for obj in paramObjects:
                if obj['WarehouseID'] == warehouse_id_to_find:
                    facility_id = obj['FacilityID']
                    break  # 找到匹配项后立即停止循环

            rnMappingResult.append({
                'CompanyID': 'LT',
                'CustomerID': customerId,
                'FacilityID': facility_id,
                'ASNContent': ASNContent
            })
    return json.dumps(rnMappingResult)



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


def contains_ignore_case_and_space(text, search_term):
    # 移除字符串中的所有空格并转换为小写
    processed_text = text.replace(' ', '').lower()
    processed_search_term = search_term.replace(' ', '').lower()

    return processed_search_term in processed_text


# 示例使用
text = 'The price of lum ber is rising.'
search_term = 'lumber'
result = contains_ignore_case_and_space(text, search_term)
print(result)  # 输出结果将是True如果找到了，否则是False
