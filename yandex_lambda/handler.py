""" main handler that handle http requests to yandex cloud """

import subprocess
from verdict_codes import *

PYTHON_VERSION = 'python3.7'

def handler(event, context):

    if 'queryStringParameters' not in event:
        return {
            'statusCode': CHECKER_ERROR,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'isBase64Encoded': False,
            'body': ""
        }

    for parameter in ('ip', 'port', 'round'):
        if parameter not in event['queryStringParameters']:
            return {
                'statusCode': CHECKER_ERROR,
                'headers': {
                    'Content-Type': 'text/plain'
                },
                'isBase64Encoded': False,
                'body': ""
            }
    
    response = subprocess.run([PYTHON_VERSION, 'main.py', '--ip', event['queryStringParameters']['ip'], '--port', event['queryStringParameters']['port'], '--round', event['queryStringParameters']['round']], stdout=subprocess.PIPE)
    response_text = response.stdout.decode('utf-8').split('\n')[:-1]

    response_error, response_code = None, None
    if len(response_text) > 1:
        response_error = response_text[0]
    response_code = response_text[-1]

    return {
        'statusCode': response_code,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'isBase64Encoded': False,
        'body': ""
    }
