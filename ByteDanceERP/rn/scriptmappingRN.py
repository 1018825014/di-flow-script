import json
from datetime import datetime


def run(data):
    # to json
    orderData = json.loads(data['orderData'])
    warehouseData = json.loads(data['warehouseData'])
    facilityName = None
    for warehouse in warehouseData:
        if warehouse['accountingCode'] == orderData.get('warehouseNo', ''):
            facilityName = warehouse['warehouseName']

    itemLines = []

    order_attach_data = {
        'SubReceiptType': orderData.get('subType', ''),
        'SCACCode': orderData.get('logisticsCompanyNo', ''),
        'CarrierName': orderData.get('logisticsCompanyName', ''),
        'DeliveryService': orderData.get('logisticsServiceNo', ''),
        'DynTxtPropertyValue04': orderData.get('logisticsServiceName', ''),
        'DynTxtPropertyValue05': orderData.get('tenantDominantNo', ''),
        'TrackingNo': orderData.get('wayBillNo', ''),
        'DynTxtPropertyValue07': orderData.get('callbackUrl', ''),

    }

    products = orderData.get('orderDetailList', {})

    for product in products:
        batches = product.get('batches', [])
        if batches:
            batchNo = batches[0].get('batchNo', '')
            if batchNo is not None and batchNo != '':
                for batch in batches:
                    item_attach_data = {
                        'POLineNo': product.get('lineNo', ''),
                        'DynTxtPropertyValue02': batch.get('batchName', ''),
                        'CountryOrigin': batch.get('originArea', '')
                    }
                    itemLine = {
                        'title': product.get('skuName', ''),
                        'sku': product.get('skuNo', ''),
                        'lotNo': batch.get('batchNo', ''),
                        'snList': batch.get('snNoList', []),
                        'qty': batch.get('quantity', 0),
                        'productAttachData': json.dumps(item_attach_data)
                    }
                    itemLines.append(itemLine)

        else:
            item_attach_data = {
                'POLineNo': product.get('lineNo', ''),

            }
            itemLine = {
                'sku': product.get('skuNo', ''),
                'title': product.get('skuName', ''),
                'qty': product.get('quantity', 0),
                'snList': product.get('snNoList', []),
                'orderItemAttachData': json.dumps(item_attach_data)
            }
            itemLines.append(itemLine)

    receiptType = str(orderData.get('businessType', ''))
    if receiptType in ['10', '40', '60']:
        receiptType = 'Regular Receipt'
    elif receiptType in ['20', '50', '70', '80']:
        receiptType = 'Return From End User'

    resultData = {
        'recipientName': orderData.get('CompanyCode', ''),
        'referenceNo': orderData.get('businessNo', ''),
        'receiptType': receiptType,
        'vendorNo': orderData.get('supplierCode', ''),
        'vendorName': orderData.get('supplierName', ''),
        'remark': orderData.get('remark', ''),
        'rawData': json.dumps(orderData),
        'sourceType': 1,
        'tenantId': data.get('tenantId', ''),
        'merchantId': data.get('merchantId', ''),
        'channelId': data.get('channelId', ''),
        'channelName': data.get('channelName', ''),
        'dataChannel': 'BYTEDANCE_ERP',
        'status': 'Imported',
        'facilityCode': orderData.get('warehouseNo', ''),
        'facilityName': facilityName,
        'products': itemLines,

        'attachData': json.dumps(order_attach_data)
    }

    return json.dumps(resultData)


def test_run():
    # Sample input data
    data = {
        "warehouseData": "[{\"id\":\"1803666791369519106\",\"merchantId\":\"1800825780248997890\",\"sort\":1,"
                         "\"warehouseCode\":\"F1\",\"warehouseName\":\"Valley View\",\"warehouseType\":2,"
                         "\"accountingCode\":\"889\",\"customerCode\":\"ZJTLLC0001\",\"city\":\"Buena Park\","
                         "\"state\":\"CA\",\"country\":\"USA\",\"zipCode\":\"90620\",\"email\":\"test@unisco.com\","
                         "\"status\":\"Enable\",\"enable\":true,\"isDefault\":false}]",
        "merchantId": "1800825780248997890",
        "tenantId": "1782713020027588610",
        "orderData": "{\"CompanyCode\":\"BYTED00001\",\"warehouseNo\":\"889\",\"businessNo\":\"businessNo104\","
                     "\"businessType\":10,\"callbackUrl\":\"https://bytesec.bytedance.com/api/router\","
                     "\"supplierCode\":\"supplierCode1\",\"supplierName\":\"supplierName1\","
                     "\"subType\":\"SA20240517000027\",\"logisticsCompanyName\":\"UPS\","
                     "\"logisticsCompanyNo\":\"UPSN\",\"logisticsServiceName\":\"UPS NextDayAir\","
                     "\"logisticsServiceNo\":\"GRND\",\"remark\":\"remark1\",\"tenantDominantNo\":1001,"
                     "\"orderDetailList\":[{\"lineNo\":1001,\"qualityLevel\":1,\"quantity\":1001,"
                     "\"skuName\":\"UNIS_Product\",\"skuNo\":\"UNIS_Product\",\"batches\":[{\"batchNo\":\"batche1\","
                     "\"batchName\":\"bname1\",\"originArea\":\"area\",\"quantity\":2,\"snNoList\":[\"batche1sn1\","
                     "\"batche1sn2\"]},{\"batchNo\":\"bnxxx\",\"batchName\":\"bname2\",\"originArea\":\"area\","
                     "\"quantity\":2,\"snNoList\":[\"batche2sn1\",\"batche2sn2\"]}],\"snNoList\":[\"PA7LXXXX\","
                     "\"PA7LXXXa\"]}]}",
        "channelName": "Fuzheng-Test-ByteDance",
        "channelId": "1800828358798045185"
    }

    # Run the function
    result = run(data)

    # Print the output
    print(json.dumps(json.loads(result), indent=4))


# Call the test function
test_run()
