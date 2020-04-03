""" main handler that handle http requests to yandex cloud """

import subprocess
from verdict_codes import *

PYTHON_VERSION = 'python3.7'

def handle_http(event):
    for parameter in ('ip', 'port', 'round'):
        if parameter not in event['queryStringParameters']:
            return YC_ERROR
    
    response = subprocess.run([PYTHON_VERSION, 'main.py', '--ip', event['queryStringParameters']['ip'], '--port', event['queryStringParameters']['port'], '--round', event['queryStringParameters']['round']], stdout=subprocess.PIPE)
    response_text = response.stdout.decode('utf-8').split('\n')[:-1]

    response_error, response_code = "", None
    if len(response_text) > 1:
        response_error = response_text[0]
    response_code = response_text[-1]

    return {
        'statusCode': response_code,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'isBase64Encoded': False,
        'body': response_error
    }

def handle_queue_message(event):

    try:
        message = event['messages'][0]

        parameters = message['details']['message']['message_attributes']
        ip = parameters['ip']['stringValue']
        port = parameters['port']['stringValue']
        round = parameters['round']['stringValue']

        response = subprocess.run([PYTHON_VERSION, 'main.py', '--ip', ip, '--port', port, '--round', round], stdout=subprocess.PIPE)
        response_text = response.stdout.decode('utf-8').split('\n')[:-1]

        response_error, response_code = "", None
        if len(response_text) > 1:
            response_error = response_text[0]
        response_code = response_text[-1]

        return {
            'statusCode': response_code,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'isBase64Encoded': False,
            'body': response_error
        }
    except:
        return YC_ERROR

def handler(event, context):

    
    if 'queryStringParameters' in event:
        return handle_http(event)

    if 'messages' in event:
        return handle_queue_message(event)

    return YC_ERROR
