import json
from datetime import datetime


def run(data):
    # to json
    warehouseList = json.loads(data['orderData'])