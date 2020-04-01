""" main handler that handle http requests to yandex cloud """

import subprocess
from verdict_codes import *

PYTHON_VERSION = 'python3.6'

def handler(event, context):

    if 'queryStringParameters' not in event:
        return {
            'statusCode': CHECKER_ERROR
        }

    for parameter in ('ip', 'port', 'round'):
        if parameter not in event['queryStringParameters']:
            return {
                'statusCode': CHECKER_ERROR
            }
    
    response = subprocess.run([PYTHON_VERSION, 'main.py', '--ip', event['queryStringParameters']['ip'], '--port', event['queryStringParameters']['port'], '--round', event['queryStringParameters']['round']], stdout=subprocess.PIPE)
    response_text = response.stdout.decode('utf-8')

    return {
        'statusCode': response_text
    }
