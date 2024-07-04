import json


def run(event_dict):
    LastUpdateDate = event_dict.get('LastUpdateDate')
    createdAt = event_dict.get('created_at_min')
    result = {}
    if LastUpdateDate :
        result['LastUpdateDate'] = LastUpdateDate

    else:
        if createdAt :
            result['LastUpdateDate'] = createdAt
        else:
            result['LastUpdateDate'] = '2000-01-01T00:00:00Z'


    return json.dumps(result)