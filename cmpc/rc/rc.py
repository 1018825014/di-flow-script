import json
from datetime import datetime


def run(event_dict):
    rcs = json.loads(event_dict['rcdata'])

    results = []
    units = []
    paramObjects = [
        {
            'WarehouseID': '6106_107',
            'FacilityID': '875',
            'Desc': 'Charleston'
        },
        {
            'WarehouseID': '6101_108',
            'FacilityID': '909',
            'Desc': 'New Jersey'
        },
        {
            'WarehouseID': '6103_103',
            'FacilityID': '920',
            'Desc': 'Long Beach'
        },
        {
            'WarehouseID': '6108_106',
            'FacilityID': '140',
            'Desc': 'Ignition'
        },
        {
            'WarehouseID': '6111_106',
            'FacilityID': '895',
            'Desc': 'Houston'
        }
    ]
    for rcdata in rcs:
        rc = rcdata['RC']
        facility_id_to_find = rcdata.get('FacilityID')
        warehouse_id = None
        for obj in paramObjects:
            if obj['FacilityID'] == facility_id_to_find:
                warehouse_id = obj['WarehouseID']
                break
        datetime_str = rc.get('ReceivedDate')
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f')

        formatted_date = datetime_obj.strftime('%Y%m%d')
        row = [{
            'WarehouseCompany': 'UNIS',
            'ContainerNumber': rc.get('ContainerNumber', ''),
            'WarehouseID': warehouse_id,
            'CMPCPONumber': rcdata.get('ReferenceNo'),
            'BLNum': rc.get('BOLNo'),
            'CMPCInvoiceNum': rc.get('PONo'),
            'ArrivalDateWarehouse': formatted_date,
            'ProductLine': rc.get('DynTxtPropertyValue02'),
            'Details': [{
                'Status': 'I',
                'Message': 'Extra information'
            }]
        }]
        result = {'row': row}
        results.append(result)
    return json.dumps(results)


import json


def main():
    # 模拟的输入数据
    input_data = ('{"rcdata":"[{\"FacilityID\":\"875\",\"CustomerID\":\"CMPCPL0001\",\"ReferenceNo\":\"2900048569\",'
                  '\"PONo\":\"0153419212\",\"RC\":{\"WISECompanyID\":\"ORG-1\",\"CompanyID\":\"LT\",'
                  '\"FacilityID\":\"875\",\"CustomerID\":\"CMPCPL0001\",\"PONo\":\"0153419212\",'
                  '\"ReferenceNo\":\"2900048569\",\"WISEPOID\":\"RN-689\",'
                  '\"ReceivedDate\":\"2024-05-11T05:23:17.942\",\"ContainerNumber\":\"MSNU740305-5\",\"Note\":\"\",'
                  '\"Items\":[{\"POLineNo\":1,\"ItemNumber\":\"M100PLY000010\",\"ItemShortDescription\":\"t\",'
                  '\"ItemDescription\":\"t\",\"ReceivedQuantity\":644,\"CustomerMaterial\":\"\",\"ItemNote\":\"\",'
                  '\"SerialNumber\":[],\"LotNo\":\"\",\"DynTxtPropertyValue03\":\"GOOD\",\"SupplierID\":\"ORG-8166\",'
                  '\"SupplierName\":\"CMPC PLYWOOD\",\"TitleID\":\"CMPC PLYWOOD\",\"UOM\":\"EA\",\"ExpectedQty\":644,'
                  '\"ExpirationDate\":\"\",\"PalletQty\":1,\"BaseUOM\":\"EA\",\"ReceivedBaseQty\":644,'
                  '\"GoodsType\":\"GOOD\",\"ManufactureDate\":\"\"}],\"PalletQty\":1,\"Cartons\":[],'
                  '\"DynTxtPropertyValue01\":\"F\",\"DynTxtPropertyValue02\":\"LUMBER-PLYW\",'
                  '\"DynTxtPropertyValue03\":\"\",\"DynTxtPropertyValue04\":\"\",\"DynTxtPropertyValue05\":\"\",'
                  '\"DynTxtPropertyValue06\":\"\",\"DynTxtPropertyValue07\":\"\",\"DynTxtPropertyValue08\":\"\",'
                  '\"DynTxtPropertyValue09\":\"\",\"DynTxtPropertyValue10\":\"\",\"DynTxtPropertyValue11\":\"\",'
                  '\"DynTxtPropertyValue12\":\"\",\"DynTxtPropertyValue13\":\"\",\"DynTxtPropertyValue14\":\"\",'
                  '\"DynTxtPropertyValue15\":\"\",\"DynTxtPropertyValue16\":\"\",\"DynTxtPropertyValue17\":\"\",'
                  '\"DynTxtPropertyValue18\":\"\",\"DynTxtPropertyValue19\":\"\",\"DynTxtPropertyValue20\":\"\",'
                  '\"TitleID\":\"ORG-8166\",\"SupplierID\":\"CMPC PLYWOOD\",\"SupplierName\":\"CMPC PLYWOOD\",'
                  '\"BOLNo\":\"MEDUEJ109226\",\"SealStatus\":\"\",\"SCACCode\":\"UPSN\",\"CarrierName\":\"UPS\",'
                  '\"wiseCustomerId\":\"ORG-8166\",\"DockCheckIn\":\"2024-05-11T05:23:15.097\",'
                  '\"DockCheckOut\":\"2024-05-11T05:23:15.894\",\"ETA\":\"2023-12-19T00:00:00\",'
                  '\"Status\":\"Closed\"},\"CreatedWhen\":\"2024-05-11T09:24:18.007\"}]}"}')

    # 将 JSON 字符串转换为 Python 字典
    input_dict = json.loads(input_data)

    # 调用 run 函数，并打印输出结果
    output = run(input_dict)
    print(output)


if __name__ == "__main__":
    main()
