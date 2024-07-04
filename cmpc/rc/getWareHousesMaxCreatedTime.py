


def run(event_dict):
    createWhen = event_dict.get('lastCreatedTime')
    lastQueryTime = event_dict.get('lastQueryTime')
    wmsResponse = json.loads(event_dict['warehousesDCResponse'])
    created_when_list = [item['CreatedWhen'] for item in wmsResponse]
    if createWhen:
        created_when_list.append(createWhen)

    if lastQueryTime:
        created_when_list.append(lastQueryTime)

    max_created_when = '2024-01-01T00:00:00.000'
    if created_when_list:
        max_created_when = max(created_when_list)

    data = {'CreatedWhen': max_created_when}
    json_data = json.dumps(data)
    return json_data