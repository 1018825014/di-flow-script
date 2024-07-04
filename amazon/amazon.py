def run(event_dict):
    created_at_min = event_dict.get('created_at_min')
    created_start_date = event_dict.get('createdStartDate', '')
    created_at_min = created_at_min[:-6] + 'Z'
    query_time = created_start_date or created_at_min

    return json.dumps({'queryTime': query_time})