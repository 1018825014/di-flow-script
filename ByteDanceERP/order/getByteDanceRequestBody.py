
import json
from datetime import datetime, timedelta
def run(event_dict):
    body = json.loads(event_dict['hookBody'])




    return json.dumps(json.loads(event_dict['hookBody']))