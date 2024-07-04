import hashlib
import json


def run(event_dict):
    app_secret = event_dict.get('app_secret', '')
    param = event_dict.get('param', '')
    sign = event_dict.get('sign', '')
    s = app_secret + param + app_secret
    md5_hash = hashlib.md5(s.encode('utf-8')).hexdigest().upper()
    if md5_hash == sign:
        return 'varifyPass:' + sign
    else:
        return 'varifyFail:' + md5_hash


if __name__ == '__main__':
    data = {
        "param": "{\"applyNo\":\"DPN20240517000035\",\"businessNo\":\"DPN20240517000030\",\"businessType\":10,\"callbackUrl\":\"https://bytesec.bytedance.com/api/router\",\"companyCode\":\"BYTED00001\",\"invoiceDate\":\"2024-05-17 16:30:21\",\"invoiceNo\":\"SA20240517000027\",\"logisticsCompanyName\":\"UPS\",\"logisticsCompanyNo\":\"UPS\",\"logisticsServiceName\":\"UPS NextDayAir\",\"logisticsServiceNo\":\"1DAY\",\"needPrintPackingList\":false,\"orderLineList\":[{\"lineNo\":1,\"qualityLevel\":1,\"quantity\":1,\"skuName\":\"UNIS_Product\",\"skuNo\":\"UNIS_Product\"}],\"partnerName\":\"H-OMS\",\"productList\":[],\"receiverInfo\":{\"receiverAddress\":\"Beautiful garden entrance\",\"receiverCity\":\"Autauga County\",\"receiverCountry\":\"美国\",\"receiverCountryIdentifier\":\"US\",\"receiverDistrict\":\"Autaugaville\",\"receiverName\":\"King\",\"receiverPhone\":\"18000000000\",\"receiverProvince\":\"Alabama\",\"receiverZipCode\":\"36003\",\"taxFileNoCountry\":\"US\",\"taxFileNoType\":\"VAT\"},\"remark\":\"\",\"senderInfo\":{\"senderAddress\":\"beautiful street\",\"senderCity\":\"Autauga County\",\"senderCountry\":\"美国\",\"senderCountryIdentifier\":\"US\",\"senderDistrict\":\"Autaugaville\",\"senderName\":\"kk\",\"senderPhone\":\"18000000000\",\"senderProvince\":\"Alabama\",\"senderZipCode\":\"36003\"},\"shopName\":\"UNIS_Stores\",\"shopNo\":\"UNIS_Stores\",\"subType\":1,\"tradeTerms\":\"DDP\",\"transactionNo\":\"unis_order_test\",\"warehouseNo\":\"ValleyView\"}",
        "sign": "58F82AC1772B6C437B1740BDA7D0BCE4",
        "app_secret": "6cdb7b62e120aa135bd0f658ff687fb6"}
    print(run(data))
