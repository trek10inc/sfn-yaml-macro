import json

def handler(event, context):
    print('Event', json.dumps(event, default=str))
    return event
