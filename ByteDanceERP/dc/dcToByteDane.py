import json
import datetime
import copy


def run(event_dict):
    # 将 false 替换为 False
    shipmentData = json.loads(event_dict['shipmentData'])

    omsShipDate = shipmentData.get('shipDate')
    # 将时间戳转换为秒
    timestamp_in_seconds = omsShipDate / 1000
    # 创建UTC时间的datetime对象
    utc_dt = datetime.datetime.utcfromtimestamp(timestamp_in_seconds)
    # 转换为UTC+8时区
    utc_plus_8_dt = utc_dt + datetime.timedelta(hours=8)
    # 格式化日期时间
    formatted_date_time = utc_plus_8_dt.strftime('%Y-%m-%d %H:%M:%S')

    packages = shipmentData.get('packages', [])
    logisticsList = []
    orderLineList = []
    for package in packages:
        itemLines = package.get('itemLines', [])
        sku_dict = {}
        for itemLine in itemLines:
            comma_separated_string = itemLine.get('sn', '')
            snList = comma_separated_string.split(',') if comma_separated_string else []
            lineNo = itemLine.get('poLineNo', '')
            if lineNo is None:
                return 'lineNo is null.'
            skuNo = itemLine.get('itemSku', '')
            skuName = itemLine.get('shipmentItemAttachData', {}).get('skuName', '')
            quantity = itemLine.get('shippedQty', '')
            lotNo = itemLine.get('lotNo', '')

            if lineNo in sku_dict:
                existing_sku = sku_dict[lineNo]
                if existing_sku['skuNo'] != skuNo or existing_sku['skuName'] != skuName:
                    return f'Conflict found for lineNo {lineNo}: different skuNo or skuName.'

                existing_sku['quantity'] += quantity
                if snList:
                    existing_sku['snList'].extend(copy.deepcopy(snList))
            else:
                sku_dict[lineNo] = {
                    'lineNo': lineNo,
                    'skuNo': skuNo,
                    'skuName': skuName,
                    'qualityLevel': 1,
                    'quantity': quantity
                }
                if snList:
                    sku_dict[lineNo]['snList'] = copy.deepcopy(snList)
        skuList = [sku for sku in sku_dict.values()]

        logistic = {
            'weight': package.get('weight', ''),
            'length': package.get('length', ''),
            'width': package.get('width', ''),
            'height': package.get('height', ''),
            'volume': package.get('volume', ''),
            'logisticsCompanyNo': shipmentData.get('carrier', {}).get('scac', ''),
            'logisticsServiceNo': shipmentData.get('deliveryService', ''),
            'wayBillNo': package.get('trackingNumber', ''),
            'skuList': skuList
        }
        logisticsList.append(logistic)

    # 构造orderlinelist
    sku_dict = {}
    for package in packages:
        itemLines = package.get('itemLines', [])
        for itemLine in itemLines:
            comma_separated_string = itemLine.get('sn', '')
            snList = comma_separated_string.split(',') if comma_separated_string else []
            lineNo = itemLine.get('poLineNo', '')
            if lineNo is None:
                return 'lineNo is null.'
            skuNo = itemLine.get('itemSku', '')
            quantity = itemLine.get('shippedQty', 0)
            lotNo = itemLine.get('lotNo', '')

            if lineNo in sku_dict:
                existing_sku = sku_dict[lineNo]
                if existing_sku['skuNo'] != skuNo:
                    return f'Conflict found for lineNo {lineNo}: different skuNo.'

                existing_sku['quantity'] += quantity
                if snList:
                    if 'snList' not in existing_sku:
                        existing_sku['snList'] = []
                    existing_sku['snList'].extend(copy.deepcopy(snList))
                if lotNo:
                    found = False
                    for batch in existing_sku.get('batchs', []):
                        if batch['batchNo'] == lotNo:
                            batch['quantity'] += quantity
                            if snList:
                                batch['snNoList'].extend(copy.deepcopy(snList))
                            found = True
                            break
                    if not found:
                        newBatch = {
                            'batchNo': lotNo,
                            'quantity': quantity
                        }
                        if snList:
                            newBatch['snNoList'] = copy.deepcopy(snList)
                        existing_sku['batchs'].append(newBatch)
            else:
                batchs = []
                if lotNo:
                    batch = {
                        'batchNo': lotNo,
                        'quantity': quantity
                    }
                    if snList:
                        batch['snNoList'] = copy.deepcopy(snList)
                    batchs.append(batch)
                sku_dict[lineNo] = {
                    'lineNo': lineNo,
                    'skuNo': skuNo,
                    'qualityLevel': 1,
                    'quantity': quantity
                }
                if snList:
                    sku_dict[lineNo]['snList'] = copy.deepcopy(snList)
                if batchs:
                    sku_dict[lineNo]['batchs'] = copy.deepcopy(batchs)

    for lineNo, sku in sku_dict.items():
        orderLine = {
            'lineNo': sku['lineNo'],
            'skuNo': sku['skuNo'],
            'qualityLevel': sku['qualityLevel'],
            'quantity': sku['quantity']
        }
        if 'snList' in sku and sku['snList'] and sku['snList'] != ['']:
            orderLine['snNoList'] = copy.deepcopy(sku['snList'])
        if 'batchs' in sku and sku['batchs']:
            orderLine['batchs'] = [batch for batch in sku['batchs']]
        orderLineList.append(orderLine)

    param = {
        'businessNo': shipmentData.get('purchaseOrderNo', ''),
        'businessType': shipmentData.get('shipmentAttachData', {}).get('businessType', ''),
        'receiptNo': shipmentData.get('dispatchNo', ''),
        'operateTime': formatted_date_time,
        'warehouseNo': shipmentData.get('accountingCode', ''),
        'logisticsList': logisticsList,
        'orderLineList': orderLineList
    }
    result = {
        'param': param,
        'callbackUrl': shipmentData.get('orderAttachData', {}).get('MISC16', '')
    }
    return json.dumps(result)


