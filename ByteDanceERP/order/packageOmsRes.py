import json
from datetime import datetime, timedelta


import json

def run(event_dict):
    res = json.loads(event_dict['omsRes'])
    code = res.get('code', 0)
    data = res.get('data', {})
    msg = res.get('msg', '')

    if code == 0:
        success = True
    else:
        success = False
    code = str(code)

    hookRes = {
        'code': code,
        'success': success,
        'msg': msg
    }

    return json.dumps(hookRes)

if __name__ == '__main__':
    data = {"omsRes":"{\"code\":3000011,\"data\":null,\"msg\":\" channel order number and reference number already "
                     "exists\"}"}
    print(run(data))
