import json
from datetime import datetime


def run(data):
    # to json
    orderData = json.loads(data['orderData'])

    itemLines = []
    # 获取当前UTC时间
    now = datetime.utcnow()
    formatted_time = now.strftime('%Y-%m-%dT%H:%M:%S.') + ('%03d' % (now.microsecond // 1000))
    timezone_formatted = '+00:00'
    final_formatted_time = formatted_time + timezone_formatted

    orderDate = orderData.get('invoiceDate', '')
    # 检查 orderDate 是否为空
    if orderDate:
        # 解析输入时间字符串为 datetime 对象
        dt = datetime.strptime(orderDate, '%Y-%m-%d %H:%M:%S')
        # 转换为所需格式
        isoOrderDate = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        isoOrderDate = now.strftime('%Y-%m-%dT%H:%M:%SZ')

    shipToAddress = {
        'name': orderData.get('receiverInfo', {}).get('receiverName', ''),
        'address1': orderData.get('receiverInfo', {}).get('receiverDistrict', ''),
        'address2': orderData.get('receiverInfo', {}).get('receiverAddress', ''),
        'phone': orderData.get('receiverInfo', {}).get('receiverPhone', ''),
        'city': orderData.get('receiverInfo', {}).get('receiverCity', ''),
        'state': orderData.get('receiverInfo', {}).get('receiverProvince', ''),
        'zipCode': orderData.get('receiverInfo', {}).get('receiverZipCode', ''),
        'country': orderData.get('receiverInfo', {}).get('receiverCountry', '')
    }
    shipFromAddress = {
        'firstName': orderData.get('senderInfo', {}).get('senderName', ''),
        'address1': orderData.get('senderInfo', {}).get('senderDistrict', ''),
        'address2': orderData.get('senderInfo', {}).get('senderAddress', ''),
        'phone': orderData.get('senderInfo', {}).get('senderPhone', ''),
        'city': orderData.get('senderInfo', {}).get('senderCity', ''),
        'state': orderData.get('senderInfo', {}).get('senderProvince', ''),
        'zipCode': orderData.get('senderInfo', {}).get('senderZipCode', ''),
        'country': orderData.get('senderInfo', {}).get('senderCountry', '')
    }

    carrier = {
        'name': orderData.get('logisticsCompanyName', ''),
        'scac': orderData.get('logisticsCompanyNo', '')
    }
    OrderType = str(orderData.get('businessType', ''))
    ShipMethod = 'Small Parcel'
    if OrderType in ['10']:
        OrderType = 'DropShip Order'
        ShipMethod = 'Small Parcel'
    elif OrderType in ['20', '30', '60']:
        OrderType = 'Regular Order'
        ShipMethod = 'LTL'
    order_attach_data = {
        'RetailerName': orderData.get('partnerName', ''),
        'TitleId': orderData.get('companyCode', ''),
        'OrderType': OrderType,
        'SubOrderType': orderData.get('businessType', ''),
        'SCACCode': orderData.get('logisticsCompanyNo', ''),
        'CarrierName': orderData.get('logisticsCompanyName', ''),
        'DeliveryService': orderData.get('logisticsServiceNo', ''),
        'MISC02': orderData.get('logisticsServiceName', ''),
        'MISC03': orderData.get('receiverCountryIdentifier', ''),  # 使用 get 方法并提供默认值
        'MISC04': orderData.get('receiverTaxNo', ''),  # 使用 get 方法并提供默认值
        'MISC14': orderData.get('shopNo', ''),
        'MISC15': orderData.get('wmsShopNo', ''),
        'MISC16': orderData.get('callbackUrl', ''),
        'note': orderData.get('remark', ''),
        'RequirePrintPackingList': orderData.get('needPrintPackingList', ''),
        'shipFromAddress': shipFromAddress
    }

    products = orderData.get('orderLineList', {})

    for product in products:
        batches = product.get('batches', [])
        extension = product.get('extension', {})
        if batches:
            batchNo = batches[0].get('batchNo', '')
            if batchNo is not None and batchNo != '':
                for batch in batches:
                    item_attach_data = {
                        'sn': batch.get('snNoList', []),
                        'GoodsType': product.get('qualityLevel', ''),
                        'DTLMISC02': batch.get('batchName', ''),
                        'DTLMISC03': batch.get('originArea', ''),
                        'DTLMISC04': extension.get('so', ''),
                        'DTLMISC05': extension.get('price', 0),
                        'DTLMISC06': extension.get('currency', ''),
                        'DTLMISC07': extension.get('supplierItem', ''),
                        'DTLMISC08': extension.get('customerItem', ''),
                        'DTLMISC09': extension.get('customerPo', '')
                    }
                    itemLine = {
                        'poLineNo': product.get('lineNo', ''),
                        'itemDescription': product.get('skuName', ''),
                        'itemSku': product.get('skuNo', ''),
                        'lotNo': batch.get('batchNo', ''),
                        'qty': batch.get('quantity', 0),
                        'orderItemAttachData': json.dumps(item_attach_data)
                    }
                    itemLines.append(itemLine)

        else:
            item_attach_data = {
                'sn': product.get('snNoList', []),
                'GoodsType': product.get('qualityLevel', ''),
                'DTLMISC04': extension.get('so', ''),
                'DTLMISC05': extension.get('price', 0),
                'DTLMISC06': extension.get('currency', ''),
                'DTLMISC07': extension.get('supplierItem', ''),
                'DTLMISC08': extension.get('customerItem', ''),
                'DTLMISC09': extension.get('customerPo', '')
            }
            itemLine = {
                'poLineNo': product.get('lineNo', ''),
                'itemDescription': product.get('skuName', ''),
                'itemSku': product.get('skuNo', ''),
                'qty': product.get('quantity', 0),
                'orderItemAttachData': json.dumps(item_attach_data)
            }
            itemLines.append(itemLine)

    businessNo = orderData.get('businessNo', {})
    salesOrderNo = orderData.get('salesOrderNo', '')
    if not salesOrderNo:
        salesOrderNo = businessNo
    resultData = {
        'rawData': json.dumps(orderData),
        'source': 'DI',
        'tenantId': data.get('tenantId', ''),
        'merchantId': data.get('merchantId', ''),
        'channelId': data.get('channelId', ''),
        'channelName': data.get('channelName', ''),
        'dataChannel': 'BYTEDANCE_ERP',
        'status': 'Imported',
        'orderDate': isoOrderDate,
        'referenceNo': orderData.get('businessNo', ''),
        'purchaseOrderNo': orderData.get('businessNo', ''),
        'channelSalesOrderNumber': salesOrderNo,
        'carrier': carrier,
        'buyerFirstName': orderData.get('receiverName', ''),
        'shipMethod': ShipMethod,
        'loadDate': final_formatted_time,
        'deliveryService': orderData.get('logisticsServiceNo', ''),
        'shipToAddress': shipToAddress,
        'shipFromAddress': shipFromAddress,
        'itemLines': itemLines,
        'orderAttachData': json.dumps(order_attach_data),
        'freightTerm': 'Collect'
    }

    return json.dumps(resultData)


def test_run():
    # Sample input data
    data = {
        "merchantId": "1797216678122557442",
        "tenantId": "1782713020027588610",
        "orderData": "{\"companyCode\":\"BYTED00001\",\"warehouseNo\":\"889\",\"businessNo\":\"DPN20240517000035\",\"salesOrderNo\":\"salesOrderNo001\",\"transactionNo\":\"unis_order_test\",\"partnerName\":\"H-OMS\",\"businessType\":10,\"subType\":1,\"applyNo\":\"DPN20240517000035\",\"logisticsCompanyName\":\"UPS\",\"logisticsCompanyNo\":\"UPS\",\"logisticsServiceName\":\"UPS NextDayAir\",\"logisticsServiceNo\":\"1DAY\",\"shopNo\":\"UNIS_Stores\",\"wmsShopNo\":\"wmsShopNo\",\"remark\":\"remark001\",\"needPrintPackingList\":true,\"callbackUrl\":\"https://bytesec.bytedance.com/api/router\",\"invoiceDate\":\"2024-05-17 16:30:21\",\"invoiceNo\":\"SA20240517000027\",\"orderLineList\":[{\"lineNo\":1001,\"qualityLevel\":1,\"quantity\":1001,\"skuName\":\"UNIS_Product\",\"skuNo\":\"UNIS_Product\",\"batches\":[{\"batchNo\":\"batche1\",\"batchName\":\"bname1\",\"originArea\":\"area\",\"quantity\":2,\"snNoList\":[\"batche1sn1\",\"batche1sn2\"]},{\"batchNo\":\"bnxxx\",\"batchName\":\"bname2\",\"originArea\":\"area\",\"quantity\":2,\"snNoList\":[\"batche2sn1\",\"batche2sn2\"]}],\"snNoList\":[\"PA7LXXXX\",\"PA7LXXXa\"],\"extension\":{\"so\":\"ex-so\",\"price\":\"ex-price\",\"currency\":\"ex-currency\",\"supplierItem\":\"ex-supplierItem\",\"customerItem\":\"ex-customerItem\",\"customerPo\":\"ex-customerPo\"}}],\"productList\":[],\"receiverInfo\":{\"receiverAddress\":\"Beautiful garden entrance\",\"receiverCity\":\"Autauga County\",\"receiverCountry\":\"美国\",\"receiverCountryIdentifier\":\"US\",\"receiverDistrict\":\"Autaugaville\",\"receiverName\":\"King\",\"receiverPhone\":\"18000000000\",\"receiverProvince\":\"Alabama\",\"receiverZipCode\":\"36003\",\"taxFileNoCountry\":\"US\",\"taxFileNoType\":\"VAT\"},\"senderInfo\":{\"senderAddress\":\"beautiful street\",\"senderCity\":\"Autauga County\",\"senderCountry\":\"美国\",\"senderCountryIdentifier\":\"US\",\"senderDistrict\":\"Autaugaville\",\"senderName\":\"kk\",\"senderPhone\":\"18000000000\",\"senderProvince\":\"Alabama\",\"senderZipCode\":\"36003\"},\"tradeTerms\":\"DDP\"}",
        "channelName": "gpbd",
        "channelId": "1797499945683369985"
    }

    # Run the function
    result = run(data)

    # Print the output
    print(json.dumps(json.loads(result), indent=4))


# Call the test function
test_run()