def main():
    # Sample event_dict with shipmentData
    event_dict = {
        'shipmentData': "{\"shipmentId\":\"1806630385327620098\",\"shipmentNo\":\"SP00001316\","
                        "\"orderId\":\"1806168541023846402\",\"orderNo\":\"SO100064355\","
                        "\"dispatchNo\":\"SO100064355-1\",\"merchantId\":\"1800825780248997890\","
                        "\"tenantId\":\"1782713020027588610\",\"referenceNo\":\"CKTZ240627026369\","
                        "\"channelId\":\"1800828358798045185\",\"channelName\":\"Fuzheng-Test-ByteDance\","
                        "\"dataChannel\":\"BYTEDANCE_ERP\",\"purchaseOrderNo\":\"CKTZ240627026369\","
                        "\"channelSalesOrderNumber\":\"CKTZ240627026369\",\"status\":\"New\",\"shipMethod\":\"Small "
                        "Parcel\",\"masterTrackingNumber\":\"911406193997\",\"proNumber\":\"911406193997\","
                        "\"accountingCode\":\"889\",\"warehouseName\":\"Valley View\",\"carrier\":{\"name\":\"UPS\","
                        "\"scac\":\"UPSN\"},\"deliveryService\":\"GRND\",\"shipFromAddress\":{\"address1\":\"6800 "
                        "Valley View St.\",\"address2\":\"address2\",\"city\":\"Buena Park\",\"state\":\"CA\","
                        "\"zipCode\":\"90620\",\"country\":\"USA\"},\"shipToAddress\":{\"name\":\"kk\","
                        "\"address1\":\"昌平区\",\"address2\":\"beautiful street\",\"city\":\"北京市\",\"state\":\"北京市\","
                        "\"zipCode\":\"\",\"country\":\"中国\"},\"shipDate\":20241000,\"sourceType\":0,"
                        "\"shipmentAttachData\":{\"Items\":[{\"ItemNumber\":\"UNIS_Product_1\",\"OrderedQty\":2,"
                        "\"ShippedQty\":2,\"DifferenceQty\":0,\"UOM\":\"EA\",\"UPC\":\"\",\"Weight\":0,"
                        "\"CFT\":1.1574,\"WeightUnitCode\":\"L\",\"LineNo\":\"1\",\"SupplierID\":\"\","
                        "\"TitleID\":\"ZJTD LLC\",\"LotNo\":\"Batch20240627\",\"UnitPrice\":\"\",\"DTLMISC01\":\"\","
                        "\"DTLMISC02\":\"Batch20240627\",\"DTLMISC03\":\"\",\"DTLMISC04\":\"\",\"DTLMISC05\":\"\","
                        "\"DTLMISC06\":\"\",\"DTLMISC07\":\"\",\"DTLMISC08\":\"\",\"DTLMISC09\":\"\","
                        "\"DTLMISC10\":\"\",\"DTLMISC11\":\"\",\"DTLMISC12\":\"\",\"DTLMISC13\":\"\","
                        "\"DTLMISC14\":\"\",\"DTLMISC15\":\"\",\"DTLMISC16\":\"\",\"DTLMISC17\":\"\","
                        "\"DTLMISC18\":\"\",\"DTLMISC19\":\"\",\"DTLMISC20\":\"\",\"DTLMISC21\":\"\","
                        "\"DTLMISC22\":\"\",\"DTLMISC23\":\"\",\"DTLMISC24\":\"\",\"DTLMISC25\":\"\","
                        "\"OriginalDynamic\":{\"dynTxtPropertyValue02\":\"Batch20240627\"},\"EAN\":\"\","
                        "\"DigitBarcode14\":\"\",\"Description\":\"UNIS_Product_1\",\"Color\":\"\",\"Size\":\"\","
                        "\"Pack\":\"\",\"SizeOfEDI\":\"\",\"EnteredUOM\":\"EA\",\"PalletTiHiQty\":0,"
                        "\"BaseUOM\":\"EA\",\"ShippedBaseQty\":2,\"ReturnLabel\":\"N\",\"GoodsType\":\"GOOD\"}],"
                        "\"callbackUrl\":\"https://bytesec.bytedance.com/api/router\",\"businessType\":\"60\"},"
                        "\"orderAttachData\":{\"MISC04\":\"\",\"MISC15\":\"\",\"RequirePrintPackingList\":false,"
                        "\"SCACCode\":\"UPSN\",\"MISC16\":\"https://bytesec.bytedance.com/api/router\",\"note\":\"\","
                        "\"CarrierName\":\"UPS\",\"RetailerName\":\"\",\"OrderType\":\"DropShip Order\","
                        "\"shipFromAddress\":{\"zipCode\":\"36003\",\"country\":\"美国\",\"address2\":\"beautiful "
                        "street\",\"city\":\"Autauga County\",\"address1\":\"Autaugaville\",\"firstName\":\"kk\","
                        "\"phone\":\"18000000000\",\"state\":\"Alabama\"},\"DeliveryService\":\"GRND\","
                        "\"TitleId\":\"BYTED00001\",\"SubOrderType\":60,\"MISC02\":\"UPS GRND\",\"MISC03\":\"\","
                        "\"MISC14\":\"\"},\"createTime\":1719569224000,\"updateTime\":1719569224000,\"itemLines\":[{"
                        "\"shipmentItemLineId\":\"1806630385453449218\",\"shipmentId\":\"1806630385327620098\","
                        "\"referenceNo\":\"CKTZ240627026369\",\"poLineNo\":\"1\",\"itemName\":\"UNIS_Product_1\","
                        "\"itemSku\":\"UNIS_Product_1\",\"uom\":\"EA\",\"linearUom\":\"INCH\","
                        "\"weightUom\":\"POUND\",\"weight\":0,\"volume\":\"0.5787\","
                        "\"masterTrackingNumber\":\"911406193997\",\"trackingNumber\":\"911406193997\","
                        "\"shippedQty\":2,\"shippedQtySum\":2,\"shipmentItemAttachData\":{\"qualityLevel\":1,"
                        "\"skuName\":\"UNIS_Product_1\"},\"lotNo\":\"Batch20240627\",\"sn\":\"\"}],\"packages\":[{"
                        "\"shipmentPackageId\":\"1806630385386340354\",\"shipmentId\":\"1806630385327620098\","
                        "\"orderId\":\"1806168541023846402\",\"trackingNumber\":\"911406193997\","
                        "\"linearUom\":\"INCH\",\"weightUom\":\"POUND\",\"weight\":0,\"volume\":\"0.58\","
                        "\"masterTrackingNumber\":\"911406193997\",\"carrierName\":\"UPS\",\"itemLines\":[{"
                        "\"shipmentItemLineId\":\"1806630385453449218\",\"shipmentId\":\"1806630385327620098\","
                        "\"referenceNo\":\"CKTZ240627026369\",\"poLineNo\":\"1\",\"itemName\":\"UNIS_Product_1\","
                        "\"itemSku\":\"UNIS_Product_1\",\"uom\":\"EA\",\"linearUom\":\"INCH\","
                        "\"weightUom\":\"POUND\",\"weight\":0,\"volume\":\"0.5787\","
                        "\"masterTrackingNumber\":\"911406193997\",\"trackingNumber\":\"911406193997\","
                        "\"shippedQty\":2,\"shipmentItemAttachData\":{\"qualityLevel\":1,"
                        "\"skuName\":\"UNIS_Product_1\"},\"lotNo\":\"Batch20240627\",\"sn\":\"\"}]}]}"
    }

    # Run the function
    output = run(event_dict)
    # Print the output
    print(output)


if __name__ == "__main__":
    main()
