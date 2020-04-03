""" main handler that handle http requests to yandex cloud """

import boto3
import subprocess
from verdict_codes import *

PYTHON_VERSION = 'python3.7'

def status_to_queue(ip, port, round, status):

    #TODO add aws_access_key_id and aws_secret_access_key

    # Create client
    client = boto3.client(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )


    # Create queue and get its url
    queue_url = client.create_queue(QueueName='checker-response-queue').get('QueueUrl')
    print('Created queue url is "{}"'.format(queue_url))


    # Send message to queue
        client.send_message(
            QueueUrl=queue_url,
            MessageBody='{},{},{},{}'.format(ip, port, round, status),
            MessageAttributes={
                        "ip": {
                            "StringValue": str(ip),
                            "DataType": "Number"
                        },
                        "port": {
                            "StringValue": str(port),
                            "DataType": "Number"
                        },
                        "round": {
                            "StringValue": str(round),
                            "DataType": "Number"
                        }
                        "status": {
                            "StringValue": str(status),
                            "DataType": "Number"
                        }
                    }
        )

def handle_http(event):

    # Check if ip, port, round in queryStringParameters
    for parameter in ('ip', 'port', 'round'):
        if parameter not in event['queryStringParameters']:
            return YC_ERROR
    
    # Run checker
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
        # Trigger can get more than 1 message
        # To recieve all messages trigger should take only 1 message in group
        # Get first message
        message = event['messages'][0]

        parameters = message['details']['message']['message_attributes']
        ip = parameters['ip']['stringValue']
        port = parameters['port']['stringValue']
        round = parameters['round']['stringValue']


        # Run checker
        response = subprocess.run([PYTHON_VERSION, 'main.py', '--ip', ip, '--port', port, '--round', round], stdout=subprocess.PIPE)
        response_text = response.stdout.decode('utf-8').split('\n')[:-1]

        response_error, response_code = "", None
        if len(response_text) > 1:
            response_error = response_text[0]
        response_code = response_text[-1]

        status_to_queue(ip, port, round, response_code)
        return {
            'statusCode': response_code,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'isBase64Encoded': False,
            'body': response_error
        }
    except:
        status_to_queue(ip, port, round, CHECKER_ERROR)
        return YC_ERROR

def handler(event, context):

    
    if 'queryStringParameters' in event:
        return handle_http(event)

    if 'messages' in event:
        return handle_queue_message(event)

    return YC_ERROR
