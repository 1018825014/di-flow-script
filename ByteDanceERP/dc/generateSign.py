import hashlib
import json
from datetime import datetime


def run(event_dict):
    app_key = event_dict['app_key']
    method = 'wms.outboundDetailNotify'
    app_secret = event_dict['app_secret']
    param_str = event_dict['param']

    sign_origin_str = f'appKey={app_key}&method={method}&params={param_str}'

    md5_hash = hashlib.md5((app_secret + sign_origin_str + app_secret).encode()).hexdigest().upper()

    # 获取当前时间
    now = datetime.now()

    # 格式化时间
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    res = {
        'sign': md5_hash,
        'timestamp': formatted_time
    }
    return json.dumps(res)


# 测试用例的实际值
event_dict = {
    "app_key": "67F03198D746CDBE",
    "param": "{\"businessNo\":\"CKTZ240627026369\",\"businessType\":\"60\",\"receiptNo\":\"SO100064355-1\","
             "\"operateTime\":\"1970-01-01 13:37:21\",\"warehouseNo\":\"889\",\"logisticsList\":[{\"weight\":0,"
             "\"length\":\"\",\"width\":\"\",\"height\":\"\",\"volume\":\"0.58\",\"logisticsCompanyNo\":\"UPSN\","
             "\"logisticsServiceNo\":\"GRND\",\"wayBillNo\":\"911406193997\",\"skuList\":[{\"lineNo\":\"1\","
             "\"skuNo\":\"UNIS_Product_1\",\"skuName\":\"UNIS_Product_1\",\"qualityLevel\":1,\"quantity\":2}]}],"
             "\"orderLineList\":[{\"lineNo\":\"1\",\"skuNo\":\"UNIS_Product_1\",\"qualityLevel\":1,\"quantity\":2,"
             "\"batchs\":[{\"batchNo\":\"Batch20240627\",\"quantity\":2}]}]}",
    "app_secret": "6cdb7b62e120aa135bd0f658ff687fb6"
}

# 调用函数并输出结果
result = run(event_dict)
result_dict = json.loads(result)

print("Generated Sign:", result_dict['sign'])
print(result)
