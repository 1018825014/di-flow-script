import json
from datetime import datetime, timedelta

def run(event_dict):
    current_time = datetime.utcnow()
    two_years_ago = current_time - timedelta(days=365 * 2 + 1)
    formatted_time = two_years_ago.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    LastUpdateDate = event_dict.get('LastUpdateDate')
    createdAt = event_dict.get('created_at_min')

    result = {}
    if LastUpdateDate:
        result['LastUpdateDate'] = LastUpdateDate
    else:
        if createdAt:
            if createdAt < formatted_time:
                createdAt = formatted_time
            result['LastUpdateDate'] = createdAt
        else:
            result['LastUpdateDate'] = formatted_time

    return json.dumps(result)

# Test cases

# Case 1: No dates provided
print(run({}))

# Case 2: Only LastUpdateDate provided
print(run({"LastUpdateDate": "2023-03-02T16:00:01.000Z"}))

# Case 3: Only createdAt provided, older than two years ago
two_years_old = (datetime.utcnow() - timedelta(days=365 * 2 + 100)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
print(run({"created_at_min": two_years_old}))

# Case 4: Only createdAt provided, newer than two years ago
recent_date = (datetime.utcnow() - timedelta(days=100)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
print(run({"created_at_min": recent_date}))

# Case 5: Both dates provided
print(run({"LastUpdateDate": "2023-03-02T16:00:01.000Z", "created_at_min": two_years_old}))
