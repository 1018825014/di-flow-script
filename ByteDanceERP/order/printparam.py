import json


def run(event_dict):
    params = event_dict['outPut']


    result = {
        'params': params,
        'method': method,
        'uri': uri,
        'url': url,
        'code': code
    }

    return json.dumps(result)
