def run(data):
    statusEnum = ['NEW', 'RESUBMIT', 'RES-CONT']
    requestParams = []
    for status in statusEnum:
        requestParams.append(
            {
                'row': [
                    {
                        'WarehouseCompany': 'UNIS',
                        'Details': [
                            {
                                'Status': status,
                                'Message': ''
                            }
                        ]
                    }
                ]

            }
        )
    return json.dumps(requestParams)