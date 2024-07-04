import unittest
import json

from ebay.ebayPackInven import run


# 确保替换为实际的模块和函数名

class TestRunFunction(unittest.TestCase):

    def test_normal_case(self):
        """ 测试常规情况，所有数据都是有效和正确的。 """
        event_dict = {
            'inventoryData': json.dumps([
                {'itemSku': '123', 'qty': 10},
                {'itemSku': '456', 'qty': 20}
            ]),
            'allProducts': json.dumps([
                {'sku': '123'},
                {'sku': '456'}
            ])
        }
        expected_output = json.dumps({
            'requests': [
                {'shipToLocationAvailability': {'quantity': 10}, 'sku': '123'},
                {'shipToLocationAvailability': {'quantity': 20}, 'sku': '456'}
            ]
        })
        self.assertEqual(run(event_dict), expected_output)

    def test_sku_not_in_inventory(self):
        """ 测试存在于产品列表但不在库存数据中的 SKU """
        event_dict = {
            'inventoryData': json.dumps([
                {'itemSku': '123', 'qty': 10}
            ]),
            'allProducts': json.dumps([
                {'sku': '123'},
                {'sku': '789'}
            ])
        }
        expected_output = json.dumps({
            'requests': [
                {'shipToLocationAvailability': {'quantity': 10}, 'sku': '123'}
            ]
        })
        self.assertEqual(run(event_dict), expected_output)

    def test_empty_input(self):
        """ 测试空输入情况 """
        event_dict = {
            'inventoryData': json.dumps([]),
            'allProducts': json.dumps([])
        }
        expected_output = {}  # 空字典作为返回值
        self.assertEqual(run(event_dict), expected_output)

    def test_invalid_json(self):
        """ 测试输入的 JSON 格式不正确 """
        event_dict = {
            'inventoryData': '[{\'itemSku\': \'123\', \'qty\': 10}]',  # 错误的 JSON 格式
            'allProducts': '[{\'sku\': \'123\'}]'
        }
        with self.assertRaises(json.JSONDecodeError):
            run(event_dict)

if __name__ == '__main__':
    unittest.main()
