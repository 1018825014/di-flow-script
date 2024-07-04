def run(event_dict):
    orderData = {}
    orderData.update(event_dict['orderDatas'])
    orderData.update(event_dict['orderDataDetail'])

    return orderData