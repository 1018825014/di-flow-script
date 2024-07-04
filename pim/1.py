import math
import base64
import json
from datetime import datetime, timedelta


def run(data):
    resultData = []

    # to json
    productJson = json.loads(data['shopifyProduct'])
    productVariantJsonArr = productJson.get('variants')
    productImageJsonArr = productJson.get('images')

    # 处理变体数据
    for productVariantJson in productVariantJsonArr:
        # title
        title = ''
        productTitle = productJson.get('title')
        productVariantTitle = productVariantJson.get('title')

        if productTitle is not None:
            title = title + productTitle
        if productVariantTitle is not None and productVariantTitle.lower() != 'Default Title'.lower():
            title = title + ' - ' + productVariantTitle

        # image obj array
        productImages = []
        productVariantImageId = productVariantJson.get('image_id')

        if productVariantImageId is not None:
            for productImageJson in productImageJsonArr:
                productImageId = productImageJson.get('id')
                if productVariantImageId == productImageId:
                    productImageName = productImageJson.get('alt')
                    if productImageName is None:
                        productImageName = ''
                    productImageUrl = productImageJson.get('src')
                    if productImageUrl is not None and productImageUrl != '':
                        productImages.append({
                            'name': productImageName,
                            'url': productImageUrl,
                        })

        description = title
        vendor = productJson.get('vendor')
        if vendor is not None and vendor != '':
            description = vendor + ' | ' + description

        channelSource = 'Shopify' + '(' + data['channelName'] + ')'

        po = {
            'tenantId': data['tenantId'],
            'merchantId': data['merchantId'],
            'channelId': data['channelId'],
            'productReferenceNo': productJson.get('id'),
            'skuReferenceNo': productVariantJson.get('id'),
            'sku': productVariantJson.get('sku'),

            'title': title,
            'productTags': productJson.get('tags'),
            'description': description,
            'productImages': productImages,
            'pricing': productVariantJson.get('price'),
            # 三维处理
            'length': productVariantJson.get('length'),
            'width': productVariantJson.get('width'),
            'height': productVariantJson.get('height'),
            'uomDimensions': productVariantJson.get('dimensions_unit'),
            # 重量处理
            'weight': productVariantJson.get('weight'),
            'uomWeight': productVariantJson.get('weight_unit'),
            'length': productVariantJson.get('length'),
            'channelSource': channelSource,
            'barcode': productVariantJson.get('barcode'),
            'inventoryQuantity': productVariantJson.get('inventory_quantity')
        }

        resultData.append(po)

    # result
    return json.dumps(resultData)


