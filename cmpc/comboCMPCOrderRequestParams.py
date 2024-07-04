def run(data):
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
            'Desc': 'Jacksonville'
        },
        {
            'WarehouseID': '6111_106',
            'FacilityID': '895',
            'Desc': 'Houston'
        }
    ]
    requestParams = []
    for paramObject in paramObjects:
        requestParams.append(
            {
                'requestBody': {
                    'row': [
                        {
                            'WarehouseCompany': 'UNIS',
                            'WarehouseID': paramObject.get('WarehouseID'),
                            'Details': [
                                {
                                    'Status': 'NEW',
                                    'Message': ''
                                }
                            ]
                        }
                    ]
                },
                'facilityId': paramObject.get('FacilityID'),
                'facilityName': paramObject.get('Desc')
            }
        )
        return json.dumps(requestParams)