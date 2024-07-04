import hashlib


def sign(app_secret, param):
    s = app_secret + param + app_secret
    md5_hash = hashlib.md5(s.encode('utf-8')).hexdigest().upper()
    return md5_hash


# 示例用法
app_secret = "6cdb7b62e120aa135bd0f658ff687fb6"
param = ("{\"applyNo\":\"DPN20240517000035\",\"businessNo\":\"DPN20240517000035\",\"businessType\":10,"
         "\"callbackUrl\":\"https://bytesec.bytedance.com/api/router\",\"companyCode\":\"BYTED00001\","
         "\"invoiceDate\":\"2024-05-17 16:30:21\",\"invoiceNo\":\"SA20240517000027\","
         "\"logisticsCompanyName\":\"UPS\",\"logisticsCompanyNo\":\"UPS\",\"logisticsServiceName\":\"UPS "
         "NextDayAir\",\"logisticsServiceNo\":\"1DAY\",\"needPrintPackingList\":false,\"orderLineList\":[{"
         "\"lineNo\":1,\"qualityLevel\":1,\"quantity\":1,\"skuName\":\"UNIS_Product\",\"skuNo\":\"UNIS_Product\"}],"
         "\"partnerName\":\"H-OMS\",\"productList\":[],\"receiverInfo\":{\"receiverAddress\":\"Beautiful garden "
         "entrance\",\"receiverCity\":\"Autauga County\",\"receiverCountry\":\"美国\","
         "\"receiverCountryIdentifier\":\"US\",\"receiverDistrict\":\"Autaugaville\",\"receiverName\":\"King\","
         "\"receiverPhone\":\"18000000000\",\"receiverProvince\":\"Alabama\",\"receiverZipCode\":\"36003\","
         "\"taxFileNoCountry\":\"US\",\"taxFileNoType\":\"VAT\"},\"remark\":\"\",\"senderInfo\":{"
         "\"senderAddress\":\"beautiful street\",\"senderCity\":\"Autauga County\",\"senderCountry\":\"美国\","
         "\"senderCountryIdentifier\":\"US\",\"senderDistrict\":\"Autaugaville\",\"senderName\":\"kk\","
         "\"senderPhone\":\"18000000000\",\"senderProvince\":\"Alabama\",\"senderZipCode\":\"36003\"},"
         "\"shopName\":\"UNIS_Stores\",\"shopNo\":\"UNIS_Stores\",\"subType\":1,\"tradeTerms\":\"DDP\","
         "\"transactionNo\":\"unis_order_test\",\"warehouseNo\":\"ValleyView\"}")
sign_result = sign(app_secret, param)
print(sign_result == "1DD04FFC53F6FF6A4ADDBBF3C152ABB7")
