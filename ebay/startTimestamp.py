import json
from datetime import datetime, timedelta

def run(event_dict):
    maxDateTime_str = event_dict.get('maxDateTime', None)
    created_at_min_str = event_dict.get('created_at_min', None)

    if maxDateTime_str is not None:
        return json.dumps({'startTimestamp': maxDateTime_str})
    elif created_at_min_str is not None:
        if created_at_min_str == '':
            return json.dumps({})
        try:
            # Check if the timezone is 'Z' for UTC or contains offset
            if created_at_min_str.endswith('Z'):
                formatted_utc = created_at_min_str[:-1] + '.000Z'
            else:
                date_part, time_part = created_at_min_str.split('T')
                year, month, day = map(int, date_part.split('-'))
                if '+' in time_part:
                    time_part, tz_part = time_part.split('+')
                    tz_hour, tz_minute = map(int, tz_part.split(':'))
                else:
                    # No timezone offset provided, assume UTC
                    tz_hour = 0
                    tz_minute = 0

                hour, minute, second = map(int, time_part.split(':'))

                dt = datetime(year, month, day, hour, minute, second)
                utc_dt = dt - timedelta(hours=tz_hour, minutes=tz_minute)
                formatted_utc = utc_dt.strftime('%Y-%m-%dT%H:%M:%S') + '.000Z'

            return json.dumps({'startTimestamp': formatted_utc})
        except ValueError as e:
            return json.dumps({'error': f'Invalid datetime format: {str(e)}'})
    else:
        return json.dumps({})

def main():
    # Test cases
    test_cases = [
        # Case 1: maxDateTime is provided
        {'maxDateTime': '2024-05-23T10:00:00Z'},
        # Case 2: created_at_min is provided with 'Z' (UTC)
        {'created_at_min': '2024-05-23T10:00:00Z'},
        # Case 3: created_at_min is provided with timezone offset
        {'created_at_min': '2024-05-23T10:00:00+02:00'},
        # Case 4: created_at_min is provided without timezone (assume UTC)
        {'created_at_min': '2024-05-23T10:00:00'},
        # Case 5: created_at_min is an empty string
        {'created_at_min': ''},
        {'maxDateTime': ''},
        # Case 6: No datetime provided
        {}
    ]

    # Run the test cases
    for i, test_case in enumerate(test_cases):
        result = run(test_case)
        print(f"Test Case {i+1}: {test_case}\nResult: {result}\n")


if __name__ == "__main__":
    main()