if __name__ == '__main__':
    data = {
        "order_id": "1743",
        "is_parent_order": "N",
        "parent_order_id": "0",
        "company_id": "56",
        "user_id": "74",
        "total": "19.20",
        "subtotal": 24,
        "discount": 0,
        "subtotal_discount": 4.8,
        "payment_surcharge": 0,
        "shipping_ids": "24",
        "shipping_cost": "0.00",
        "timestamp": "1711701996",
        "status": "O",

        "promotions": {
            "15": {
                "bonuses": [
                    {
                        "bonus": "order_discount",
                        "discount_bonus": "by_percentage",
                        "discount_value": "20",
                        "promotion_id": "15"
                    }
                ],
                "total_discount": 4.8,
                "name": "20% discount coupon",
                "short_description": ""
            }
        },
        "promotion_ids": "15",
        "firstname": "1",
        "lastname": "M",
        "company": "",
        "b_firstname": "1",
        "b_lastname": "",
        "b_address": "1",
        "b_address_2": "",
        "b_city": "1111",
        "b_county": "",
        "b_state": "CA",
        "b_country": "US",
        "b_zipcode": "01342",
        "b_phone": "+1(111)111-1111",
        "s_firstname": "1111",
        "s_lastname": "1111",
        "s_address": "1111",
        "s_address_2": "",
        "s_city": "1111",
        "s_county": "",
        "s_state": "CA",
        "s_country": "US",
        "s_zipcode": "01342",
        "s_phone": "+1(111)111-1111",
        "s_address_type": "",
        "p_firstname": "bassel",
        "p_lastname": "a",
        "p_email": "basselunis@gmail.com",
        "phone": "+1(111)111-1111",
        "fax": "",
        "url": "",
        "email": "basselunis@gmail.com",
        "payment_id": "17",
        "tax_exempt": "N",
        "lang_code": "en",
        "ip_address": "63.222.121.45",
        "repaid": "0",
        "validation_code": "",
        "localization_id": "0",
        "pickup_person_id": "8",
        "profile_id": "75",
        "storefront_id": "1",
        "updated_at": "1711701996",
        "fulfillment_status": "U",
        "payment_status": "U",
        "payment_amount": "0.00",
        "delivery_type": "pickup",
        "business_type": "M",
        "booked_start_at": "0",
        "booked_end_at": "0",
        "deposit_amount": "0.00",
        "order_method": "buy_it_now",
        "payment_method": {
            "payment_id": "17",
            "company_id": "0",
            "usergroup_ids": "0",
            "position": "4",
            "status": "A",
            "template": "views/orders/components/payments/empty.tpl",
            "processor_id": "0",
            "a_surcharge": "0.000",
            "p_surcharge": "0.000",
            "tax_ids": [],
            "localization": "",
            "payment_category": "tab1",
            "payment": "Pay later",
            "description": "",
            "instructions": "<p>Pay later: Please visit the seller’s detail page or directly contact the seller to check how to pay directly to the seller later.</p>",
            "surcharge_title": "",
            "lang_code": "en",
            "processor": 1,
            "processor_type": 1,
            "processor_status": 1,
            "image": [],
            "storefront_ids": ""
        },
        "fields": [],
        "products": {
            "3463773863": {
                "item_id": "3463773863",
                "order_id": "1743",
                "product_id": "4925",
                "product_code": "EA",
                "price": "12.00",
                "amount": "2",
                "extra": {
                    "product_options": [],
                    "unlimited_download": "N",
                    "updated_timestamp": "1710819282",
                    "return_period": "10",
                    "product": "test a doll",
                    "company_id": "56",
                    "is_edp": "N",
                    "edp_shipping": "N",
                    "base_price": 12,
                    "stored_price": "N",
                    "average_tax_value": 0,
                    "average_shipping_cost": 0,
                    "average_discount_applied": 4.8
                },
                "business_type": "M",
                "item_name": "test a doll",
                "status": "O",
                "created_at": "1711701996",
                "update_at": "0",
                "display_subtotal": 24,
                "snapshot_id": "55",
                "product": "test a doll (Single Item (Sell Per Piece), New)",
                "product_status": "A",
                "deleted_product": 1,
                "discount": 0,
                "company_id": "56",
                "base_price": 12,
                "original_price": 12,
                "cart_id": "3463773863",
                "tax_value": 0,
                "subtotal": 24,
                "shipped_amount": 0,
                "shipment_amount": "2",
                "is_accessible": 1,
                "product_url": "http://stage-marketplace.cubework.com/toys-games-and-hobbies/test-a-doll/?variation_id=4925",
                "reviews": {
                    "count": 0,
                    "average_rating": "0.00"
                },
                "ga_category_name": "Toys, Games, & Hobbies",
                "variation_feature_ids": {
                    "552": "552",
                    "553": "553"
                },
                "variation_feature_collection": {
                    "552": {
                        "feature_id": "552",
                        "purpose": "group_variation_catalog_item"
                    },
                    "553": {
                        "feature_id": "553",
                        "purpose": "group_variation_catalog_item"
                    }
                },
                "variation_group_id": 170,
                "variation_group_code": "PV-22D659945",
                "variation_parent_product_id": 4926,
                "variation_sub_group_id": "170_4926",
                "variation_features": {
                    "552": {
                        "feature_id": "552",
                        "feature_style": "dropdown",
                        "position": "0",
                        "purpose": "group_variation_catalog_item",
                        "display_on_catalog": "N",
                        "description": "Product Type",
                        "internal_name": "Product Type",
                        "prefix": "",
                        "suffix": "",
                        "display_no_stock": "N",
                        "purpose_position": "1",
                        "variant": "Single Item (Sell Per Piece)",
                        "variant_id": "1209",
                        "variant_position": "0",
                        "dev_key": "single_item"
                    },
                    "553": {
                        "feature_id": "553",
                        "feature_style": "dropdown",
                        "position": "0",
                        "purpose": "group_variation_catalog_item",
                        "display_on_catalog": "N",
                        "description": "Condition",
                        "internal_name": "Condition",
                        "prefix": "",
                        "suffix": "",
                        "display_no_stock": "N",
                        "purpose_position": "1",
                        "variant": "New",
                        "variant_id": "1211",
                        "variant_position": "0",
                        "dev_key": "new"
                    }
                }
            }
        },
        "taxes": [],
        "tax_subtotal": 0,
        "display_shipping_cost": "0.00",
        "profile_update_timestamp": "",
        "is_root": "",
        "last_activity": "",
        "login_phone": "",
        "alternate_phone": "",
        "birthday": "",
        "purchase_timestamp_from": "",
        "purchase_timestamp_to": "",
        "responsible_email": "",
        "password_change_timestamp": "",
        "api_key": "",
        "helpdesk_user_id": "",
        "janrain_identifier": "",
        "has_read_guide": "",
        "employee_number": "",
        "user_alter": "",
        "is_phone_login": "",
        "is_email_login": "",
        "user_country_code": "",
        "b_country_descr": "United States",
        "s_country_descr": "United States",
        "b_state_descr": "California",
        "s_state_descr": "California",
        "need_shipping": 1,
        "shipping": [
            {
                "shipping_id": "24",
                "shipping": "local pick up",
                "delivery_time": "",
                "description": "",
                "rate_calculation": "R",
                "service_params": {
                    "active_stores": ""
                },
                "destination": "I",
                "min_weight": "0.000",
                "max_weight": "0.000",
                "service_id": "599",
                "free_shipping": 1,
                "module": "store_locator",
                "service_code": "pickup",
                "is_address_required": "N",
                "rate_info": {
                    "rate_id": "307",
                    "shipping_id": "24",
                    "rate_value": 1,
                    "destination_id": "21",
                    "base_rate": "0.00"
                },
                "image": [],
                "group_key": 0,
                "rate": 0,
                "data": {
                    "stores": {
                        "12": {
                            "store_location_id": "12",
                            "company_id": "56",
                            "position": "110",
                            "country": "US",
                            "state": "AL",
                            "latitude": "32.3182314",
                            "longitude": "-86.902298",
                            "localization": "",
                            "status": "A",
                            "main_destination_id": 1,
                            "pickup_destinations_ids": "0",
                            "zipcode": "28677",
                            "lang_code": "en",
                            "name": "test store location",
                            "description": "",
                            "city": "alabama",
                            "pickup_address": "alabama 1182 7030 Vally View St 9-5",
                            "pickup_phone": "",
                            "pickup_time": "",
                            "pickup_rate": 0,
                            "delivery_time": ""
                        },
                        "13": {
                            "store_location_id": "13",
                            "company_id": "56",
                            "position": "120",
                            "country": "US",
                            "state": "IN",
                            "latitude": "39.768403",
                            "longitude": "-86.158068",
                            "localization": "",
                            "status": "A",
                            "main_destination_id": "7",
                            "pickup_destinations_ids": "7",
                            "zipcode": "11134",
                            "lang_code": "en",
                            "name": "J.B.I INC.",
                            "description": "",
                            "city": "indiana",
                            "pickup_address": "indiana 12333",
                            "pickup_phone": "",
                            "pickup_time": "",
                            "pickup_rate": 0,
                            "delivery_time": ""
                        },
                        "16": {
                            "store_location_id": "16",
                            "company_id": "56",
                            "position": "150",
                            "country": "US",
                            "state": "CT",
                            "latitude": "54.308863191512174",
                            "longitude": "48.393487354189446",
                            "localization": "",
                            "status": "A",
                            "main_destination_id": 1,
                            "pickup_destinations_ids": "0",
                            "zipcode": "28677",
                            "lang_code": "en",
                            "name": "test location2",
                            "description": "",
                            "city": "",
                            "pickup_address": "",
                            "pickup_phone": "",
                            "pickup_time": "",
                            "pickup_rate": 0,
                            "delivery_time": ""
                        },
                        "18": {
                            "store_location_id": "18",
                            "company_id": "56",
                            "position": "160",
                            "country": "AT",
                            "state": "",
                            "latitude": "54.30175122530816",
                            "longitude": "48.397650718688965",
                            "localization": "",
                            "status": "A",
                            "main_destination_id": "29",
                            "pickup_destinations_ids": "29",
                            "zipcode": "",
                            "lang_code": "en",
                            "name": "pick up location2",
                            "description": "",
                            "city": "",
                            "pickup_address": "",
                            "pickup_phone": "",
                            "pickup_time": "",
                            "pickup_rate": 0,
                            "delivery_time": ""
                        }
                    }
                },
                "taxed_price": 0,
                "group_name": "Pennie Test length Test length Test length Test length Test length",
                "store_location_id": "12",
                "store_data": {
                    "store_location_id": "12",
                    "company_id": "56",
                    "position": "110",
                    "country": "US",
                    "state": "AL",
                    "latitude": "32.3182314",
                    "longitude": "-86.902298",
                    "localization": "",
                    "status": "A",
                    "main_destination_id": 1,
                    "pickup_destinations_ids": "0",
                    "zipcode": "28677",
                    "lang_code": "en",
                    "name": "test store location",
                    "description": "",
                    "city": "alabama",
                    "pickup_address": "alabama 1182 7030 Vally View St 9-5",
                    "pickup_phone": "",
                    "pickup_time": "",
                    "pickup_rate": 0,
                    "delivery_time": ""
                },
                "need_shipment": 1
            }
        ],
        "shipment_ids": [],
        "coupons": {
            "123123": [
                15
            ]
        },
        "secondary_currency": "USD",
        "user_type": "V",
        "display_subtotal": 24,
        "payment_info": [],
        "product_groups": [
            {
                "name": "Pennie Test length Test length Test length Test length Test length",
                "company_id": 56,
                "products": {
                    "3463773863": {
                        "product_id": 4925,
                        "product_code": "EA",
                        "product": "test a doll",
                        "amount": 2,
                        "product_options": [],
                        "price": 12,
                        "stored_price": "N",
                        "main_pair": {
                            "pair_id": "34231",
                            "image_id": "0",
                            "detailed_id": "35934",
                            "position": "0",
                            "object_id": "4925",
                            "object_type": "product",
                            "detailed": {
                                "object_id": "4925",
                                "object_type": "product",
                                "type": "M",
                                "image_path": "https://stage-marketplace.cubework.com/images/detailed/35/058b927f0c5c29aa190e8e022f7ec990.jpeg",
                                "alt": "",
                                "image_x": "1079",
                                "image_y": "1440",
                                "http_image_path": "http://stage-marketplace.cubework.com/images/detailed/35/058b927f0c5c29aa190e8e022f7ec990.jpeg",
                                "https_image_path": "https://stage-marketplace.cubework.com/images/detailed/35/058b927f0c5c29aa190e8e022f7ec990.jpeg",
                                "absolute_path": "/app/images/detailed/35/058b927f0c5c29aa190e8e022f7ec990.jpeg",
                                "relative_path": "detailed/35/058b927f0c5c29aa190e8e022f7ec990.jpeg",
                                "is_high_res": 1
                            }
                        },
                        "extra": {
                            "product_options": [],
                            "unlimited_download": "N",
                            "updated_timestamp": "1710819282",
                            "return_period": "10"
                        },
                        "stored_discount": "N",
                        "company_id": "56",
                        "return_period": "10",
                        "amount_total": 2,
                        "options_type": "P",
                        "exceptions_type": "F",
                        "options_type_raw": 1,
                        "exceptions_type_raw": 1,
                        "modifiers_price": 0,
                        "is_edp": "N",
                        "edp_shipping": "N",
                        "discount": 0,
                        "promotions": [],
                        "average_tax_value": 0,
                        "average_shipping_cost": 0,
                        "average_discount_applied": 4.8,
                        "base_price": 12,
                        "category_ids": [
                            386
                        ],
                        "display_price": 12,
                        "main_category": 386
                    }
                },
                "group_key": 56,
                "package_info": {
                    "C": 24,
                    "W": "0.001",
                    "I": 2,
                    "shipping_freight": 0,
                    "packages": [
                        {
                            "products": {
                                "3463773863": 2
                            },
                            "amount": 2,
                            "weight": 0.1,
                            "cost": 24
                        }
                    ],
                    "origination": {
                        "name": "Pennie Test length Test length Test length Test length Test length",
                        "address": "FuJianSheng2222  testunit1111",
                        "city": "Xia Men ShI111   testunit1111",
                        "country": "BO",
                        "state": "state333",
                        "zipcode": "99032",
                        "phone": "+1(212)121-2212",
                        "company_id": "56"
                    },
                    "location": {
                        "firstname": "1111",
                        "lastname": "1111",
                        "address": "1111",
                        "city": "1111",
                        "state": "CA",
                        "country": "US",
                        "zipcode": "01342",
                        "phone": "+1(111)111-1111",
                        "country_descr": "United States",
                        "state_descr": "California",
                        "address_type": "residential"
                    }
                },
                "package_info_full": {
                    "C": 24,
                    "W": "0.001",
                    "I": 2,
                    "shipping_freight": 0,
                    "packages": [
                        {
                            "products": {
                                "3463773863": 2
                            },
                            "amount": 2,
                            "weight": 0.1,
                            "cost": 24
                        }
                    ],
                    "origination": {
                        "name": "Pennie Test length Test length Test length Test length Test length",
                        "address": "FuJianSheng2222  testunit1111",
                        "city": "Xia Men ShI111   testunit1111",
                        "country": "BO",
                        "state": "state333",
                        "zipcode": "99032",
                        "phone": "+1(212)121-2212",
                        "company_id": "56"
                    },
                    "location": {
                        "firstname": "1111",
                        "lastname": "1111",
                        "address": "1111",
                        "city": "1111",
                        "state": "CA",
                        "country": "US",
                        "zipcode": "01342",
                        "phone": "+1(111)111-1111",
                        "country_descr": "United States",
                        "state_descr": "California",
                        "address_type": "residential"
                    }
                },
                "all_edp_free_shipping": 1,
                "all_free_shipping": 1,
                "free_shipping": 1,
                "shipping_no_required": 1,
                "shipping_by_marketplace": 1,
                "shippings": {
                    "24": {
                        "shipping_id": "24",
                        "shipping": "local pick up",
                        "delivery_time": "",
                        "description": "",
                        "rate_calculation": "R",
                        "service_params": {
                            "active_stores": ""
                        },
                        "destination": "I",
                        "min_weight": "0.000",
                        "max_weight": "0.000",
                        "service_id": "599",
                        "free_shipping": 1,
                        "module": "store_locator",
                        "service_code": "pickup",
                        "is_address_required": "N",
                        "rate_info": {
                            "rate_id": "307",
                            "shipping_id": "24",
                            "rate_value": 1,
                            "destination_id": "21",
                            "base_rate": "0.00"
                        },
                        "image": [],
                        "group_key": 0,
                        "rate": 0,
                        "data": {
                            "stores": {
                                "12": {
                                    "store_location_id": "12",
                                    "company_id": "56",
                                    "position": "110",
                                    "country": "US",
                                    "state": "AL",
                                    "latitude": "32.3182314",
                                    "longitude": "-86.902298",
                                    "localization": "",
                                    "status": "A",
                                    "main_destination_id": 1,
                                    "pickup_destinations_ids": "0",
                                    "zipcode": "28677",
                                    "lang_code": "en",
                                    "name": "test store location",
                                    "description": "",
                                    "city": "alabama",
                                    "pickup_address": "alabama 1182 7030 Vally View St 9-5",
                                    "pickup_phone": "",
                                    "pickup_time": "",
                                    "pickup_rate": 0,
                                    "delivery_time": ""
                                },
                                "13": {
                                    "store_location_id": "13",
                                    "company_id": "56",
                                    "position": "120",
                                    "country": "US",
                                    "state": "IN",
                                    "latitude": "39.768403",
                                    "longitude": "-86.158068",
                                    "localization": "",
                                    "status": "A",
                                    "main_destination_id": "7",
                                    "pickup_destinations_ids": "7",
                                    "zipcode": "11134",
                                    "lang_code": "en",
                                    "name": "J.B.I INC.",
                                    "description": "",
                                    "city": "indiana",
                                    "pickup_address": "indiana 12333",
                                    "pickup_phone": "",
                                    "pickup_time": "",
                                    "pickup_rate": 0,
                                    "delivery_time": ""
                                },
                                "16": {
                                    "store_location_id": "16",
                                    "company_id": "56",
                                    "position": "150",
                                    "country": "US",
                                    "state": "CT",
                                    "latitude": "54.308863191512174",
                                    "longitude": "48.393487354189446",
                                    "localization": "",
                                    "status": "A",
                                    "main_destination_id": 1,
                                    "pickup_destinations_ids": "0",
                                    "zipcode": "28677",
                                    "lang_code": "en",
                                    "name": "test location2",
                                    "description": "",
                                    "city": "",
                                    "pickup_address": "",
                                    "pickup_phone": "",
                                    "pickup_time": "",
                                    "pickup_rate": 0,
                                    "delivery_time": ""
                                },
                                "18": {
                                    "store_location_id": "18",
                                    "company_id": "56",
                                    "position": "160",
                                    "country": "AT",
                                    "state": "",
                                    "latitude": "54.30175122530816",
                                    "longitude": "48.397650718688965",
                                    "localization": "",
                                    "status": "A",
                                    "main_destination_id": "29",
                                    "pickup_destinations_ids": "29",
                                    "zipcode": "",
                                    "lang_code": "en",
                                    "name": "pick up location2",
                                    "description": "",
                                    "city": "",
                                    "pickup_address": "",
                                    "pickup_phone": "",
                                    "pickup_time": "",
                                    "pickup_rate": 0,
                                    "delivery_time": ""
                                }
                            }
                        },
                        "taxed_price": 0
                    },
                    "-1": {
                        "shipping_id": "-1",
                        "shipping": "No shipping methods are available",
                        "delivery_time": "",
                        "description": " ",
                        "rate_calculation": "M",
                        "service_params": [],
                        "destination": "I",
                        "min_weight": "0.000",
                        "max_weight": "0.000",
                        "service_id": "0",
                        "free_shipping": 1,
                        "module": 1,
                        "service_code": 1,
                        "is_address_required": "Y",
                        "rate_info": [],
                        "image": [],
                        "group_key": 0,
                        "rate": 0,
                        "taxed_price": 0
                    }
                },
                "chosen_shippings": [
                    {
                        "shipping_id": "24",
                        "shipping": "local pick up",
                        "delivery_time": "",
                        "description": "",
                        "rate_calculation": "R",
                        "service_params": {
                            "active_stores": ""
                        },
                        "destination": "I",
                        "min_weight": "0.000",
                        "max_weight": "0.000",
                        "service_id": "599",
                        "free_shipping": 1,
                        "module": "store_locator",
                        "service_code": "pickup",
                        "is_address_required": "N",
                        "rate_info": {
                            "rate_id": "307",
                            "shipping_id": "24",
                            "rate_value": 1,
                            "destination_id": "21",
                            "base_rate": "0.00"
                        },
                        "image": [],
                        "group_key": 0,
                        "rate": 0,
                        "data": {
                            "stores": {
                                "12": {
                                    "store_location_id": "12",
                                    "company_id": "56",
                                    "position": "110",
                                    "country": "US",
                                    "state": "AL",
                                    "latitude": "32.3182314",
                                    "longitude": "-86.902298",
                                    "localization": "",
                                    "status": "A",
                                    "main_destination_id": 1,
                                    "pickup_destinations_ids": "0",
                                    "zipcode": "28677",
                                    "lang_code": "en",
                                    "name": "test store location",
                                    "description": "",
                                    "city": "alabama",
                                    "pickup_address": "alabama 1182 7030 Vally View St 9-5",
                                    "pickup_phone": "",
                                    "pickup_time": "",
                                    "pickup_rate": 0,
                                    "delivery_time": ""
                                },
                                "13": {
                                    "store_location_id": "13",
                                    "company_id": "56",
                                    "position": "120",
                                    "country": "US",
                                    "state": "IN",
                                    "latitude": "39.768403",
                                    "longitude": "-86.158068",
                                    "localization": "",
                                    "status": "A",
                                    "main_destination_id": "7",
                                    "pickup_destinations_ids": "7",
                                    "zipcode": "11134",
                                    "lang_code": "en",
                                    "name": "J.B.I INC.",
                                    "description": "",
                                    "city": "indiana",
                                    "pickup_address": "indiana 12333",
                                    "pickup_phone": "",
                                    "pickup_time": "",
                                    "pickup_rate": 0,
                                    "delivery_time": ""
                                },
                                "16": {
                                    "store_location_id": "16",
                                    "company_id": "56",
                                    "position": "150",
                                    "country": "US",
                                    "state": "CT",
                                    "latitude": "54.308863191512174",
                                    "longitude": "48.393487354189446",
                                    "localization": "",
                                    "status": "A",
                                    "main_destination_id": 1,
                                    "pickup_destinations_ids": "0",
                                    "zipcode": "28677",
                                    "lang_code": "en",
                                    "name": "test location2",
                                    "description": "",
                                    "city": "",
                                    "pickup_address": "",
                                    "pickup_phone": "",
                                    "pickup_time": "",
                                    "pickup_rate": 0,
                                    "delivery_time": ""
                                },
                                "18": {
                                    "store_location_id": "18",
                                    "company_id": "56",
                                    "position": "160",
                                    "country": "AT",
                                    "state": "",
                                    "latitude": "54.30175122530816",
                                    "longitude": "48.397650718688965",
                                    "localization": "",
                                    "status": "A",
                                    "main_destination_id": "29",
                                    "pickup_destinations_ids": "29",
                                    "zipcode": "",
                                    "lang_code": "en",
                                    "name": "pick up location2",
                                    "description": "",
                                    "city": "",
                                    "pickup_address": "",
                                    "pickup_phone": "",
                                    "pickup_time": "",
                                    "pickup_rate": 0,
                                    "delivery_time": ""
                                }
                            }
                        },
                        "taxed_price": 0,
                        "group_name": "Pennie Test length Test length Test length Test length Test length",
                        "store_location_id": "12",
                        "store_data": {
                            "store_location_id": "12",
                            "company_id": "56",
                            "position": "110",
                            "country": "US",
                            "state": "AL",
                            "latitude": "32.3182314",
                            "longitude": "-86.902298",
                            "localization": "",
                            "status": "A",
                            "main_destination_id": 1,
                            "pickup_destinations_ids": "0",
                            "zipcode": "28677",
                            "lang_code": "en",
                            "name": "test store location",
                            "description": "",
                            "city": "alabama",
                            "pickup_address": "alabama 1182 7030 Vally View St 9-5",
                            "pickup_phone": "",
                            "pickup_time": "",
                            "pickup_rate": 0,
                            "delivery_time": ""
                        }
                    }
                ]
            }
        ],
        "doc_ids": [],
        "order_url": "http://stage-marketplace.cubework.com/index.php?dispatch=orders.details&order_id=1743",
        "store_url": "http://stage-marketplace.cubework.com/index.php?dispatch=companies.vendor_store&cid=56",
        "refunds_total": 0
    }
    print(run(data))
